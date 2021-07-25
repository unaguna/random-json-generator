import random
from typing import Optional

from .__common import Generator
from .._context import Context
from .._options import Options


class BoolGenerator(Generator[bool]):
    def gen_without_schema_check(self,
                                 schema: Optional[dict],
                                 *,
                                 options: Optional[Options] = None,
                                 context: Optional[Context] = None) -> bool:
        return random.random() < 0.5
