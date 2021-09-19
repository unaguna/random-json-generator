import random
import sys
from typing import Optional

from .__common import Factory
from ..__number_range import NumberRange
from .._context import GenerationContext, SchemaContext
from ..options import Options
from ..error import SchemaConflictError, GenerateError

__default_schema = {
    "minimum": -sys.float_info.max / 2,
    "exclusiveMinimum": float('-inf'),
    "maximum": sys.float_info.max / 2,
    "exclusiveMaximum": float('inf'),
}


def __validate(value: float, schema: dict) -> bool:
    """Check if the value matches the schema.

    This function is only used to filter out illegal values in the float generation process, so it doesn't check every
    item in the schema. If you want to validate a value, it is recommended to use ``jsonschema`` module.

    Args:
        value: Value to be checked.
        schema: Normalized JsonSchema.

    Returns:
        True if it conforms to the scheme, otherwise False.
    """

    if value is None:
        return False

    return schema["exclusiveMinimum"] < value < schema["exclusiveMaximum"] and \
           schema["minimum"] <= value <= schema["maximum"]


def _apply_default(number_range: NumberRange) -> NumberRange:
    """Apply default range.

    Args:
        number_range: A range.

    Returns:
        A range with minimum and maximum. They are not None.
    """
    if number_range.minimum is None:
        if number_range.maximum is None:
            return NumberRange(minimum=0.0,
                               maximum=1.0,
                               exclusive_minimum=False,
                               exclusive_maximum=True)
        else:
            return number_range.replace(minimum=_little_less(number_range.maximum), exclusive_minimum=False)
    else:
        if number_range.maximum is None:
            return number_range.replace(maximum=_little_greater(number_range.minimum), exclusive_maximum=True)
        else:
            return number_range


def _check_consistency(number_range: NumberRange, context: GenerationContext):
    """Check the instance in consistency

    Attributes:
        number_range:
            Subject of the examination.

    Raises:
        SchemaConflictError:
            If number_range has consistency.
    """
    # 矛盾が発生するのは、最大と最小の両方が定義されている場合のみ
    if number_range.minimum is None or number_range.maximum is None:
        return

    if number_range.minimum > number_range.maximum:
        if number_range.exclusive_minimum is False and number_range.exclusive_maximum is False:
            raise SchemaConflictError("Minimum value must be lower than or equal to the maximum value.", context)
        if number_range.exclusive_minimum is True and number_range.exclusive_maximum is False:
            raise SchemaConflictError("ExclusiveMinimum value must be lower than the maximum value.", context)
        if number_range.exclusive_minimum is False and number_range.exclusive_maximum is True:
            raise SchemaConflictError("Minimum value must be lower than the exclusiveMaximum value.", context)
        if number_range.exclusive_minimum is True and number_range.exclusive_maximum is True:
            raise SchemaConflictError("ExclusiveMinimum value must be lower than the exclusiveMaximum value.", context)
    elif number_range.minimum == number_range.maximum:
        if number_range.exclusive_minimum is True and number_range.exclusive_maximum is False:
            raise SchemaConflictError("ExclusiveMinimum value must be lower than the maximum value.", context)
        if number_range.exclusive_minimum is False and number_range.exclusive_maximum is True:
            raise SchemaConflictError("Minimum value must be lower than the exclusiveMaximum value.", context)
        if number_range.exclusive_minimum is True and number_range.exclusive_maximum is True:
            raise SchemaConflictError("ExclusiveMinimum value must be lower than the exclusiveMaximum value.", context)


def _little_greater(number: float) -> float:
    """Return a number greater than the argument.

    Args:
        number: A number.

    Returns:
        A number greater than the argument.
    """
    if number > 0:
        return number * sys.float_info.radix
    elif number < 0:
        return number / sys.float_info.radix
    else:
        return 1.0


def _little_less(number: float) -> float:
    """Return a number less than the argument.

    Args:
        number: A number.

    Returns:
        A number less than the argument.
    """
    if number > 0:
        return number / sys.float_info.radix
    elif number < 0:
        return number * sys.float_info.radix
    else:
        return -1.0


class NumFactory(Factory[float]):
    _schema: dict
    _number_range: NumberRange

    def __init__(self, schema: Optional[dict], *,
                 schema_is_validated: bool = False, context: Optional[SchemaContext] = None):
        super(NumFactory, self).__init__(schema, schema_is_validated=schema_is_validated, context=context)

        # 生成する数値の範囲
        self._number_range = NumberRange.from_schema(self._schema)

    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[GenerationContext] = None) -> float:
        if options is None:
            options = Options.default()
        if context is None:
            context = GenerationContext.root(self._schema)

        # 生成する数値の範囲
        _check_consistency(self._number_range, context)
        number_range = _apply_default(self._number_range)

        # 境界値を許容しない Schema であっても、境界値を含む乱数生成を行うため、
        # Schema に合致する値を引くまで生成を繰り返す。
        for i in range(options.regeneration_attempt_limit):
            generated = random.uniform(number_range.minimum, number_range.maximum)

            if generated == float("inf") or generated == float("-inf") or generated == float("NaN"):
                raise GenerateError("Error by too large or too small maximum or minimum", context)

            if generated in number_range:
                break
        else:
            raise GenerateError("No valid value generated on loop.", context)

        return generated
