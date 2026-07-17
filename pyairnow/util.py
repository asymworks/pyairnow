'''Shared helpers for response normalization'''
from typing import Any


def coalesce(raw: dict, *keys: str, default: Any = None) -> Any:
    '''
    Return the first non-null value among `keys`, or `default`.

    `dict.get(key, default)` only falls back when the key is absent, so a key
    present with a JSON null returns None rather than the default.
    '''
    for key in keys:
        value = raw.get(key)
        if value is not None:
            return value
    return default
