from typing import Optional

from .__common import Factory
from .._context import GenerationContext, SchemaContext
from ..options import Options


class NoneFactory(Factory[None]):

    def __init__(self, schema: Optional[dict], *,
                 schema_is_validated: bool = False, context: Optional[SchemaContext] = None):
        super(NoneFactory, self).__init__(schema, schema_is_validated=schema_is_validated, context=context)

    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[GenerationContext] = None) -> None:
        return None
