from enum import StrEnum


class EventNames(StrEnum):
    INLINE_DEANGRIFY = "TG_INLINE_DEANGRIFY"
    PRIVATE_MESSAGE = "TG_PRIVATE_MESSAGE"
