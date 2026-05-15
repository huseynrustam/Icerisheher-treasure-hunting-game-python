# Old City Treasure Hunt

A text-based treasure hunting game set inside Baku's historic Old City (Icherisheher).

Players move through landmarks, answer quiz questions to search locations, find an old key, and uncover a hidden treasure.

## Features

- Interactive command-line gameplay
- Location-based treasure hunt with map navigation
- Quiz questions for searching and clue discovery
- Hints system with limited uses
- Score saving to `scores.txt`
- Default questions automatically created if `questions.txt` is missing

## Requirements

- Python 3.7+

## Get the Source

The game is available on GitHub:

https://github.com/huseynrustam/Icerisheher-treasure-hunting-game-python

### Clone and Use

```bash
git clone https://github.com/huseynrustam/Icerisheher-treasure-hunting-game-python.git
cd Icerisheher-treasure-hunting-game-python\old_city_treasure_hunt
python main.py
```

If you already have the repository locally, pull the latest changes with:

```bash
git pull
```

## How to Run

1. Open a terminal in the `old_city_treasure_hunt` directory.
2. Run:

```bash
python main.py
```

## Commands

- `help` - Show available commands
- `map` - Display the text map of Icherisheher
- `move <place>` - Move to a connected location
- `search` - Answer a question and search the current location
- `hint` - Use a hint to get guidance
- `status` - Show your current score, location, and inventory
- `restart` - Restart the game from the beginning
- `exit` - Exit the game

## Game Files

- `main.py` - Entry point for running the game
- `game.py` - Main game logic and command loop
- `location.py` - Location model for map nodes
- `player.py` - Player state, inventory, score, and hints
- `question_manager.py` - Loads and validates quiz questions
- `file_manager.py` - Saves game results to `scores.txt`
- `questions.txt` - Quiz questions used for searching locations
- `scores.txt` - Saved score history and results

## Tests

The `tests/` directory contains unit tests for core game components.

Run tests with your preferred Python test runner, for example:

```bash
python -m unittest discover -s tests
```

## Notes

- The game saves final results automatically after each completed or exited session.
- If `questions.txt` is missing, the game creates a default set of questions.
