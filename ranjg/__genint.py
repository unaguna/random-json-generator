import random
from .error import SchemaConflictError


def genint(schema: dict) -> int:
    """Generate a random integer according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.

    Returns:
        Generated integer value.
    """

    schema = __normalize_schema(schema)

    minimum: int = schema["minimum"]
    maximum: int = schema["maximum"]

    if minimum > maximum:
        raise SchemaConflictError("Minimum value must be lower than or equal to the maximum value.")

    return random.randint(minimum, maximum)


def __normalize_schema(schema: dict) -> dict:
    """Schema normalization.

    To make it easier to use for randomly generation, set items to ``schema`` object.

    Args:
        schema: JSON schema for randomly generation.

    Returns:
        New schema based on ``schema`` and the default values.
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
        minimum = max(inclusive_minimum, exclusive_minimum + 1)
    elif exclusive_minimum is not None:
        minimum = exclusive_minimum + 1
    elif inclusive_minimum is not None:
        minimum = inclusive_minimum

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
        maximum = min(inclusive_maximum, exclusive_maximum - 1)
    elif exclusive_maximum is not None:
        maximum = exclusive_maximum - 1
    elif inclusive_maximum is not None:
        maximum = inclusive_maximum

    if minimum is None and maximum is None:
        minimum = 0
        maximum = 100
    elif minimum is None:
        minimum = maximum - 5
    elif maximum is None:
        maximum = minimum + 5

    return {
        "minimum": minimum,
        "maximum": maximum,
    }
