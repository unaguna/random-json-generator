import os
from typing import List, Iterable, Union
from jsonschema import ValidationError


class InvalidSchemaError(Exception):
    __INDENT_UNIT_LENGTH = 4

    def __init__(self,
                 validation_error_list: List[ValidationError]):
        self.__validation_error_list = validation_error_list

        message_line_list = sum(map(self.__make_message_by_error, validation_error_list), [])

        super().__init__(os.linesep + os.linesep.join(message_line_list))

    def __make_message_by_error(self, error: ValidationError, indent: int = __INDENT_UNIT_LENGTH) -> List[str]:
        """バリデーションエラー毎のエラーメッセージを生成する。
        
        Args:
            error: バリデーションエラー
            indent: 各行の先頭につけるスペースの数

        Returns:
            メッセージの各行からなるリスト
        """

        def context_to_message_line(e: ValidationError):
            """エラーの文脈毎のエラーメッセージを生成する。

            Args:
                e: バリデーションエラー

            Returns:
                指定したバリデーションエラーが発生するに至る原因となったバリデーションエラーのエラーメッセージの各行からなるリスト。
            """
            return self.__make_message_by_error(e, indent + 2 * self.__INDENT_UNIT_LENGTH)

        path_str = self.__path_to_str(error.absolute_path)
        context_line_list = sum(map(context_to_message_line, error.context), [])

        return [
                   f"{indent * ' '}On instance{path_str}:",
                   f"{(indent + self.__INDENT_UNIT_LENGTH) * ' '}{error.message}",
               ] + context_line_list

    def __path_to_str(self, path: Iterable[Union[str, int]]) -> str:
        """JSONパスを文字列へ変換

        Args:
            path: JSONパスを表す Iterable

        Returns:
            JSONパスを表す文字列
        """
        return "".join(map(self.__path_part_to_str, path))

    def __path_part_to_str(self, path_part: Union[str, int]) -> str:
        """JSONパスの1区画を文字列へ変換

        Args:
            path_part: JSONパスの1区画を表す文字列か整数値

        Returns:
            JSONパスを表す文字列の1区画
        """
        return f"[{path_part}]" \
            if isinstance(path_part, int) \
            else f"[\"{path_part}\"]"


class SchemaConflictError(Exception):
    pass


class GenerateError(Exception):
    pass
