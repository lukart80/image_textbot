import os
from io import BytesIO

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

load_dotenv()
font_family = './font/my_font.ttf'
FONT_SIZE = 200
font = ImageFont.truetype(font_family, FONT_SIZE)

updater = Updater(token=os.getenv('TELEGRAM_TOKEN'))
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Пришли мне фото!')


def message(update, context):
    text = update.message.text
    context.user_data['text'] = text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Теперь пришли мне фото!')


def photo_handler(update, context):
    file = update.message.photo[-1].get_file()
    try:
        text = context.user_data['text']
        photo = BytesIO(file.download_as_bytearray())
        with Image.open(photo) as im:
            width, height = im.size
            draw = ImageDraw.Draw(im)
            draw.text((0, height / 2), text, font=font, fill='rgb(0, 0, 0)')
            im.save('super_pic.png')
            context.bot.send_photo(update.effective_chat.id,
                                   open('super_pic.png', 'rb'))
            os.remove('./super_pic.png')
    except KeyError:
        context.bot.send_message(update.effective_chat.id,
                                 text='Сначала пришли текст для фото!')


def main():
    while True:
        start_handler = CommandHandler('start', start)

        image_handler = MessageHandler(Filters.photo, photo_handler)
        text_handler = MessageHandler(Filters.text, message)
        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(image_handler)

        dispatcher.add_handler(text_handler)
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    main()
