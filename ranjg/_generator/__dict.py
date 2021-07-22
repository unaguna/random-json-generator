import random

import ranjg
from .__common import Generator
from ..util.listutil import diff
from ..util.nonesafe import dfor


# required 項目の値の生成に使用するスキーマのデフォルト値。
# properties に当該キーの指定がない場合に使用する。
_default_required_schema = {
    "type": "number",
    "minimum": 0,
    "maximum": 0,
}

__default_options = {
    "prob_not_required_properties": 0.5,
}


def _normalize_options(options: dict) -> dict:
    """Option normalization.

    To make it easier to use for randomly generation, set items to ``options`` object.

    Args:
        options: Options for randomly generation.

    Returns:
        New options based on ``options`` and the default values.
    """
    options = dfor(options, {})

    n_options = __default_options.copy()
    n_options.update(options)

    return n_options


class DictGenerator(Generator[dict]):
    def gen(self, schema: dict, *, schema_is_validated: bool = False) -> dict:
        generated = dict()

        options = _normalize_options({})

        # すでに生成or棄却が済んだキー
        # それぞれのキーは生成された場合は True, 棄却された場合は False を値に持つ。
        generated_keys = dict()

        required: list = schema.get("required", [])
        properties: dict = schema.get("properties", {})
        not_required = diff(properties.keys(), required)

        # 必須項目を生成する
        for required_key in required:
            # すでに生成済みの項目は生成しない。ただし、棄却済みであるものは生成する。
            if generated_keys.get(required_key) is True:
                continue

            generated[required_key] = ranjg.gen(properties.get(required_key, _default_required_schema))
            generated_keys[required_key] = True

        # 必須でない項目を生成する
        for prop_key in not_required:
            # すでに生成or棄却済みの項目は生成しない。
            if generated_keys.get(prop_key) is not None:
                continue

            # 一定確率 (options に指定) で生成しない。
            if random.random() >= options["prob_not_required_properties"]:
                generated_keys[prop_key] = False
                continue

            generated[prop_key] = ranjg.gen(properties[prop_key])
            generated_keys[prop_key] = True

        return generated
