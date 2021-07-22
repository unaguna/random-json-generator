import random

from .__common import Generator


class BoolGenerator(Generator[bool]):
    def gen_without_schema_check(self, schema: dict) -> bool:
        return random.random() < 0.5
