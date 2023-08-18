from enum import Enum


class Method(str, Enum):
    SETWEBHOOK = 'setWebhook'
    ANSWERINLINEQUERY = 'answerInlineQuery'
