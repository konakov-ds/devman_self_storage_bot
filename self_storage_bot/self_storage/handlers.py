import re
from collections import defaultdict
from dotenv import load_dotenv
from telegram import KeyboardButton, ReplyKeyboardMarkup,\
    ReplyKeyboardRemove
from telegram.ext import CommandHandler, ConversationHandler,\
    Filters, MessageHandler


load_dotenv()

users_info = defaultdict()
storage_info = defaultdict()

ADDRESSES = ['⚓️ Адрес 1', '⚓️ Адрес 2', '⚓️ Адрес 3', '⚓️ Адрес 4']

ADDRESSES_KEYBOARD = ReplyKeyboardMarkup(
    keyboard = [
                [
                    KeyboardButton(text=address),
                ]
                for address in ADDRESSES
            ],
    resize_keyboard=True
)

TYPE_STORAGE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard = [
                [
                    KeyboardButton(text='Сезонные вещи'),
                    KeyboardButton(text='Другое'),
                    KeyboardButton(text='Главное меню'),
                ]
            ],
    resize_keyboard=False
)


def start(update, context):
    message = update.message
    user_name = message.chat.first_name
    user_id = message.chat_id

    context.bot.send_message(
        chat_id=user_id,
        text=(
            f'Привет, {user_name}.🤚\n\n'
            'Я помогу вам арендовать личную ячейку для хранения вещей.'
            'Давайте посмотрим адреса складов, чтобы выбрать ближайший!'
        ),
        reply_markup=ADDRESSES_KEYBOARD,
    )
    print('select 1')
    return 1

def select_address(update, context):
    message = update.message
    user_id = message.chat_id

    address = update.message.text
    storage_info[user_id]['address'] = address

    context.bot.send_message(
        chat_id=user_id,
        text='Что хотите хранить?',
        reply_markup=TYPE_STORAGE_KEYBOARD
    )

    return 2

def select_storage_type(update, context):
    user_id = update.effective_chat.id
    address = update.message.text
    print(address)
    storage_info[user_id]['address'] = address

    context.bot.send_message(
        chat_id=user_id,
        text='Что хотите хранить?',
        reply_markup=TYPE_STORAGE_KEYBOARD
    )

    return 2


def stop(update):
    update.message.reply_text("Стоп")
    return ConversationHandler.END


order_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        1: [MessageHandler(Filters.text, select_address, pass_user_data=True)],
        # 2: [MessageHandler(Filters.text, select_storage_type, pass_user_data=True)],
        # 6: [MessageHandler(Filters.text, select_toppings, pass_user_data=True)],
        # 7: [MessageHandler(Filters.text, select_berries, pass_user_data=True)],
        # 8: [MessageHandler(Filters.text, select_decor, pass_user_data=True)],
        # 9: [MessageHandler(Filters.text, select_print, pass_user_data=True)],
        # 10: [MessageHandler(Filters.text, check_print_selection, pass_user_data=True)],
        # 11: [MessageHandler(Filters.text, save_print, pass_user_data=True)],
        # 12: [MessageHandler(Filters.text, ask_comment, pass_user_data=True)],
        # 13: [MessageHandler(Filters.text, save_comment, pass_user_data=True)],
        # 14: [MessageHandler(Filters.text, check_address, pass_user_data=True)],
        # 15: [MessageHandler(Filters.text, save_address, pass_user_data=True)],
        # 16: [MessageHandler(Filters.text, ask_delivery_time, pass_user_data=True)],
        # 17: [MessageHandler(Filters.text, apply_promocode, pass_user_data=True)],
        # 18: [MessageHandler(Filters.text, create_order_menu, pass_user_data=True)],
    },


    fallbacks=[CommandHandler('stop', stop)]
)
