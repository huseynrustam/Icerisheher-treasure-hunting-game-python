import os
import sys
import unittest


# Add the project folder to Python's import path so tests can import location.py.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from location import Location


class TestLocation(unittest.TestCase):
    """Tests for the Location class."""

    def test_location_stores_details_correctly(self):
        # Create a sample location with all important fields filled in.
        location = Location(
            "Shirvanshahs' Palace",
            "A royal building in the old city.",
            "Treasure belongs where rulers lived.",
            item="treasure",
        )

        # Add one connected place to check the neighbor list.
        location.add_neighbor("Juma Mosque")

        # Make sure the object stores exactly what was given to it.
        self.assertEqual(location.name, "Shirvanshahs' Palace")
        self.assertEqual(location.description, "A royal building in the old city.")
        self.assertEqual(location.neighbors, ["Juma Mosque"])
        self.assertEqual(location.clue, "Treasure belongs where rulers lived.")
        self.assertEqual(location.item, "treasure")


# This allows the test file to be run directly.
if __name__ == "__main__":
    unittest.main()
