import random
from typing import Optional

from .__common import Factory
from .._context import GenerationContext
from ..options import Options


class BoolFactory(Factory[bool]):

    def __init__(self, schema: Optional[dict], *, schema_is_validated: bool = False):
        super(BoolFactory, self).__init__(schema, schema_is_validated=schema_is_validated)

    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[GenerationContext] = None) -> bool:
        if options is None:
            options = Options.default()

        return random.random() < options.default_prob_of_true_given_bool
