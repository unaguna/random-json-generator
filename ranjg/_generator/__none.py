from typing import Optional

from .__common import Generator
from .._context import Context


class NoneGenerator(Generator[None]):
    def gen_without_schema_check(self,
                                 schema: dict,
                                 *,
                                 context: Optional[Context] = None) -> None:
        return None
