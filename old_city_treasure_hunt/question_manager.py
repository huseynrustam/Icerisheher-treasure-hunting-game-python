import os
import random


class QuestionManager:
    """Loads quiz questions and selects random questions."""

    def __init__(self, questions_file="questions.txt"):
        # Store the file path so the game can load questions from a text file.
        self.questions_file = questions_file

        # Questions are stored as tuples: (question_text, correct_answer).
        self.questions = []

        # Load questions immediately so the game is ready to ask them.
        self.load_questions()

    def load_questions(self):
        """Read questions from the text file and validate their format."""
        try:
            with open(self.questions_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            # If the file is missing, create it from the default question list.
            print(f"{os.path.basename(self.questions_file)} was not found. Creating a default question file.")
            self.create_default_questions_file()
            try:
                with open(self.questions_file, "r", encoding="utf-8") as file:
                    lines = file.readlines()
            except OSError as error:
                print(f"File read error after creating questions file: {error}")
                self.questions = []
                return
        except OSError as error:
            print(f"File read error: {error}")
            self.questions = []
            return

        valid_questions = []
        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                # Each line must look like this: question text|answer text
                question, answer = line.split("|", 1)
                question = question.strip()
                answer = answer.strip()
                if not question or not answer:
                    raise ValueError
                valid_questions.append((question, answer))
            except ValueError:
                print(f"Invalid question format on line {line_number}. Expected: question|answer")

        if not valid_questions:
            # If every line was invalid, keep the game playable with defaults.
            print("No valid questions were found. Default questions will be used in memory.")
            valid_questions = self.default_questions()

        self.questions = valid_questions

    def create_default_questions_file(self):
        """Create a new questions file using the built-in default questions."""
        try:
            with open(self.questions_file, "w", encoding="utf-8") as file:
                for question, answer in self.default_questions():
                    file.write(f"{question}|{answer}\n")
        except OSError as error:
            print(f"Could not create questions file: {error}")

    def get_random_question(self):
        """Return one random question, or None if no questions are available."""
        if not self.questions:
            return None
        return random.choice(self.questions)

    def default_questions(self):
        """Return the built-in backup questions for the treasure hunt."""
        return [
            ("What do guards carry while protecting city gates?", "spears"),
            ("What lights the streets at night before electricity?", "torches"),
            ("What do merchants sell in busy market streets?", "spices"),
            ("What animal carries goods during long desert journeys?", "camel"),
            ("What do travelers look for after a long journey?", "shelter"),
            ("What protects a city from enemy attacks?", "walls"),
            ("What do rulers wear to show power?", "crowns"),
            ("What do sailors use to travel across the sea?", "ships"),
            ("What do blacksmiths make from hot iron?", "swords"),
            ("What do watchmen stand on to see enemies from far away?", "towers"),
            ("What do people use to open locked palace doors?", "keys"),
            ("What is usually hidden inside royal treasure chests?", "gold"),
            ("What do traders follow to travel between kingdoms?", "routes"),
            ("What do ancient messengers carry between rulers?", "letters"),
            ("What do people drink in crowded caravanserais after long travel?", "tea"),
            ("What is burned to keep rooms warm in winter?", "firewood"),
            ("What do builders use to construct strong fortresses?", "stone"),
            ("What do people ride through old city streets?", "horses"),
            ("What do travelers use to find direction on long journeys?", "compass"),
            ("What do kings protect inside their palaces?", "treasure"),
        ]
