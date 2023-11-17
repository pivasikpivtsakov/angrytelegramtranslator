from .event_names import EventNames as TgEventNames
from .inline_deangrify import InlineDeangrifyPayload as TgInlineDeangrifyPayload
from .private_message import PrivateMessagePayload as TgPrivateMessagePayload
from .handle import handle_private_message as tg_handle_private_message,\
    handle_inline_deangrify as tg_handle_inline_deangrify
