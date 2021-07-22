import random

from .__common import Generator


class BoolGenerator(Generator[bool]):
    def gen(self, schema: dict, *, schema_is_validated: bool = False) -> bool:
        return random.random() < 0.5
