class Player:
    """Stores the player's current progress."""

    def __init__(self, start_location):
        # The player begins at the chosen starting location.
        self.current_location = start_location

        # Inventory stores collected items, such as the old key and treasure.
        self.inventory = []

        # Score increases for correct answers, new places, and important items.
        self.score = 0

        # A set avoids duplicate visited places.
        self.visited_places = {start_location}

        # The player has a limited number of hints before the game ends.
        self.hints_left = 3
