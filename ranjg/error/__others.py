from .._context import Context


class GenerateError(Exception):
    """Errors during randomly generation.
    """
    def __init__(self, message: str, context: Context):
        super(GenerateError, self).__init__(message)
        self.context = context


class SchemaConflictError(GenerateError):
    """Conflict errors in the schema.

    This error raises if the schema has conflict.
    In other words, when no value satisfy the schema, this error is raised.

    When the schema is invalid (exp: ``schema.type`` is illegal string), ``InvalidSchemaError`` is raised.
    """
    pass
