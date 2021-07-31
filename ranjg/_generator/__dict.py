import random
from typing import Optional

import ranjg
from .__common import Generator
from .._context import Context
from .._options import Options
from ..util.listutil import diff


# required 項目の値の生成に使用するスキーマのデフォルト値。
# properties に当該キーの指定がない場合に使用する。
_default_required_schema = {
    "type": "number",
    "minimum": 0,
    "maximum": 0,
}


class DictGenerator(Generator[dict]):
    def gen_without_schema_check(self,
                                 schema: Optional[dict],
                                 *,
                                 options: Optional[Options] = None,
                                 context: Optional[Context] = None) -> dict:
        if schema is None:
            schema = None
        if options is None:
            options = Options.default()
        if context is None:
            context = Context.root(schema)

        generated = dict()

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
            if random.random() >= options.default_prob_of_optional_properties:
                generated_keys[prop_key] = False
                continue

            next_schema = properties[prop_key]
            generated[prop_key] = ranjg.gen(next_schema,
                                            schema_is_validated=True,
                                            context=context.resolve(prop_key, next_schema))
            generated_keys[prop_key] = True

        return generated
