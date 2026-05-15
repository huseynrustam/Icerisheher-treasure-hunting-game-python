import os
import sys
import unittest


# Add the project folder to Python's import path so tests can import player.py.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from player import Player


class TestPlayer(unittest.TestCase):
    """Tests for the Player class."""

    def test_player_starts_with_correct_default_values(self):
        # Create a player at the same starting place used by the game.
        player = Player("Fortress Walls")

        # A new player should have no items, no points, and three hints.
        self.assertEqual(player.current_location, "Fortress Walls")
        self.assertEqual(player.inventory, [])
        self.assertEqual(player.score, 0)
        self.assertEqual(player.visited_places, {"Fortress Walls"})
        self.assertEqual(player.hints_left, 3)


# This allows the test file to be run directly.
if __name__ == "__main__":
    unittest.main()
