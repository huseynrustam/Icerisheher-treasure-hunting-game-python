import os

from file_manager import FileManager
from location import Location
from player import Player
from question_manager import QuestionManager


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions.txt")
SCORES_FILE = os.path.join(BASE_DIR, "scores.txt")

# This dictionary is the real game map.
# Each key is a location, and each list contains places connected to it.
MAP_CONNECTIONS = {
    "Watch Tower": ["Shirvanshahs' Palace"],
    "Shirvanshahs' Palace": ["Watch Tower", "Juma Mosque"],
    "Juma Mosque": ["Shirvanshahs' Palace", "Fortress Walls", "Market Square"],
    "Fortress Walls": ["Juma Mosque", "Maiden Tower", "Caravanserai"],
    "Maiden Tower": ["Fortress Walls", "Market Square", "Small Fortress Street"],
    "Market Square": ["Juma Mosque", "Maiden Tower", "Caravanserai"],
    "Small Fortress Street": ["Maiden Tower", "Bathhouse"],
    "Bathhouse": ["Small Fortress Street"],
    "Caravanserai": ["Fortress Walls", "Market Square", "Underground Tunnel"],
    "Underground Tunnel": ["Caravanserai", "Old Well"],
    "Old Well": ["Underground Tunnel"],
}

# This clue is only shown after the player finds the old key
# and answers the special key question correctly.
TREASURE_CLUE = (
    "The key's marks point up from the old water and beyond the Friday stones; "
    "the final door waits beneath the shadow of the watch tower."
)

TREASURE_CLUE_QUESTION = (
    "The old key has a long inscription: 'I am not kept where travelers slept, "
    "not where water washed the dust away, and not where the crowd first enters. "
    "I belong where decisions were made, ceremonies were held, and rulers guarded their secrets.' "
    "What kind of place is the inscription describing?"
)

TREASURE_CLUE_ANSWER = "palace"


class TreasureGame:
    """Main game class."""

    def __init__(self):
        # The locations dictionary stores every Location object by name.
        self.locations = {}

        # The player is created when the game starts or restarts.
        self.player = None

        # These values track the current game session.
        self.moves = 0
        self.game_over = False
        self.result_message = "Game not completed."

        # Searched places do not give repeated points.
        self.searched_locations = set()

        # This becomes True only after the key's harder question is solved.
        self.treasure_clue_revealed = False

        # Helper classes handle questions and saving scores.
        self.question_manager = QuestionManager(QUESTIONS_FILE)
        self.file_manager = FileManager(SCORES_FILE)

        # Build the map once, then create the first player state.
        self.build_map()
        self.restart_game(show_intro=False)

    def build_map(self):
        """Create locations and connect them as a graph."""
        self.locations = {
            "Fortress Walls": Location(
                "Fortress Walls",
                "You stand beside the ancient stone walls of Icherisheher.",
                "The walls keep the city safe, but they do not keep the secret. Begin where the old city can be seen from above.",
            ),
            "Maiden Tower": Location(
                "Maiden Tower",
                "The famous tower stands tall above the old city and looks toward the sea.",
                "A tower helps you see far, but the secret is not kept in open sight. Search the roads that lead below the busy streets.",
            ),
            "Market Square": Location(
                "Market Square",
                "The square is full of old trade routes, footsteps, and city noise.",
                "Crowds leave too many tracks. A quieter path near merchants may hide what you need.",
            ),
            "Small Fortress Street": Location(
                "Small Fortress Street",
                "A narrow old street runs through the heart of the fortress.",
                "This street carries you inward, but it does not keep the key.",
            ),
            "Bathhouse": Location(
                "Bathhouse",
                "The old bathhouse is quiet. It was built for rest, water, and cleaning.",
                "Water removes dust, but it also washes signs away. The secret is not hidden here.",
            ),
            "Caravanserai": Location(
                "Caravanserai",
                "This old travelers' inn once welcomed merchants, guests, and stories from far away.",
                "Travelers carried stories about hidden doors. The oldest clue may be deeper than the inn itself.",
            ),
            "Underground Tunnel": Location(
                "Underground Tunnel",
                "A narrow tunnel runs below the old stones of Icherisheher.",
                "The air is cold here, and every step sounds close to a hidden chamber.",
            ),
            "Old Well": Location(
                "Old Well",
                "An old stone well waits in the deepest part of the route.",
                "The well does not hold treasure, but it guarded something small enough to open the next secret.",
                item="old key",
            ),
            "Juma Mosque": Location(
                "Juma Mosque",
                "The mosque stands on a calm stone path inside the old city.",
                "The stones here point along a solemn path. If the key has spoken, follow what it told you.",
            ),
            "Shirvanshahs' Palace": Location(
                "Shirvanshahs' Palace",
                "You see the palace, an important place connected with rulers and old history.",
                "Only the old key can explain why this guarded place matters.",
                item="treasure",
            ),
            "Watch Tower": Location(
                "Watch Tower",
                "A high watch tower looks across the old city's roofs and walls.",
                "The tower watches the secret from above, but the treasure is not kept in the open air.",
            ),
        }

        # Copy the neighbor lists from MAP_CONNECTIONS into the Location objects.
        for location_name, neighbors in MAP_CONNECTIONS.items():
            self.locations[location_name].neighbors = neighbors

    def show_intro(self):
        """Show the opening story and basic instruction."""
        print("\n" + "=" * 55)
        print("OLD CITY TREASURE HUNT")
        print("=" * 55)
        print(
            "You are exploring Baku Old City, also called Icherisheher.\n"
            "An old story says a hidden treasure is somewhere inside the walls.\n"
            "Find clues, discover the old key, and choose the right place to search."
        )
        print("\nType 'help' to see the commands.\n")

    def show_help(self):
        """Print all commands the player can type."""
        print("\nCommands:")
        print("  help                 Show this help message")
        print("  map                  Show the text map")
        print("  move <place>         Move to a connected place")
        print("  search               Answer a question and search for a clue")
        print("  hint                 Use one hint")
        print("  status               Show your score and progress")
        print("  restart              Start the game again")
        print("  exit                 Exit the game")

    def show_map(self):
        """Print a text version of the treasure map."""
        print(
            """
================= ICHERISHEHER TREASURE MAP =================

                           [ Watch Tower ]
                                  |
                                  |
                    [ Shirvanshahs' Palace ]
                                  |
                           [ Juma Mosque ]
                                  |
         -------------------------------------------------
         |                                               |
         |                                               |
 [ Fortress Walls ] ---- [ Maiden Tower ] ---- [ Market Square ]
         |                          |                      |
         |                          |                      |
         |                 [ Small Fortress Street ]      |
         |                          |                      |
         |                   [ Bathhouse ]                |
         |                                                 |
         ---------------- [ Caravanserai ] ----------------
                                   |
                            [ Underground Tunnel ]
                                   |
                               [ Old Well ]

================================================================
"""
        )

    def show_location(self):
        """Show the player's current location and possible moves."""
        location = self.locations[self.player.current_location]
        print(f"\nLocation: {location.name}")
        print(location.description)
        print("Connected places: " + ", ".join(location.neighbors))

    def move(self, destination):
        """Move the player to a connected location if the move is valid."""
        try:
            # Accept different capitalization from the player.
            destination = self.find_location_name(destination)
            current = self.locations[self.player.current_location]

            # A player can only move along map connections.
            if destination not in current.neighbors:
                raise ValueError(f"You cannot move from {current.name} to {destination}.")

            # The palace is locked until the old key is found.
            if destination == "Shirvanshahs' Palace" and "old key" not in self.player.inventory:
                print("\nThe palace is locked. You need an old key before entering.")
                return

            # Update location and count one successful move.
            self.player.current_location = destination
            self.moves += 1

            # Visiting a new place gives points once.
            if destination not in self.player.visited_places:
                self.player.visited_places.add(destination)
                self.player.score += 5
                print("\nNew location discovered! +5 points")

            # These places are allowed, but they warn the player they may not be central.
            if destination in ["Bathhouse", "Market Square"]:
                print("\nWarning: This place feels like a wrong path, but it may still teach you something.")

            self.show_location()

        except ValueError as error:
            print(f"\nMove error: {error}")

    def search(self):
        """Search the current location after answering a quiz question."""
        location = self.locations[self.player.current_location]

        # Searching the same place again repeats the clue but gives no new points.
        if location.name in self.searched_locations:
            print("\nYou already searched this place. Here is the clue again:")
            print(location.clue)
            # If the player found the key but missed its question, allow a retry.
            if location.item == "old key" and "old key" in self.player.inventory:
                self.reveal_treasure_clue()
            return

        print("\nBefore you can search, answer this question.")
        if self.ask_question():
            # A correct answer unlocks the location clue and gives points.
            self.player.score += 3
            self.searched_locations.add(location.name)
            print("\nCorrect! +3 points")
            print("Clue:")
            print(location.clue)

            # The old key unlocks the palace and starts the special clue challenge.
            if location.item == "old key" and "old key" not in self.player.inventory:
                self.player.inventory.append("old key")
                self.player.score += 10
                print("\nYou found an old key! +10 points")
                self.reveal_treasure_clue()

            # Finding the treasure ends the game with a win.
            if location.item == "treasure" and "treasure" not in self.player.inventory:
                self.player.inventory.append("treasure")
                self.player.score += 15
                self.result_message = "You found the treasure in Shirvanshahs' Palace. You win!"
                print("\nYou found the hidden treasure! +15 points")
                self.check_win()
        else:
            # Wrong answers lose a small number of points, but the player can retry.
            self.player.score -= 2
            print("\nWrong answer. -2 points")
            print("You did not reveal the clue. You can try searching again.")

    def reveal_treasure_clue(self):
        """Ask the key question and reveal the harder treasure clue if correct."""
        if self.treasure_clue_revealed:
            return

        print("\nThe key has writing on it. Answer this question to understand the message.")
        if self.ask_treasure_clue_question():
            self.treasure_clue_revealed = True
            self.player.score += 5
            print("\nYou understood the key's message! +5 points")
            print("Clue:")
            print(TREASURE_CLUE)
        else:
            print("\nThe inscription is still unclear. Search the key's place again to try reading it.")

    def ask_question(self):
        """Ask a random normal question and check the answer."""
        question_data = self.question_manager.get_random_question()
        if question_data is None:
            print("No valid questions are available, so the search cannot continue.")
            return False

        question, answer = question_data
        user_answer = input(question + " ").strip().lower()
        return user_answer == answer.lower()

    def ask_treasure_clue_question(self):
        """Ask the special question used to understand the old key."""
        user_answer = input(TREASURE_CLUE_QUESTION + " ").strip().lower()
        return user_answer == TREASURE_CLUE_ANSWER

    def give_hint(self):
        """Use one hint and print advice based on the player's progress."""
        if self.player.hints_left <= 0:
            self.end_game("You used all hints. Game over.")
            return

        self.player.hints_left -= 1
        current = self.player.current_location
        print(f"\nHint used. Hints left: {self.player.hints_left}")

        # Hints change depending on whether the key and treasure clue are found.
        if "old key" not in self.player.inventory:
            print("Search the lower route from the travelers' inn, then go deeper than the street level.")
        elif not self.treasure_clue_revealed:
            print("You have the key, but its message is still unread. Search the place where you found it again.")
        elif current != "Juma Mosque":
            print("You understood the key. Return to the tower and follow the quiet prayer path.")
        else:
            print("You are close. Trust the key's message and choose the guarded stone place.")

        if self.player.hints_left == 0:
            self.end_game("You used all hints. Game over.")

    def show_status(self):
        """Print the player's current progress."""
        print("\nStatus:")
        print(f"  Current location: {self.player.current_location}")
        print(f"  Score: {self.player.score}")
        print(f"  Moves: {self.moves}")
        print(f"  Hints left: {self.player.hints_left}")
        print(f"  Inventory: {', '.join(self.player.inventory) if self.player.inventory else 'empty'}")
        print(f"  Visited places: {', '.join(sorted(self.player.visited_places))}")

    def restart_game(self, show_intro=True):
        """Reset the game state and put the player back at the start."""
        self.player = Player("Fortress Walls")
        self.moves = 0
        self.game_over = False
        self.result_message = "Game restarted before completion."
        self.searched_locations = set()
        self.treasure_clue_revealed = False
        if show_intro:
            print("\nThe game has restarted.")
            self.show_intro()
            self.show_location()

    def check_win(self):
        """End the game if the treasure is in the player's inventory."""
        if "treasure" in self.player.inventory:
            self.end_game("You found the treasure in Shirvanshahs' Palace. You win!")

    def end_game(self, result_message):
        """Mark the game as finished, show the summary, and save the result."""
        self.result_message = result_message
        self.game_over = True
        self.show_summary()
        self.save_score()

    def show_summary(self):
        """Print the final game summary."""
        print("\n" + "=" * 55)
        print("FINAL SUMMARY")
        print("=" * 55)
        print(f"Result: {self.result_message}")
        print(f"Final score: {self.player.score}")
        print(f"Total moves: {self.moves}")
        print(f"Hints left: {self.player.hints_left}")
        print(f"Visited places: {', '.join(sorted(self.player.visited_places))}")
        print(f"Inventory: {', '.join(self.player.inventory) if self.player.inventory else 'empty'}")
        print("=" * 55)

    def save_score(self):
        """Send the final score data to FileManager."""
        self.file_manager.save_score(
            self.player.score,
            self.moves,
            self.player.hints_left,
            self.player.visited_places,
            self.player.inventory,
            self.result_message,
        )

    def find_location_name(self, text):
        """Find a location by name while ignoring capitalization."""
        for location_name in self.locations:
            if location_name.lower() == text.strip().lower():
                return location_name
        raise ValueError(f"'{text}' is not a known location.")

    def handle_command(self, command):
        """Read one player command and call the correct game method."""
        try:
            command = command.strip()
            if not command:
                raise ValueError("Please type a command.")

            lower_command = command.lower()

            if lower_command == "help":
                self.show_help()
            elif lower_command == "map":
                self.show_map()
            elif lower_command.startswith("move "):
                destination = command[5:].strip()
                if not destination:
                    raise ValueError("Please write a place after 'move'.")
                self.move(destination)
            elif lower_command == "search":
                self.search()
            elif lower_command == "hint":
                self.give_hint()
            elif lower_command == "status":
                self.show_status()
            elif lower_command == "restart":
                self.restart_game()
            elif lower_command == "exit":
                self.end_game("Player exited the game.")
            else:
                raise ValueError("Unknown command. Type 'help' to see valid commands.")
        except ValueError as error:
            print(f"\nCommand error: {error}")

    def play(self):
        """Run the main input loop until the game ends."""
        self.show_intro()
        self.show_location()

        while not self.game_over:
            try:
                command = input("\n> ")
                self.handle_command(command)
            except KeyboardInterrupt:
                print("\n\nKeyboard interrupt received. Exiting the game safely.")
                self.end_game("Player exited with keyboard interrupt.")
            except EOFError:
                print("\nInput ended. Exiting the game safely.")
                self.end_game("Input ended unexpectedly.")
