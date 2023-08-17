from telegram.models import InputMessageContent


class InputTextMessageContent(InputMessageContent):
    message_text: str
