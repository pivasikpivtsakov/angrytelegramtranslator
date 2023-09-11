from enum import Enum


def enum_to_set_str(_enum: type[Enum]) -> set[str]:
    return set(map(str, _enum))
