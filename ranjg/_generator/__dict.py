import random
from typing import Optional

import ranjg
from .__common import Generator
from .._context import Context
from .._options import Options
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
    def gen_without_schema_check(self,
                                 schema: Optional[dict],
                                 *,
                                 options: Optional[Options] = None,
                                 context: Optional[Context] = None) -> dict:
        if schema is None:
            schema = None
        if context is None:
            context = Context.root(schema)

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

            next_schema = properties.get(required_key, _default_required_schema)
            generated[required_key] = ranjg.gen(next_schema,
                                                schema_is_validated=True,
                                                context=context.resolve(required_key, next_schema))
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

            next_schema = properties[prop_key]
            generated[prop_key] = ranjg.gen(next_schema,
                                            schema_is_validated=True,
                                            context=context.resolve(prop_key, next_schema))
            generated_keys[prop_key] = True

        return generated
