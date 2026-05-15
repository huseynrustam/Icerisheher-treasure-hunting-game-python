class Location:
    """Represents one place in the game map."""

    def __init__(self, name, description, clue, item=None):
        # The display name of the place, for example "Maiden Tower".
        self.name = name

        # The text shown when the player arrives at this location.
        self.description = description

        # Neighbor names are the places the player can move to from here.
        self.neighbors = []

        # The clue appears after the player answers a question correctly.
        self.clue = clue

        # Some locations hide an item, such as "old key" or "treasure".
        self.item = item

    def add_neighbor(self, location_name):
        """Add one connected place to this location."""
        self.neighbors.append(location_name)
