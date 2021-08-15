from typing import Optional

from . import Factory, NoneFactory, IntFactory, BoolFactory, StrFactory, DictFactory, ListFactory, NumFactory


def create_factory(gen_type: Optional[str], schema: Optional[dict], *, schema_is_validated: bool = False) -> Factory:
    """Returns a ranjg.factory.Factory instance according to gen_type.

    Args:
        gen_type:
            generator's type
    Returns:
        random-value factory
    """

    if gen_type is None:
        # TODO: None 固定でよいか要検討
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
