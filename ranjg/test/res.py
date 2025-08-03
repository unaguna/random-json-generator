from typing import Union, Dict

__SAMPLE_SCHEMA_STR = {
    'type': 'string',
    'minLength': 10,
    'maxLength': 20,
}

__SAMPLE_SCHEMA_INT = {
    'type': 'integer',
    'minimum': 1,
    'maximum': 5,
}

__SAMPLE_SCHEMA_NUM = {
    'type': 'number',
    'minimum': 1,
    'maximum': 5,
}

__SAMPLE_SCHEMA_BOOL = {
    'type': 'boolean',
}

__SAMPLE_SCHEMA_NULL = {
    'type': 'null',
}

__SAMPLE_SCHEMA_ARRAY = {
    'type': 'array',
    'minItems': 2,
    'maxItems': 4,
    'items': {'type': 'boolean'},
}

__SAMPLE_SCHEMA_OBJECT = {
    'type': 'object',
    'required': ['p1', 'p2'],
    'properties': {'p1': {'type': 'boolean'}},
}

__SAMPLE_SCHEMA = {
    'null': __SAMPLE_SCHEMA_NULL,
    'boolean': __SAMPLE_SCHEMA_BOOL,
    'integer': __SAMPLE_SCHEMA_INT,
    'number': __SAMPLE_SCHEMA_NUM,
    'string': __SAMPLE_SCHEMA_STR,
    'object': __SAMPLE_SCHEMA_OBJECT,
    'array': __SAMPLE_SCHEMA_ARRAY,
}

__TYPE_MAP: Dict[type, str] = {
    None: 'null',
    bool: 'boolean',
    int: 'integer',
    float: 'number',
    str: 'string',
    list: 'array',
    dict: 'object',
}


def sample_schema(typ: Union[str, type]) -> dict:
    """Returns a sample schema for dict.

    This function is pure and does not dynamically change its return value.
    However, since the return value may change depending on the version upgrade of the module,
    we should not create tests that depend on the contents of these schemas.

    Args:
        typ:
            value of schema.type

    Returns:
        the schema
    """
    if isinstance(typ, type):
        typ = _type_to_type_str(typ)

    return __SAMPLE_SCHEMA[typ].copy()


def _type_to_type_str(t: type) -> str:
    return __TYPE_MAP[t]


def class_path(clz) -> str:
    return f'{clz.__module__}.{clz.__name__}'
