from .__common import _Generator


class NoneGenerator(_Generator[None]):
    def gen(self, schema: dict, *, schema_is_validated: bool = False) -> None:
        return None
