from datetime import datetime


class FileManager:
    """Handles saving final game results."""

    def __init__(self, scores_file="scores.txt"):
        # Store the score file path so all saved results go to one place.
        self.scores_file = scores_file

    def get_best_score(self, current_score):
        """Find the highest saved score, including the current game's score."""
        best_score = current_score

        try:
            with open(self.scores_file, "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("Final score:"):
                        try:
                            # Read old score lines in the format: Final score: 25
                            saved_score = int(line.split(":", 1)[1].strip())
                            best_score = max(best_score, saved_score)
                        except ValueError:
                            # Ignore damaged score lines instead of stopping the game.
                            continue
        except FileNotFoundError:
            # No score file exists yet, so the current score is the best score.
            pass
        except OSError as error:
            print(f"\nCould not read best score: {error}")

        return best_score

    def save_score(self, score, moves, hints_left, visited_places, inventory, result_message):
        """Append the final game result to the score file."""
        best_score = self.get_best_score(score)
        saved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(self.scores_file, "a", encoding="utf-8") as file:
                # Each saved game is written as a readable block of text.
                file.write("Old City Treasure Hunt Result\n")
                file.write(f"Date saved: {saved_at}\n")
                file.write(f"Final score: {score}\n")
                file.write(f"Best score: {best_score}\n")
                file.write(f"Moves: {moves}\n")
                file.write(f"Hints left: {hints_left}\n")
                file.write(f"Visited places: {', '.join(sorted(visited_places))}\n")
                file.write(f"Inventory: {', '.join(inventory) if inventory else 'empty'}\n")
                file.write(f"Result: {result_message}\n")
                file.write("-" * 40 + "\n")
            print(f"\nFinal result saved to {self.scores_file}.")
        except OSError as error:
            print(f"\nCould not save score: {error}")
