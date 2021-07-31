from typing import NamedTuple, Union


class Options(NamedTuple):

    # In dict generation, every optional property in the schema is contained in the result dict with a x probability
    # independently
    default_prob_of_optional_properties: Union[int, float] = 0.5
