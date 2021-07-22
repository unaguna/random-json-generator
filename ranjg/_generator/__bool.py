import random

from .__common import _Generator


class BoolGenerator(_Generator[bool]):
    def gen(self, schema: dict, *, schema_is_validated: bool = False) -> bool:
        return random.random() < 0.5
