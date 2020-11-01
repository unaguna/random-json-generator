**ranjg 0.1.0.x — Randomly json generator**

**ranjg** is a package providing functions to generate random JSON data according to JSON-Schema-**LIKE** object. (It is similar to JSON schema, but does NOT support some keywords. Also see [here](#Supported-keywords-of-schema).)

This package can be used on command line and python code.

Quick Start (on command line)
-----------------------------
1. Install the package with the following command. (Same to usage in python code)

    ```sh
    pip install ranjg
    ```

1. Make a schema file. For example (schema.json):

    ```json : schema.json
    {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 32
            },
            "age": {
                "type": "integer",
                "minimum": 0
            },
            "comment": {
                "type": "string",
                "minLength": 1
            }
        },
        "required": ["name", "age"]
    }
    ```

1. Execute the package on command line with following command:

    ```sh
    python -m ranjg ./schema.json
    ```
    Then generated json string will be outputted.

    It generates JSON **randomly**. So you will get a different result each time you execute it.

Quick Start (in python code)
----------------------------
1. Install the package with the following command. (Same to usage on command line)

    ```sh
    pip install ranjg
    ```

1. Make a python file. For example (generate.py):

    ```python : generate.py
    import ranjg

    schema = {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string',
                'minLength': 1,
                'maxLength': 32
            },
            'age': {
                'type': 'integer',
                'minimum': 0
            },
            'comment': {
                'type': 'string',
                'minLength': 1
            }
        },
        'required': ['name', 'age']
    }

    generated = ranjg.gen(schema)

    print(generated)
    ```

1. Execute the python code with following command:

    ```sh
    python generate.py
    ```
    Then generated json string will be outputted.

    It generates JSON **randomly**. So you will get a different result each time you execute it.

Document (command line usage)
-----------------------------
You can execute ranjg with below command:
```sh
python -m ranjg <schema_file_path> [-j <json_output_path>]
```
This command generates a JSON string. Each argument has the following meaning:

- `<schema_file_path>`: A file path of the JSON-schema-like file. Generated JSON string will be according to this schema. ([What's "JSON-schema-*like*"?](#Supported-keywords-of-schema))
- `-j <json_output_path>` (optional): When it's specified, a generated JSON string will be written to the specified file. When it's not specified, a generated JSON string will be written to stdout.

Document (python code usage)
----------------------------
Usually, the following function is used:
```py : ranjg
def gen(schema: dict = None,
        schema_file: str = None,
        output_file: str = None,
        output_fp = None) -> str
```
This function returns a generated JSON string.

Either `schema` or `schema_file` must be specified (generated JSON string is according to them). `schema` is a JSON-schema-like dict and `schema_file` is the path to a JSON-schema-like file. ([What's "JSON-schema-*like*"?](#Supported-keywords-of-schema))

When `output_file` is specified, the generated JSON string will be written to the file of the specified path. When `output_fp` is specified with a file object opened in write mode, the result will be written to the specified file. You cannot specify `output_file` and `output_fp` in the same function call.

Supported keywords of schema
------------------
This package generates JSON string according to JSON-schema-**LIKE** object. *JSON-schema-LIKE object* is like general JSON schema, but it doesN'T SUPPORT some keywords of general JSON schema.

The following keywords can be used in much the same way as in regular JSON schema. (If you want to know the effect of each keyword, please read [JSON Schema Reference](https://json-schema.org/understanding-json-schema/reference/index.html).)

**Supported keywords**

- "type" (Allow only single type.)
    - **Allowed**: "object", "array", "string", "number", "integer", "boolean" and "null"
    - **NOT Allowed**: ["string", "null"] etc.
- "properties", "required"
- "items", "minItems", "maxItems", "additionalItems"
- "pattern", "minLength", "maxLength"
    - **Warning**: When "pattern" specified, "minLength" and "maxLength" are ignored.
- "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum"
    - **Warning**: Boolean specification of "exclusiveMinimum" and "exclusiveMaximum" can be used ONLY with `"type": "integer"`, but CANNOT with `"type": "number"`. (To be revised.)
