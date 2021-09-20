import abc
from typing import TypeVar, Generic, Optional, Union

from ..options import Options
from .._context import GenerationContext, SchemaContext
from ..schema import validate as validate_schema

_T = TypeVar('_T')


class Factory(abc.ABC, Generic[_T]):
    _schema: dict
    #: True であれば、_schema 全体が (子要素のスキーマも含め) validated。
    _schema_is_validated: bool = False

    def __init__(self, schema: Optional[dict], *,
                 schema_is_validated: bool = False, context: Optional[SchemaContext]):
        self._schema = schema if schema is not None else {}
        self._schema_is_validated = schema_is_validated

        self.validate_schema()

    @abc.abstractmethod
    def gen(self,
            *,
            options: Optional[Options] = None,
            context: Optional[GenerationContext] = None) -> _T:
        pass

    @property
    def schema_is_validated(self) -> bool:
        return self._schema_is_validated

    def validate_schema(self) -> None:
        """validate schema

        It determines if the schema is free of irregularities.

        Raises:
            InvalidSchemaError:
                When the schema is invalid
        """
        if not self._schema_is_validated:
            validate_schema(self._schema)
            self._schema_is_validated = True

    def gen_as_child(self, *,
                     # 入力漏れを防ぐため、引数にデフォルト値は設定しない。
                     options: Options,
                     parent_context: GenerationContext,
                     child_key: Union[str, int]) -> _T:
        """Generate value as another dict or list.

        It is wrapper of ``Factory#gen`` for ranjg development since it is called in ``ListFactory#gen`` etc..
        Normally, there is no need for users of ranjg to use this method.

        This method is provided for the purpose of not creating bugs in child element generation.
        As part of this, to prevent omission of argument specification, no default argument is provided.

        In order to fulfill the purpose of this method's existence, this method should be used when creating child
        elements in ranjg.

        Args:
            options (Options):
                The options for generation.
                Usually, the options used to generate the parent element is specified as is.
            parent_context (GenerationContext):
                The context of construction.
                Usually, the context used to generate the parent element is specified as is.
            child_key (str|int):
                The path to the generated element from the parent element.
                If the parent element is a dict, it is a string; if it is a list, it is an integer.

        Returns:
            Generated something.
        """
        return self.gen(options=options,
                        context=parent_context.resolve(child_key, self._schema))
