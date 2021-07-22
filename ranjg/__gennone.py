from ._generator import NoneGenerator


def gennone(schema: dict = None) -> None:
    """Generate ``None``.

    Returns:
        Generated ``None``.
    """
    if schema is None:
        schema = {}

    return NoneGenerator().gen(schema)
