"""スキーマ不正エラークラスを提供するモジュール

スキーマ不正エラークラス ``InvalidSchemaError`` を__init__へ提供するモジュール。
"""
import os
from typing import List, Iterable, Union, Iterator

from jsonschema import ValidationError


_INDENT_UNIT_LENGTH = 4


def __path_part_to_str(path_part: Union[str, int]) -> str:
    """JSONパスの1区画を文字列へ変換

    Args:
        path_part: JSONパスの1区画を表す文字列か整数値

    Returns:
        JSONパスを表す文字列の1区画
    """
    return f"[{path_part}]" \
        if isinstance(path_part, int) \
        else f"[\"{path_part}\"]"


def _path_to_str(path: Iterable[Union[str, int]]) -> str:
    """JSONパスを文字列へ変換

    Args:
        path: JSONパスを表す Iterable

    Returns:
        JSONパスを表す文字列
    """
    return "".join(map(__path_part_to_str, path))


class InvalidSchemaError(Exception):
    """スキーマ不正エラークラス

    Attributes:
        __cause_list (List[ValidationErrorWrapper]):
            このエラーの原因となったバリデーションエラーのリスト
    """

    def __init__(self,
                 validation_error_list: List[ValidationError]):
        """Initialize InvalidSchemaError

        Args:
            validation_error_list:
                このエラーの原因となったバリデーションエラーのリスト
        """
        self.__cause_list = map(lambda e: ValidationErrorWrapper(e), validation_error_list)

        message_line_list = self._make_message_line_list()

        super().__init__(os.linesep + os.linesep.join(message_line_list))

    def _make_message_line_list(self) -> List[str]:
        """エラーメッセージ作成

        Returns:
            メッセージの各行からなるリスト
        """
        return sum(map(lambda c: c.make_message(), self.__cause_list), [])


class ValidationErrorWrapper:
    """バリデーションエラークラスのラッパー
    """

    @property
    def base_error(self) -> ValidationError:
        """バリデーションエラー
        """
        return self.__base_error

    @property
    def context(self) -> Iterator:
        """エラー文脈
        """
        return map(lambda e: ValidationErrorWrapper(e), self.base_error.context)

    def __init__(self, base_error: ValidationError):
        self.__base_error = base_error

    def make_message(self, indent: int = _INDENT_UNIT_LENGTH) -> List[str]:
        """バリデーションエラーのエラーメッセージを生成する。

        Args:
            indent: 各行の先頭につけるスペースの数

        Returns:
            メッセージの各行からなるリスト
        """
        path_str = _path_to_str(self.base_error.absolute_path)
        context_line_list = self._make_message_of_context(indent)

        return [
                   f"{indent * ' '}On instance{path_str}:",
                   f"{(indent + _INDENT_UNIT_LENGTH) * ' '}{self.base_error.message}",
               ] + context_line_list

    def _make_message_of_context(self, indent: int):
        """エラー文脈のエラーメッセージを作成する。

        バリデーションエラーの原因となったすべてのバリデーションエラーからメッセージを作成する。

        Args:
            indent: 各行の先頭につけるスペースの数

        Returns:
            メッセージの各行からなるリスト
        """

        def context_to_message_line(e: ValidationErrorWrapper):
            return e.make_message(indent + 2 * _INDENT_UNIT_LENGTH)

        return sum(map(context_to_message_line, self.context), [])

