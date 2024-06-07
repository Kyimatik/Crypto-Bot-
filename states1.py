from aiogram.fsm.state import StatesGroup , State

# Машина состояний для BuyUSDT
class Crypt(StatesGroup):
    Fio = State()
    trc = State()
    sum = State()
    screen = State()
# Машина состояний для изменения курса
class Kurschange(StatesGroup):
    Buy = State()
    Sell = State()
# Машина состояний для SellUSDT
class Sellusdts(StatesGroup):
    mbanknum = State()
    screensell = State()