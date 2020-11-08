import random


def genbool() -> bool:
    """Generate a random boolean value according to the JSON schema.

    Returns:
        Generated boolean value.
    """

    return random.random() < 0.5
