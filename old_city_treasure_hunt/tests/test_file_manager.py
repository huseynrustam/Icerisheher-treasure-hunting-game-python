import os
import sys
import tempfile
import unittest
from unittest.mock import patch


# Add the project folder to Python's import path so tests can import file_manager.py.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from file_manager import FileManager


class TestFileManager(unittest.TestCase):
    """Tests for saving game results to scores.txt."""

    def test_save_score_writes_date_and_best_score(self):
        # Use a temporary folder so the real scores.txt file is not changed.
        with tempfile.TemporaryDirectory() as folder:
            scores_file = os.path.join(folder, "scores.txt")
            manager = FileManager(scores_file)

            # Mock the date so the saved text is predictable in the test.
            with patch("file_manager.datetime") as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "2026-05-16 14:30:00"

                # Hide print output from save_score.
                with patch("builtins.print"):
                    manager.save_score(
                        25,
                        4,
                        2,
                        {"Fortress Walls", "Maiden Tower"},
                        ["old key"],
                        "Game saved for test.",
                    )

            with open(scores_file, "r", encoding="utf-8") as file:
                saved_text = file.read()

            # The saved block should include the date, current score, and best score.
            self.assertIn("Date saved: 2026-05-16 14:30:00", saved_text)
            self.assertIn("Final score: 25", saved_text)
            self.assertIn("Best score: 25", saved_text)

    def test_best_score_keeps_previous_higher_score(self):
        # If an old score is higher than the current score, it should stay best.
        with tempfile.TemporaryDirectory() as folder:
            scores_file = os.path.join(folder, "scores.txt")

            # Add an existing high score before saving the new result.
            with open(scores_file, "w", encoding="utf-8") as file:
                file.write("Final score: 80\n")

            manager = FileManager(scores_file)

            with patch("builtins.print"):
                manager.save_score(30, 5, 1, {"Fortress Walls"}, [], "Lower score.")

            with open(scores_file, "r", encoding="utf-8") as file:
                saved_text = file.read()

            self.assertIn("Best score: 80", saved_text)


# This allows the test file to be run directly.
if __name__ == "__main__":
    unittest.main()
