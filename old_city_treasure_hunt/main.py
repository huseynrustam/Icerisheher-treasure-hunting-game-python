from game import TreasureGame


def main():
    """Create the game object and start the command loop."""
    game = TreasureGame()
    game.play()


# This makes sure the game only starts when this file is run directly.
# If another file imports main.py, the game will not start by accident.
if __name__ == "__main__":
    main()
