import os
import sys
import unittest
from unittest.mock import patch


# Add the project folder to Python's import path so tests can import game.py.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from game import TreasureGame


class TestTreasureGame(unittest.TestCase):
    """Tests for the main TreasureGame behavior."""

    def setUp(self):
        # Hide print output during tests so test results stay clean.
        self.print_patcher = patch("builtins.print")
        self.print_patcher.start()

        # Create a fresh game before each test.
        self.game = TreasureGame()

    def tearDown(self):
        # Stop hiding print output after each test.
        self.print_patcher.stop()

    def test_moving_to_connected_location_works(self):
        # Fortress Walls is connected to Maiden Tower, so this move should work.
        self.game.move("Maiden Tower")

        self.assertEqual(self.game.player.current_location, "Maiden Tower")
        self.assertEqual(self.game.moves, 1)

    def test_moving_to_unconnected_location_fails(self):
        # The palace is not directly connected to the start location.
        self.game.move("Shirvanshahs' Palace")

        self.assertEqual(self.game.player.current_location, "Fortress Walls")
        self.assertEqual(self.game.moves, 0)

    def test_palace_cannot_be_entered_without_old_key(self):
        # The player must find the old key before entering the palace.
        self.game.player.current_location = "Juma Mosque"

        self.game.move("Shirvanshahs' Palace")

        self.assertEqual(self.game.player.current_location, "Juma Mosque")

    def test_palace_can_be_entered_with_old_key(self):
        # Once the key is in the inventory, the palace door should open.
        self.game.player.current_location = "Juma Mosque"
        self.game.player.inventory.append("old key")

        self.game.move("Shirvanshahs' Palace")

        self.assertEqual(self.game.player.current_location, "Shirvanshahs' Palace")

    def test_finding_key_adds_old_key_to_inventory(self):
        # Old Well contains the old key.
        self.game.player.current_location = "Old Well"

        # Mock the questions so the test does not need keyboard input.
        with patch.object(self.game, "ask_question", return_value=True):
            with patch.object(self.game, "ask_treasure_clue_question", return_value=True):
                self.game.search()

        self.assertIn("old key", self.game.player.inventory)

    def test_finding_key_reveals_treasure_clue_after_harder_question(self):
        # The special treasure clue is only revealed after the key question.
        self.game.player.current_location = "Old Well"

        with patch.object(self.game, "ask_question", return_value=True):
            with patch.object(self.game, "ask_treasure_clue_question", return_value=True):
                self.game.search()

        self.assertTrue(self.game.treasure_clue_revealed)

    def test_key_clue_can_be_retried_after_wrong_harder_question(self):
        # If the special key question is wrong, the player can search again later.
        self.game.player.current_location = "Old Well"

        with patch.object(self.game, "ask_question", return_value=True):
            with patch.object(self.game, "ask_treasure_clue_question", return_value=False):
                self.game.search()

        self.assertFalse(self.game.treasure_clue_revealed)

        with patch.object(self.game, "ask_treasure_clue_question", return_value=True):
            self.game.search()

        self.assertTrue(self.game.treasure_clue_revealed)

    def test_finding_treasure_adds_treasure_to_inventory(self):
        # Searching the palace successfully should add treasure to inventory.
        self.game.player.current_location = "Shirvanshahs' Palace"

        with patch.object(self.game, "ask_question", return_value=True):
            # Stop the test from writing scores or printing a final summary.
            with patch.object(self.game, "show_summary"):
                with patch.object(self.game, "save_score"):
                    self.game.search()

        self.assertIn("treasure", self.game.player.inventory)

    def test_score_increases_when_visiting_new_locations(self):
        # Discovering a new location gives 5 points.
        self.game.move("Maiden Tower")

        self.assertEqual(self.game.player.score, 5)
        self.assertIn("Maiden Tower", self.game.player.visited_places)

    def test_hints_decrease_when_used(self):
        # Each hint should reduce the number of hints left by one.
        self.game.give_hint()

        self.assertEqual(self.game.player.hints_left, 2)

    def test_game_detects_win_when_treasure_is_in_inventory(self):
        # check_win should end the game if treasure has already been found.
        self.game.player.inventory.append("treasure")

        with patch.object(self.game, "show_summary"):
            # Avoid writing to scores.txt during this unit test.
            with patch.object(self.game, "save_score"):
                self.game.check_win()

        self.assertTrue(self.game.game_over)
        self.assertEqual(
            self.game.result_message,
            "You found the treasure in Shirvanshahs' Palace. You win!",
        )


# This allows the test file to be run directly.
if __name__ == "__main__":
    unittest.main()
