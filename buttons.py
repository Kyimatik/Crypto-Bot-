from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton , KeyboardButton , ReplyKeyboardRemove
#Главные кнопки кнопки /start 
magaz_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Покупка USDT",callback_data="busdt"),
            InlineKeyboardButton(text="Продажа USDT",callback_data="susdt")
            
        ],
        [
            InlineKeyboardButton(text="Купить/Продать другую криптовалюту",url="https://t.me/P2P_succsess?")
        ],
        [
            InlineKeyboardButton(text="Инструкция",callback_data="instruction")
        ]
        
    ],
)

#Выбор карточек для ПОКУПКИ МБАНКА 
paycards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Мбанк",callback_data="mbankcardbuy"),
        ]
    ],
    resize_keyboard=True
)
#Выбор карточек для ПРОДАЖИ МБАНКА 
sellcards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Мбанк",callback_data="mbankcardsell"),
        ]
    ],
    resize_keyboard=True
)
#Реквизиты при покупке USDT мбанк 
requisites = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Реквизиты #️⃣",callback_data="requisites")
        ]
    ],
)
#Кнопка я оплатил 
finishpay = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Я оплатил",callback_data="fnpay")
        ]
    ],
)

#После самого последнего действия вернуться в главное меню
backtomainmenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Вернуться в главное МЕНЮ",callback_data="bcktomenu")
        ]
    ],
)

#Инструкция о том как найти свой адрес trc 
instructiontrc = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Инструкция",callback_data="instructrc")
        ]
    ],
)
