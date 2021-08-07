from functools import lru_cache
from typing import NamedTuple, Union


class Options(NamedTuple):

    # The maximum number of generation when multiple attempts are required to obtain a result that satisfies the schema.
    # If it is None, regeneration is repeated until a result that matches the schema is obtained.
    # If it is too small, there is a high probability that the generation will fail and raise an GenerateError.
    regeneration_attempt_limit: int = 50

    # In bool generation, returns True with probability x, False with probability 1-x.
    default_prob_of_true_given_bool: Union[int, float] = 0.5

    # In string generation, it is used as the difference between minLength and maxLength, if necessary.
    # If only one of minLength and maxLength is specified, it is used to determine the other.
    default_length_range_of_genstr: int = 0

    # In string generation, it is used as the value of minLength when both minLength and maxLength are not specified.
    default_min_length_of_string: int = 1

    # In string generation, it is used as the value of maxLength when both minLength and maxLength are not specified.
    default_max_length_of_string: int = 10

    # In dict generation, every optional property in the schema is contained in the result dict with a x probability
    # independently
    default_prob_of_optional_properties: Union[int, float] = 0.5

    # In list generation, it is used to generate elements for which no schema is specified.
    # For example, when `item` is specified as tuple format, and minLength is greater than its length.
    default_schema_of_items: dict = {"type": "null"}

    @classmethod
    @lru_cache(maxsize=1)
    def default(cls):
        """Default options

        It is used when an user don't specify options.
        """
        return Options()
