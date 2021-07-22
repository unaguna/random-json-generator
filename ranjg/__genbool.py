from ._generator import BoolGenerator


def genbool(schema: dict = None) -> bool:
    """Generate a random boolean value according to the JSON schema.

    Returns:
        Generated boolean value.
    """
    if schema is None:
        schema = {}

    return BoolGenerator().gen(schema)
