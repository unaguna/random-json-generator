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


def create_factory(schema: Optional[dict], *,
                   schema_is_validated: bool = False,
                   gen_type: Union[str, None] = None) -> Factory:
    """Returns a ranjg.factory.Factory instance according to the schema.

    Args:
        schema (dict, optional):
            JSON schema object. See also :doc:`ranjg-json-schema`.
        schema_is_validated (bool, optional):
            Whether the schema is already validated or not.
            (In normal usage, this argument is not specified.)
        gen_type (str, optional):
            If specified, ignore ``schema.type`` and create a factory that generates values of the specified type.
            (In normal usage, this argument is not specified.)
    Returns:
        A factory to generate values according the schema.

    Examples:
        The following code is most simple usage.

        >>> from ranjg.factory import create_factory
        >>> schema_dict = { 'type': 'string' }
        >>> factory = create_factory(schema_dict)    # -> A factory according the schema
        >>> generated_1 = factory.gen()    # -> A value according the schema
        >>> generated_2 = factory.gen()    # -> A value according the schema (Almost certainly different than before.)
        >>> generated_3 = factory.gen()    # It can be generated as many times as you want.

        ``factory.gen`` can receive a keyword argument ``options``.
        See also :doc:`ranjg-options` to know about options.
    """
    if schema is None:
        schema = {}

    if gen_type is None:
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
