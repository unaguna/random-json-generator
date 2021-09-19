import random
from typing import Optional, Dict, Iterable, Any

import ranjg.factory
from .__common import Factory
from .._context import GenerationContext, SchemaContext
from ..options import Options


class DictFactory(Factory[dict]):
    _property_factories: Dict[str, Factory]
    _required_keys: Iterable[str]
    _properties: Dict[str, dict]

    def __init__(self, schema: Optional[dict], *,
                 schema_is_validated: bool = False, context: Optional[SchemaContext] = None):
        super(DictFactory, self).__init__(schema, schema_is_validated=schema_is_validated, context=context)

        if context is None:
            context = SchemaContext.root(self._schema)

        self._property_factories = {prop: ranjg.factory.create_factory(prop_schema,
                                                                       schema_is_validated=self.schema_is_validated,
                                                                       context=context.resolve(prop, prop_schema))
                                    for prop, prop_schema in self._schema.get("properties", {}).items()}

        self._required_keys = self._schema.get("required", tuple())
        self._properties = self._schema.get("properties", dict())

    def _get_properties_factory(self, property_name: str) -> Factory:
        return self._property_factories[property_name]

    def _factory_of(self, key: str,
                    *,
                    options: Options) -> Factory:
        if key in options.priority_schema_of_properties:
            schema = options.priority_schema_of_properties[key]
            return ranjg.factory.create_factory(schema,
                                                context=SchemaContext.for_options(
                                                    schema, path=('priority_schema_of_properties', key)))
        elif key in self._property_factories:
            return self._property_factories[key]
        else:
            schema = options.default_schema_of_properties
            return ranjg.factory.create_factory(schema,
                                                context=SchemaContext.for_options(
                                                    schema, path=('default_schema_of_properties',)))

    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[GenerationContext] = None) -> dict:
        if options is None:
            options = Options.default()
        if context is None:
            context = GenerationContext.root(self._schema)

        generated: Dict[str, Any] = dict()

        # すでに生成or棄却が済んだキー
        # それぞれのキーは生成された場合は True, 棄却された場合は False を値に持つ。
        generated_keys: Dict[str, bool] = dict()

        # 必須項目を生成する
        for required_key in self._required_keys:
            # すでに生成済みの項目は生成しない。ただし、棄却済みであるものは生成する。
            if generated_keys.get(required_key) is True:
                continue

            next_factory = self._factory_of(required_key, options=options)
            generated[required_key] = next_factory.gen_as_child(options=options,
                                                                parent_context=context,
                                                                child_key=required_key)
            generated_keys[required_key] = True

        # 必須でない項目を生成する
        for prop_key in self._properties.keys():
            # すでに生成or棄却済みの項目は生成しない。
            if generated_keys.get(prop_key) is not None:
                continue

            # 一定確率 (options に指定) で生成しない。
            if random.random() >= options.default_prob_of_optional_properties:
                generated_keys[prop_key] = False
                continue

            next_factory = self._factory_of(prop_key, options=options)
            generated[prop_key] = next_factory.gen_as_child(options=options,
                                                            parent_context=context,
                                                            child_key=prop_key)
            generated_keys[prop_key] = True

        return generated
