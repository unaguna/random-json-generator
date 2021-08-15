from typing import Optional

from .__common import Factory
from .._context import Context
from ..options import Options


class NoneFactory(Factory[None]):

    def __init__(self, schema: Optional[dict], *, schema_is_validated: bool = False):
        super(NoneFactory, self).__init__(schema, schema_is_validated=schema_is_validated)

    def gen_without_schema_check(self,
                                 *,
                                 options: Optional[Options] = None,
                                 context: Optional[Context] = None) -> None:
        return None
