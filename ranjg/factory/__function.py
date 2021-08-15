import random
from typing import Optional, Union, List

from . import Factory, NoneFactory, IntFactory, BoolFactory, StrFactory, DictFactory, ListFactory, NumFactory


def _raffle_type(schema_type: Union[str, List[str], None]) -> Optional[str]:
    """Returns a type string specified by the schema.

    Args:
        schema_type: The type(s) specified by the schema.

    Returns:
        A type string. If argument ``schema_type`` is None, it returns None.
    """
    if schema_type is None or type(schema_type) == str:
        return schema_type
    elif len(schema_type) <= 0:
        raise ValueError("type must not be an empty list.")
    else:
        return random.choice(schema_type)


def create_factory(schema: Optional[dict], *, schema_is_validated: bool = False) -> Factory:
    """Returns a ranjg.factory.Factory instance according to the schema.

    Args:
        schema (dict, optional):
            JSON schema object. See also :doc:`ranjg-json-schema`.
        schema_is_validated (bool, optional):
            Whether the schema is already validated or not.
            (In normal usage, this argument is not specified.)
    Returns:
        A factory to generate values according the schema.
    """
    if schema is None:
        schema = {}

    gen_type = _raffle_type(schema.get("type"))

    if gen_type is None:
        # TODO: NoneFactory 固定でよいか要検討
        return NoneFactory(schema, schema_is_validated=schema_is_validated)
    elif gen_type == "null":
        return NoneFactory(schema, schema_is_validated=schema_is_validated)
    elif gen_type == "integer":
        return IntFactory(schema, schema_is_validated=schema_is_validated)
    elif gen_type == "number":
        return NumFactory(schema, schema_is_validated=schema_is_validated)
    elif gen_type == "boolean":
        return BoolFactory(schema, schema_is_validated=schema_is_validated)
    elif gen_type == "string":
        return StrFactory(schema, schema_is_validated=schema_is_validated)
    elif gen_type == "object":
        return DictFactory(schema, schema_is_validated=schema_is_validated)
    elif gen_type == "array":
        return ListFactory(schema, schema_is_validated=schema_is_validated)
    else:
        raise ValueError(f"Unsupported type: {gen_type}")
