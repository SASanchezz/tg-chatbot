from telebot import TeleBot, types
from config.python import BOT_TOKEN
from modules.Users import add_user
from modules.Stickers import *
from modules.UsersChats import *
from interfaces.UsersChats.UsersChatsFields import UserChatFields
from interfaces.Stickers.StickerFields import StickerFields
from interfaces.States.States import StickerStates


def start():
    bot = TeleBot(BOT_TOKEN)

    @bot.message_handler(commands=['all'])
    def get_all(message):
        output = 'Все стикеры: '
        stickers = find_all_stickers()
        for sticker in stickers:
            output += (sticker[0] + ', ')
        bot.send_message(message.chat.id, output)

    @bot.message_handler(commands=['auth', 'start', 'help'])
    def send_auth(message):
        add_user(message.from_user.id,
                 message.from_user.username,
                 message.from_user.first_name,
                 str(message.from_user.last_name or ''))
        bot.send_message(message.chat.id,
                         'Отправьте стикер, а затем имя к нему, чтобы сохранить, '
                         + 'затем просто пишите /<название стикера>, чтобы получить его\n\n'
                         + 'Введите /all для получения списка всех стикеров')

    @bot.message_handler(content_types='sticker')
    def new_sticker(message: types.Message):
        if user_chat_exists(message.from_user.id, message.chat.id):
            change_user_chat(message.from_user.id, message.chat.id, int(StickerStates.adding_sticker),
                             message.sticker.file_id)
        else:
            add_user_chat(message.from_user.id, message.chat.id, int(StickerStates.adding_sticker),
                          message.sticker.file_id)

        msg = bot.reply_to(message, 'Введите имя для стикера')
        bot.register_next_step_handler(msg, name_sticker)

    def name_sticker(message: types.Message):
        if message.text is None or sticker_exists(message.text):
            msg = bot.reply_to(message, 'Такое имя уже занято или вы отправили не текст')
            bot.register_next_step_handler(msg, name_sticker)
            return

        sticker_title = find_user_chat(message.from_user.id, message.chat.id)[UserChatFields.last_sticker]

        add_sticker(message.text, sticker_title)
        change_user_chat(message.from_user.id, message.chat.id, int(StickerStates.initial), None)

    @bot.message_handler(content_types='text')
    def get_sticker(message: types.Message):
        msg = message.text
        if msg[0] != '/': return
        msg = msg[1:]
        sticker_id = find_sticker(msg)[StickerFields.sticker_id] \
            if find_sticker(msg) is not None else None

        if sticker_id is not None:
            bot.send_sticker(message.chat.id, sticker=sticker_id)
        else:
            bot.send_message(message.chat.id, 'Нет такого дня :с')

    bot.polling()


if __name__ == '__main__':
    print('Started')
    start()
