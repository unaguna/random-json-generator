from .__common import Generator


class NoneGenerator(Generator[None]):
    def gen(self, schema: dict, *, schema_is_validated: bool = False) -> None:
        return None
