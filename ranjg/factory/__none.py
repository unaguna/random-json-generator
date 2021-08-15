from typing import Optional

from .__common import Generator
from .._context import Context
from ..options import Options


class NoneGenerator(Generator[None]):
    def gen_without_schema_check(self,
                                 schema: Optional[dict],
                                 *,
                                 options: Optional[Options] = None,
                                 context: Optional[Context] = None) -> None:
        return None
