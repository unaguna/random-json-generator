from collections import namedtuple


class NumberRange(namedtuple("NumberRange", "minimum maximum exclusive_minimum exclusive_maximum")):

    def __contains__(self, item):
        if item < self.minimum:
            return False
        elif item > self.maximum:
            return False
        elif self.exclusive_minimum and item <= self.minimum:
            return False
        elif self.exclusive_maximum and item >= self.maximum:
            return False
        else:
            return True

    def replace(self, **kwargs):
        return self._replace(**kwargs)

    @classmethod
    def from_schema(cls, schema: dict = None):
        """Initialize NumberRange

        Args:
            schema: Schema object.
        """
        if schema is None:
            schema = {}
        return _from_schema(schema)


def _from_schema(schema: dict) -> NumberRange:
    """Initialize NumberRange

    Args:
        schema: Schema object.
    """
    minimum = schema.get("minimum")
    maximum = schema.get("maximum")
    exclusive_minimum = schema.get("exclusiveMinimum")
    exclusive_maximum = schema.get("exclusiveMaximum")

    if exclusive_minimum is None:
        # exclusive_minimum の指定が無いなら、フラグは立たない。
        exclusive_minimum = False
    elif exclusive_minimum is True:
        # exclusive_minimum が True なら、フラグが立つ。ただし minimum の指定が無い場合はフラグを立てない決まり。
        exclusive_minimum = minimum is not None
    elif exclusive_minimum is False:
        # exclusive_minimum が False なら、フラグが立たない。
        pass
    else:
        # exclusive_minimum が数値なら、minimum 以上なら使用される。
        if minimum is None or minimum <= exclusive_minimum:
            minimum = exclusive_minimum
            exclusive_minimum = True
        else:
            exclusive_minimum = False

    maximum = maximum
    if exclusive_maximum is None:
        # exclusive_maximum の指定が無いなら、フラグは立たない。
        exclusive_maximum = False
    elif exclusive_maximum is True:
        # exclusive_maximum が True なら、フラグが立つ。ただし maximum の指定が無い場合はフラグを立てない決まり。
        exclusive_maximum = maximum is not None
    elif exclusive_maximum is False:
        # exclusive_maximum が False なら、フラグが立たない。
        pass
    else:
        # exclusive_maximum が数値なら、maximum 以下なら使用される。
        if maximum is None or maximum >= exclusive_maximum:
            maximum = exclusive_maximum
            exclusive_maximum = True
        else:
            exclusive_maximum = False

    return NumberRange(minimum=minimum,
                       maximum=maximum,
                       exclusive_minimum=exclusive_minimum,
                       exclusive_maximum=exclusive_maximum)
