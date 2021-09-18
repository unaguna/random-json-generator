import math
import random
from typing import Optional, Union, Tuple

from .__common import Factory
from .._context import GenerationContext
from ..error import SchemaConflictError
from ..options import Options
from ..jsonschema.normalize import normalize_exclusive_minimum, normalize_exclusive_maximum


class IntFactory(Factory[int]):
    _schema: dict
    _schema_minimum: Optional[int]
    _schema_maximum: Optional[int]

    def __init__(self, schema: Optional[dict], *, schema_is_validated: bool = False):
        super(IntFactory, self).__init__(schema, schema_is_validated=schema_is_validated)

        self._schema = schema if schema is not None else {}

        # Convert float or exclusive value in schema to integer inclusive value.
        self._schema_minimum = _get_inclusive_integer_minimum(self._schema)
        self._schema_maximum = _get_inclusive_integer_maximum(self._schema)

    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[GenerationContext] = None) -> int:
        if context is None:
            context = GenerationContext.root(self._schema)

        if self._schema_minimum is not None and self._schema_maximum is not None and \
                self._schema_minimum > self._schema_maximum:
            raise SchemaConflictError("There are no integers in the range specified by the schema.", context)

        minimum, maximum = _apply_default(self._schema_minimum, self._schema_maximum)

        return random.randint(minimum, maximum)


def _get_inclusive_integer_minimum(schema: dict) -> Optional[int]:
    """Returns minimum as integer and not exclusive.

    To make it easier to use for randomly generation, convert float or exclusive minimum in schema to integer inclusive
    value.

    Args:
        schema: JSON schema for randomly generation.

    Returns:
        Inclusive minimum.
    """
    # exclusiveMinimum が真理値である場合、Draft7スタイルに変更
    inclusive_minimum, exclusive_minimum = normalize_exclusive_minimum(schema)

    minimum = None
    if inclusive_minimum is not None and exclusive_minimum is not None:
        minimum = max(__to_int_minimum(inclusive_minimum, False), __to_int_minimum(exclusive_minimum, True))
    elif exclusive_minimum is not None:
        minimum = __to_int_minimum(exclusive_minimum, True)
    elif inclusive_minimum is not None:
        minimum = __to_int_minimum(inclusive_minimum, False)

    return minimum


def _get_inclusive_integer_maximum(schema: dict) -> Optional[int]:
    """Returns maximum as integer and not exclusive.

    To make it easier to use for randomly generation, convert float or exclusive maximum in schema to integer inclusive
    value.

    Args:
        schema: JSON schema for randomly generation.

    Returns:
        Inclusive maximum.
    """
    # exclusiveMaximum が真理値である場合、Draft7スタイルに変更
    inclusive_maximum, exclusive_maximum = normalize_exclusive_maximum(schema)

    maximum = None
    if inclusive_maximum is not None and exclusive_maximum is not None:
        maximum = min(__to_int_maximum(inclusive_maximum, False), __to_int_maximum(exclusive_maximum, True))
    elif exclusive_maximum is not None:
        maximum = __to_int_maximum(exclusive_maximum, True)
    elif inclusive_maximum is not None:
        maximum = __to_int_maximum(inclusive_maximum, False)

    return maximum


def _apply_default(minimum: Optional[int], maximum: Optional[int]) -> Tuple[int, int]:
    """Apply default minimum and maximum.

    Args:
        minimum: None or minimum value of integer to generate
        maximum: None or maximum value of integer to generate

    Returns:
        A pair of minimum and maximum. They are not None.
    """
    if minimum is None and maximum is None:
        minimum = 0
        maximum = 100
    elif minimum is None:
        minimum = maximum - 5
    elif maximum is None:
        maximum = minimum + 5

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
    if exclusive:
        return math.floor(minimum) + 1
    else:
        return math.ceil(minimum)


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
    if exclusive:
        return math.ceil(maximum) - 1
    else:
        return math.floor(maximum)
