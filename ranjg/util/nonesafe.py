"""Provide null-safety functions.
"""


def dfor(value, default):
    """Function instead of null coalescing operator.

    Args:
        value: A base value.
        default: Alternative value.

    Returns:
        ``value`` if it is not ``None``, otherwise ``default``.
    """
    return value if value is not None else default
