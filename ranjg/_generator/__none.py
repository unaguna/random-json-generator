from .__common import Generator


class NoneGenerator(Generator[None]):
    def gen_without_schema_check(self, schema: dict) -> None:
        return None
