from typing import Optional

from .__common import Factory
from .._context import Context
from ..options import Options


class NoneFactory(Factory[None]):
    def gen_without_schema_check(self,
                                 schema: Optional[dict],
                                 *,
                                 options: Optional[Options] = None,
                                 context: Optional[Context] = None) -> None:
        return None
