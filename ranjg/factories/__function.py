from typing import Optional

from .__bool import BoolFactory
from .__common import Factory
from .__dict import DictFactory
from .__float import NumFactory
from .__int import IntFactory
from .__list import ListFactory
from .__none import NoneFactory
from .__str import StrFactory
from .._context import SchemaContext


def _create_factory_by_type(gen_type: str, *,
                            schema: dict,
                            context: Optional[SchemaContext] = None,
                            schema_is_validated: bool = False) -> Factory:
    """Returns a ranjg.factories.Factory instance according to the gen_type.

    Args:
        gen_type (str):
            It creates a factory that generates values of the specified type.
        schema (dict, optional):
            JSON schema object.
        context (SchemaContext, optional):
            The context of factory construction.
            (In normal usage, this argument is not specified.)
        schema_is_validated (bool, optional):
            Whether the schema is already validated or not.
            (In normal usage, this argument is not specified.)
    Returns:
        A factory to generate values according the gen_type.
    """
    if gen_type is None:
        # TODO: NoneFactory 固定でよいか要検討
        return NoneFactory(schema, schema_is_validated=schema_is_validated, context=context)
    elif gen_type == "null":
        return NoneFactory(schema, schema_is_validated=schema_is_validated, context=context)
    elif gen_type == "integer":
        return IntFactory(schema, schema_is_validated=schema_is_validated, context=context)
    elif gen_type == "number":
        return NumFactory(schema, schema_is_validated=schema_is_validated, context=context)
    elif gen_type == "boolean":
        return BoolFactory(schema, schema_is_validated=schema_is_validated, context=context)
    elif gen_type == "string":
        return StrFactory(schema, schema_is_validated=schema_is_validated, context=context)
    elif gen_type == "object":
        return DictFactory(schema, schema_is_validated=schema_is_validated, context=context)
    elif gen_type == "array":
        return ListFactory(schema, schema_is_validated=schema_is_validated, context=context)
    else:
        raise ValueError(f"Unsupported type: {gen_type}")
