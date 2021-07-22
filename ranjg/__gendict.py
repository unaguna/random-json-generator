from ._generator import DictGenerator


def gendict(schema: dict) -> dict:
    """Generate a random dict value according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.

    Returns:
        Generated dict value.
    """
    return DictGenerator().gen(schema)
