from typing import Optional

from . import Generator, NoneGenerator, IntGenerator, BoolGenerator, StrGenerator, DictGenerator, \
    ListGenerator, NumGenerator


def get_generator(gen_type: Optional[str]) -> Generator:
    """Returns a ranjg.factory.Generator instance according to gen_type.

    Args:
        gen_type:
            generator's type
    Returns:
        generator
    """

    if gen_type is None:
        # TODO: None 固定でよいか要検討
        return NoneGenerator()
    elif gen_type == "null":
        return NoneGenerator()
    elif gen_type == "integer":
        return IntGenerator()
    elif gen_type == "number":
        return NumGenerator()
    elif gen_type == "boolean":
        return BoolGenerator()
    elif gen_type == "string":
        return StrGenerator()
    elif gen_type == "object":
        return DictGenerator()
    elif gen_type == "array":
        return ListGenerator()
    else:
        raise ValueError(f"Unsupported type: {gen_type}")
