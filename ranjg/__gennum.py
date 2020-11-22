import sys
import random
from collections import namedtuple

from ranjg.util.nonesafe import dfor
from .error import GenerateError, SchemaConflictError

__default_schema = {
    "minimum": -sys.float_info.max / 2,
    "exclusiveMinimum": float('-inf'),
    "maximum": sys.float_info.max / 2,
    "exclusiveMaximum": float('inf'),
}

__default_options = {
    # 生成のやり直し回数の上限値
    "regenerate_limit": 50,
}


def gennum(schema: dict, options: dict = None) -> float:
    """Generate a random number according to the JSON schema.

    This function ignores ``schema.type`` because it is basically designed to be called by ``ranjg.gen``.

    Args:
        schema: JSON schema object.
        options: Options for adjusting the generation parameters.

    Returns:
        Generated number.
    """

    options = __normalize_options(options)

    # 生成する数値の範囲
    number_range = NumberRange.from_schema(schema)
    _check_consistency(number_range)
    number_range = _apply_default(number_range)

    # 境界値を許容しない Schema であっても、境界値を含む乱数生成を行うため、
    # Schema に合致する値を引くまで生成を繰り返す。
    for i in range(options["regenerate_limit"]):
        generated = random.uniform(number_range.minimum, number_range.maximum)

        if generated == float("inf") or generated == float("-inf") or generated == float("NaN"):
            raise GenerateError("Error by too large or too small maximum or minimum")

        if generated in number_range:
            break
    else:
        raise GenerateError("No valid value generated on loop.")

    return generated


def __normalize_options(options: dict) -> dict:
    """Option normalization.

    To make it easier to use for randomly generation, set items to ``options`` object.

    Args:
        options: Options for randomly generation.

    Returns:
        New options based on ``options`` and the default values.
    """
    options = dfor(options, {})

    n_options = __default_options.copy()
    n_options.update(options)

    return n_options


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


class NumberRange(namedtuple("NumberRange", "minimum maximum exclusive_minimum exclusive_maximum")):

    def __contains__(self, item):
        if item < self.minimum:
            return False
        elif item > self.maximum:
            return False
        elif self.exclusive_minimum and item <= self.minimum:
            return False
        elif self.exclusive_maximum and item >= self.maximum:
            return False
        else:
            return True

    @classmethod
    def from_schema(cls, schema: dict = None):
        """Initialize NumberRange

        Args:
            schema: Schema object.
        """
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        exclusive_minimum = schema.get("exclusiveMinimum")
        exclusive_maximum = schema.get("exclusiveMaximum")

        if exclusive_minimum is None:
            # exclusive_minimum の指定が無いなら、フラグは立たない。
            exclusive_minimum = False
        elif exclusive_minimum is True:
            # exclusive_minimum が True なら、フラグが立つ。ただし minimum の指定が無い場合はフラグを立てない決まり。
            exclusive_minimum = minimum is not None
        elif exclusive_minimum is False:
            # exclusive_minimum が False なら、フラグが立たない。
            pass
        else:
            # exclusive_minimum が数値なら、minimum 以上なら使用される。
            if minimum is None or minimum <= exclusive_minimum:
                minimum = exclusive_minimum
                exclusive_minimum = True
            else:
                exclusive_minimum = False

        maximum = maximum
        if exclusive_maximum is None:
            # exclusive_maximum の指定が無いなら、フラグは立たない。
            exclusive_maximum = False
        elif exclusive_maximum is True:
            # exclusive_maximum が True なら、フラグが立つ。ただし maximum の指定が無い場合はフラグを立てない決まり。
            exclusive_maximum = maximum is not None
        elif exclusive_maximum is False:
            # exclusive_maximum が False なら、フラグが立たない。
            pass
        else:
            # exclusive_maximum が数値なら、maximum 以下なら使用される。
            if maximum is None or maximum >= exclusive_maximum:
                maximum = exclusive_maximum
                exclusive_maximum = True
            else:
                exclusive_maximum = False

        return NumberRange(minimum=minimum,
                           maximum=maximum,
                           exclusive_minimum=exclusive_minimum,
                           exclusive_maximum=exclusive_maximum)


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
            return number_range._replace(minimum=_little_less(number_range.maximum), exclusive_minimum=False)
    else:
        if number_range.maximum is None:
            return number_range._replace(maximum=_little_greater(number_range.minimum), exclusive_maximum=True)
        else:
            return number_range


def _check_consistency(number_range: NumberRange):
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
        raise SchemaConflictError("Minimum value must be lower than or equal to the maximum value.")
    if number_range.minimum == number_range.maximum:
        if number_range.exclusive_minimum:
            raise SchemaConflictError("ExclusiveMinimum value must be lower than the maximum value.")
        elif number_range.exclusive_maximum:
            raise SchemaConflictError("ExclusiveMaximum value must be greater than the minimum value.")


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
