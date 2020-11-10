import math
import random
from typing import Union, Tuple

from .error import SchemaConflictError


def genint(schema: dict) -> int:
    """Generate a random integer according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.

    Returns:
        Generated integer value.
    """

    minimum, maximum = _get_inclusive_integer_range(schema)

    return random.randint(minimum, maximum)


def _get_inclusive_integer_range(schema: dict) -> Tuple[int, int]:
    """Schema normalization.

    To make it easier to use for randomly generation, set items to ``schema`` object.

    Args:
        schema: JSON schema for randomly generation.

    Returns:
        Inclusive minimum and maximum.
    """

    # 生成する数値の最小値
    inclusive_minimum = schema.get("minimum", None)
    exclusive_minimum = schema.get("exclusiveMinimum", None)
    if exclusive_minimum is True:
        exclusive_minimum = inclusive_minimum
        inclusive_minimum = None
    elif exclusive_minimum is False:
        exclusive_minimum = None
    minimum = None
    if inclusive_minimum is not None and exclusive_minimum is not None:
        minimum = max(__to_int_minimum(inclusive_minimum, False), __to_int_minimum(exclusive_minimum, True))
    elif exclusive_minimum is not None:
        minimum = __to_int_minimum(exclusive_minimum, True)
    elif inclusive_minimum is not None:
        minimum = __to_int_minimum(inclusive_minimum, False)

    # 生成する数値の最大値
    inclusive_maximum = schema.get("maximum", None)
    exclusive_maximum = schema.get("exclusiveMaximum", None)
    if exclusive_maximum is True:
        exclusive_maximum = inclusive_maximum
        inclusive_maximum = None
    elif exclusive_maximum is False:
        exclusive_maximum = None
    maximum = None
    if inclusive_maximum is not None and exclusive_maximum is not None:
        maximum = min(__to_int_maximum(inclusive_maximum, False), __to_int_maximum(exclusive_maximum, True))
    elif exclusive_maximum is not None:
        maximum = __to_int_maximum(exclusive_maximum, True)
    elif inclusive_maximum is not None:
        maximum = __to_int_maximum(inclusive_maximum, False)

    if minimum is None and maximum is None:
        minimum = 0
        maximum = 100
    elif minimum is None:
        minimum = maximum - 5
    elif maximum is None:
        maximum = minimum + 5

    if minimum > maximum:
        raise SchemaConflictError("There are no integers in the range specified by the schema.")

    return minimum, maximum


def __to_int_minimum(minimum: Union[float, int], exclusive: bool) -> int:
    """Converts the minimum value by float type to int type.

    As long as the return value is used as the minimum of integer value, it works the same way as if the argument is
    used.

    Args:
        minimum: The minimum value
        exclusive: Whether to exclude the endpoints

    Returns:
        The minimum value by integer type
    """
    if isinstance(minimum, int) or minimum.is_integer():
        padding = 1 if exclusive else 0
        return int(minimum) + padding
    else:
        return int(math.ceil(minimum))


def __to_int_maximum(maximum: Union[float, int], exclusive: bool) -> int:
    """Converts the maximum value by float type to int type.

    As long as the return value is used as the maximum of integer value, it works the same way as if the argument is
    used.

    Args:
        maximum: The maximum value
        exclusive: Whether to exclude the endpoints

    Returns:
        The maximum value by integer type
    """
    if isinstance(maximum, int) or maximum.is_integer():
        padding = 1 if exclusive else 0
        return int(maximum) - padding
    else:
        return int(math.floor(maximum))
