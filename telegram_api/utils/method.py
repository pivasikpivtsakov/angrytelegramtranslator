from enum import StrEnum


class Method(StrEnum):
    SETWEBHOOK = "setWebhook"
    ANSWERINLINEQUERY = "answerInlineQuery"
    SEND_PHOTO = "sendPhoto"
