import sys
import random

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

    schema = __normalize_schema(schema)
    options = __normalize_options(options)

    # 生成する数値の最小値
    minimum = max(schema["minimum"], schema["exclusiveMinimum"])
    maximum = min(schema["maximum"], schema["exclusiveMaximum"])

    if minimum > maximum:
        raise SchemaConflictError("Minimum value must be lower than or equal to the maximum value.")

    if maximum == schema["exclusiveMinimum"]:
        raise SchemaConflictError("ExclusiveMinimum value must be lower than the maximum value.")

    if minimum == schema["exclusiveMaximum"]:
        raise SchemaConflictError("ExclusiveMaximum value must be greater than the minimum value.")

    # 境界値を許容しない Schema であっても、境界値を含む乱数生成を行うため、
    # Schema に合致する値を引くまで生成を繰り返す。
    for i in range(options["regenerate_limit"]):
        generated = random.uniform(minimum, maximum)

        if generated == float("inf") or generated == float("-inf") or generated == float("NaN"):
            raise GenerateError("Error by too large or too small maximum or minimum")

        if __validate(generated, schema):
            break
    else:
        raise GenerateError("No valid value generated on loop.")

    return generated


def __normalize_schema(schema: dict) -> dict:
    """Schema normalization.

    To make it easier to use for randomly generation, set items to ``schema`` object.

    Args:
        schema: JSON schema for randomly generation.

    Returns:
        New schema based on ``schema`` and the default values.
    """

    n_schema = __default_schema.copy()
    n_schema.update(schema)

    return n_schema


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
