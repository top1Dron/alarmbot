from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


alarm_type_callback = CallbackData("type", "type_name")


not_configured_google_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Дать доступ к Google Calendar'),
        ],
    ],
    resize_keyboard=True,
    selective=True,
)

configured_google_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изменить Google Calendar'),
        ],
        [
            KeyboardButton(text='Получить ближайшие события из календаря Google'),
        ],
        [
            KeyboardButton(text='Добавить событие'),
            KeyboardButton(text='Просмотреть все события'),
        ],
        [
            KeyboardButton(text='Настроить напоминания'),
        ],
    ],
    resize_keyboard=True,
    selective=True,
)

def create_back_menu(callback_data) -> InlineKeyboardMarkup:
    chat_settings_menu_back = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Отмена', callback_data=callback_data),
            ],
        ]
    )
    return chat_settings_menu_back

alarm_type_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='С утра',
                                 callback_data=alarm_type_callback.new(type_name='from_morning'))
        ],
        [
            InlineKeyboardButton(text='С вечера',
                                 callback_data=alarm_type_callback.new(type_name='from_evening'))
        ],
        [
            InlineKeyboardButton(text='За определённое время',
                               callback_data=alarm_type_callback.new(type_name='by_time'))
        ],
        [
            InlineKeyboardButton(text='Отмена', callback_data='back_alarm_choose'),
        ],
    ]
)


chat_callback = CallbackData("chosen_chat", "chat_id")


