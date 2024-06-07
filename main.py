import json
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types , F 
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart , Command
from aiogram.types import Message , CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton 
import buttons 
from states1 import Crypt
from states1 import Kurschange
from states1 import Sellusdts
group_id =-4180547434
TOKEN ="Emirlan Ysmanov"

# All handlers should be attached to the Router (or Dispatcher)
bot = Bot(TOKEN)
dp = Dispatcher()
router = Router()



# Загрузка данных из JSON-файла
with open('kurs.json') as json_file:
    data = json.load(json_file)

# Функция для сохранения данных в JSON-файл
def save_data(data):
    with open('kurs.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def load_data():
    with open('kurs.json') as json_file:
        return json.load(json_file)
    


# Command start
@dp.message(Command("start"))
async def start(message: Message):
    if message.chat.type == 'private':
        data = load_data()
        buy_rate = data['BUY_RATE']
        sell_rate = data['SELL_RATE']
        await message.answer(f"""Привет🙌 <b>{message.from_user.first_name}</b>!\nПокупаем и продаем USDT (Тезер), а также любые другие криптовалюты по рыночному курсу
Покупка USDT по <b><i>{buy_rate}</i></b>
Продажа USDT по <b><i>{sell_rate}</i></b>
Другую криптовалюту покупаем по рыночному курсу, заранее обговорив в ЛС.
👨‍💻Работаем 24/7
👨‍💻Служба поддержки: @P2P_succsess""",parse_mode="HTML",reply_markup=buttons.magaz_kb)
    else:
        return 

# Command menu 
@dp.message(Command("menu"))
async def menu(message: Message):
    await message.answer("<b>Menu</b>",reply_markup=buttons.magaz_kb,parse_mode="HTML")
        





#Команда чтобы менять валюту только Для U1uk baike
@dp.message(F.text.lower() == 'в')
async def changevaluta(message: Message, state: FSMContext):
    await message.answer("Напишите новый курс для Покупки USDT")
    await state.set_state(Kurschange.Buy)
#get BUYRATE
@dp.message(Kurschange.Buy)
async def getbuyrate(message: Message , state: FSMContext):
    BY = float(message.text)
    data = load_data()
    data['BUY_RATE'] = BY
    save_data(data)
    await message.answer("Напишите новый курс для Продажи USDT")
    await state.set_state(Kurschange.Sell)
#get SELL_RATE
@dp.message(Kurschange.Sell)
async def getsellrate(message: Message, state: FSMContext):
    SY = float(message.text)
    data = load_data()
    data['SELL_RATE'] = SY
    save_data(data)
    await state.clear()
    await message.answer("Курс USDT был изменен✅   ")

    



      

#Основные callbacks бота /////////////////////////////////////////////////////////////////////////////////
#Основное отличие в том что мы начали callbackquery с @dp и начали обрабатывать сами состояние с @router.message а надо с какой начал с такой и закончил оказывается , крч и там и там должно быть первоначальный [handler]
@dp.callback_query(lambda callback_query: callback_query.data == "busdt")
async def allcalbacks(calback: CallbackQuery, state: FSMContext):
        await calback.message.answer("""<b>Выберите необходимый способ для оплаты!</b>""",parse_mode="HTML",reply_markup=buttons.paycards)


#Реквизиты callback 
@dp.callback_query(lambda callback_query: callback_query.data == "requisites")
async def allcalbacks(calback: CallbackQuery, state: FSMContext):
    await calback.message.answer("""Реквизиты для оплаты:

Банк: MBANK
Реквизиты: `UlukBa1ke`
""",parse_mode="MarkdownV2",reply_markup=buttons.finishpay)

#Я оплатил callback 
@dp.callback_query(lambda callback_query: callback_query.data == "fnpay")
async def allcalbacks(calback: CallbackQuery, state: FSMContext):
    await calback.message.answer("""Отправьте СКРИНШОТ Платёжа!
❗️В скриншоте должны быть видны Дата и Время совершения платежа!
В противном случае ваш платёж может не поступить на ваш адрес!
""")
    await state.set_state(Crypt.screen)
    
#Вернуться в главное меню 
@dp.callback_query(lambda callback_query: callback_query.data == "bcktomenu")
async def allcalbacks(calback: CallbackQuery, state: FSMContext):
    await calback.message.answer("<b>Главное меню</b>",reply_markup=buttons.magaz_kb,parse_mode="HTML")

#Мбанк покупка     
@dp.callback_query(lambda callback_query: callback_query.data == "mbankcardbuy")
async def cardmbank(calback: CallbackQuery, state: FSMContext):
    await calback.message.answer("""<i><b>Введите ФИО - MBANK</b></i>
❗️ Внимание❗️
Перевод должен быть выполнен с MBANK на MBANK!
❗️Если пополнение будет совершено с терминалов или других платёжных систем, денежные средства НЕ ПОСТУПЯТ на ваш счёт!
""",parse_mode="HTML")
    await state.set_state(Crypt.Fio)
# Getting trc adress
@dp.message(Crypt.Fio)
async def getfiobuy(message: Message , state: FSMContext):
    await state.update_data(Fio=message.text)
    await state.set_state(Crypt.trc)
    await message.answer("Введите ваш адрес USDT TRC20",parse_mode="HTML",reply_markup=buttons.instructiontrc)

# Getting sum of replenishment 
@dp.message(Crypt.trc)
async def gettrcbuy(message: Message,state: FSMContext):
    data1 = load_data()
    buy_rate = data1['BUY_RATE']
    sell_rate = data1['SELL_RATE']
    await state.update_data(trc=message.text)
    await state.set_state(Crypt.sum)
    await message.answer(f"""Укажите сумму пополнения KGS. \nМинимальная: <strong>200</strong> | Максимальная: <strong>1 000 000</strong>
<blockquote>Курс покупки USDT <b>{buy_rate}</b></blockquote>""",parse_mode="HTML")


# checking if it right ? 
@dp.message(Crypt.sum)
async def getsumbuy(message: Message, state:FSMContext):
    data1 = load_data()
    buy_rate = data1['BUY_RATE']
    sell_rate = data1['SELL_RATE']
    amount = message.text
    if amount.isdigit():
        if amount[0]=="0":
            await message.answer("Укажите правильную сумму пополнения!")
        elif int(amount) >= 200 and int(amount) <=1000000:
            await state.update_data(sum=message.text)
            data = await state.get_data()
            await state.set_state(Crypt.screen)
            newtrc = float(data['sum']) / buy_rate
            await message.answer(f"""Вы указали сумму пополнения:{data["sum"]}\nТо есть вот столько usdt - {newtrc} """)
            await message.answer(f"Отправьте {data['sum']} по следующим реквизитам",reply_markup=buttons.requisites)
        else: 
            await message.answer("Укажите правильную сумму пополнения!")
    else: 
        await message.answer("Укажите правильную сумму пополнения!")

# Final message to user and sending all data`s to group 
@dp.message(Crypt.screen , F.photo)
async def getscreen(message: Message , state: FSMContext):
    screen_id = message.photo[-1].file_id
    data = await state.get_data()
    await state.clear()
    await message.answer(f"""✅Ваша заявка принята на проверку!

🆔Ваш адрес кошелька USDT TRC20: {data["trc"]}
💵Сумма: {data["sum"]}

⚠️ Пополнение занимает от 1 секунды до 10 минут.
Пожалуйста, подождите!

✅Вы получите уведомление о зачислении средств!

Если возникли проблемы 👇
👨‍💻Служба поддержки: @P2P_succsess
""",reply_markup=buttons.backtomainmenu)
    await bot.send_photo(
    chat_id=group_id, 
    photo=screen_id, 
    caption=f"""<b>ФИО</b>-{data["Fio"]}
<b>Адрес TRC</b> - {data["trc"]}
<b>Сумма пополнения</b> - {data['sum']}""",
    parse_mode="HTML",
    message_thread_id=None 
)
#Начало продажы СВОИХ USDT 
@dp.callback_query(lambda callback_query: callback_query.data == "susdt")
async def allcalbacks(calback: CallbackQuery, state: FSMContext):
    await calback.message.answer("Выберите удобный для вас способ приема оплаты!",reply_markup=buttons.sellcards)
# asking for mbank number
@dp.callback_query(lambda callback_query: callback_query.data == "mbankcardsell")
async def allcalbacks(calback: CallbackQuery, state: FSMContext):
    await calback.message.answer("Введите пожалуйста номер вашего МБАНКА")
    await state.set_state(Sellusdts.mbanknum)
# here finally getting mbank num 
@dp.message(Sellusdts.mbanknum)
async def getmbanknumsell(message: Message, state: FSMContext):
    data1 = load_data()
    buy_rate = data1['BUY_RATE']
    sell_rate = data1['SELL_RATE']
    await state.update_data(mbanknum=message.text)
    await state.set_state(Sellusdts.screensell)
    data2 = await state.get_data()
    await message.answer(f"""✅Ваш номер МБАНКа сохранен: <code>{data2["mbanknum"]}</code>
Отправьте свои USDT на наш адрес: <code>{451452352436546526345}</code>
------------------------------------------------------------------------------------------------------
Внимание❗️ Это адрес USDT в сети TRC20❗️❗️ Будьте внимательны❗️❗️

Курс продажи USDT [<code>{sell_rate}</code>]


Отправьте СКРИНШОТ Платёжа!
❗️В скриншоте должны быть видны Дата и Время совершения платежа!
В противном случае ваш платёж может не поступить на ваш аккаунт!
""",parse_mode="HTML")


@dp.message(Sellusdts.screensell, F.photo)
async def getmbanknumsell(message: Message, state: FSMContext):
    data1 = load_data()
    buy_rate = data1['BUY_RATE']
    sell_rate = data1['SELL_RATE']
    screenidsell = message.photo[-1].file_id
    data = await state.get_data()
    await state.clear()
    await message.answer(f"""✅Ваша заявка принята на проверку!
🆔Ваш номер МБАНКа: <code><u>{data["mbanknum"]}</u></code> 

⚠️ Пополнение занимает от 1 секунды до 10 минут.
Пожалуйста подождите!

✅Вы получите уведомление о зачислении средств!

Если возникли проблемы 👇
👨‍💻Служба поддержки: @P2P_succsess
""",parse_mode="HTML")
    await bot.send_photo(
    chat_id=group_id, 
    photo=screenidsell, 
    caption=f"""<b>🆔Номер МБАНКА продавца🆔</b> - <code>{data['mbanknum']}</code>""",parse_mode="HTML",
    message_thread_id=None 
)
    
    #await bot.send_photo(group_id , screenidsell ,None , f"""<b>🆔Номер МБАНКА продавца🆔</b> - <code>{data['mbanknum']}</code>""",parse_mode="HTML")
    
    


    

#Помощь и Менюшка в простом тексте 
#кнопка меню после меню
@dp.message(F.text.lower() == "меню")
async def putonmenu(message: Message):
    await message.answer("<i><b>Меню</b></i>",reply_markup=buttons.magaz_kb,parse_mode="HTML")
#если слово помощь то приходит помощь 
@dp.message(F.text.lower() == "помощь")
async def sendhelp(message: Message):
    await message.answer(f"<code>Здравсвтуй {message.from_user.first_name} !\nЯ бот криптообменник , по всем вопросам обращайся к этому человеку</code>  @P2P_succsess ",parse_mode="HTML")
#любой другой текст 
@dp.message(F.text)
async def anyothertext(message: Message):
    await message.delete()
    #await message.answer("Напиши слово <code><b>Помощь</b></code> чтобы узнать лучше функции и команды бота. Спасибо за понимание 👍",parse_mode="HTML")




async def main() -> None:
    
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    
# Иногда классно сидеть и печатать на своей классной клаве , так как очень приятно пальцам и звук тоже прятен. Хотелось бы в дальнейшем как то писать книги но мне кажется нужно сначала прочтитать настолько много кнги чтобы начуиться их писать . В дальнейшем хочется чтобы все было хорошо у меня и у моей семьи да и все.  
