from typing import Optional

from . import Factory, NoneFactory, IntFactory, BoolFactory, StrFactory, DictFactory, ListFactory, NumFactory


def create_factory(gen_type: Optional[str]) -> Factory:
    """Returns a ranjg.factory.Factory instance according to gen_type.

    Args:
        gen_type:
            generator's type
    Returns:
        random-value factory
    """

    if gen_type is None:
        # TODO: None 固定でよいか要検討
        return NoneFactory()
    elif gen_type == "null":
        return NoneFactory()
    elif gen_type == "integer":
        return IntFactory()
    elif gen_type == "number":
        return NumFactory()
    elif gen_type == "boolean":
        return BoolFactory()
    elif gen_type == "string":
        return StrFactory()
    elif gen_type == "object":
        return DictFactory()
    elif gen_type == "array":
        return ListFactory()
    else:
        raise ValueError(f"Unsupported type: {gen_type}")
