import os
import sys
import tempfile
import unittest


# Add the project folder to Python's import path so tests can import question_manager.py.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from question_manager import QuestionManager


class TestQuestionManager(unittest.TestCase):
    """Tests for loading and creating quiz questions."""

    def test_loads_questions_from_file(self):
        # TemporaryDirectory creates a safe test folder that is deleted afterward.
        with tempfile.TemporaryDirectory() as folder:
            questions_file = os.path.join(folder, "questions.txt")

            # Write two test questions using the same question|answer format as the game.
            with open(questions_file, "w", encoding="utf-8") as file:
                file.write("What is 2 + 2?|4\n")
                file.write("What color is the sky on a clear day?|blue\n")

            manager = QuestionManager(questions_file)

            # The manager should load both questions from the file.
            self.assertEqual(len(manager.questions), 2)
            self.assertIn(("What is 2 + 2?", "4"), manager.questions)
            self.assertIn(("What color is the sky on a clear day?", "blue"), manager.questions)

    def test_creates_default_questions_if_file_is_missing(self):
        # If no questions file exists, QuestionManager should create one.
        with tempfile.TemporaryDirectory() as folder:
            questions_file = os.path.join(folder, "questions.txt")

            manager = QuestionManager(questions_file)

            # The new file should exist and contain the built-in default questions.
            self.assertTrue(os.path.exists(questions_file))
            self.assertGreater(len(manager.questions), 0)
            self.assertIn(
                ("What protects a city from enemy attacks?", "walls"),
                manager.questions,
            )


# This allows the test file to be run directly.
if __name__ == "__main__":
    unittest.main()
