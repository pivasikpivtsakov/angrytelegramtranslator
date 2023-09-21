import asyncio

from telegram_api.methods import send_photo, SendPhotoBody
from telegram_api.models import InputFile


async def main():
    path_to_file = input("path to file: ")
    your_id = input("your id: ")
    result = await send_photo(
        SendPhotoBody(
            chat_id=int(your_id),
            photo=InputFile(path_to_file=path_to_file, type="photo")
        )
    )
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
