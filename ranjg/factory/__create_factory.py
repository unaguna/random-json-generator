from typing import Optional, Union, Iterable

from . import MultiFactory
from .__common import Factory
from .__function import _create_factory_by_type


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
        gen_type = schema.get("type")

    if isinstance(gen_type, Iterable) and not isinstance(gen_type, str):
        return MultiFactory(schema, schema_is_validated=schema_is_validated)
    else:
        return _create_factory_by_type(gen_type, schema=schema, schema_is_validated=schema_is_validated)
