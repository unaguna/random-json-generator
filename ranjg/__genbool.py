import random


def genbool() -> bool:
    """スキーマに適合する真偽値を生成する。

    Returns:
        bool: 生成された真偽値
    """

    return random.random() < 0.5
