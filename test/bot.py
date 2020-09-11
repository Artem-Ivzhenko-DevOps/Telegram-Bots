import time
import telebot
import re
import pymysql


start_time = time.time()
token = '1024091588:AAFYiRd5sm5z4Ol2aF1lxFqayR8o1XNxIo0'
provider_token = ''
bot = telebot.TeleBot(token)
#Глобальные переменные
stady = 0.0
messagetext=""
serverip="localhost"    
login="oscar"
password="123456789"
DataBase="AUTOSELLBASE"
a = 10

#Меню и их кнопки
BuyAuto = telebot.types.InlineKeyboardButton('Купить автомобиль', callback_data='buyAuto')
SellAuto = telebot.types.InlineKeyboardButton('Продать автомобиль', callback_data='sellAuto')
MainMenu = telebot.types.InlineKeyboardMarkup()
MainMenu.add(BuyAuto)
MainMenu.add(SellAuto)


BactToMM = telebot.types.InlineKeyboardButton('Назад в главное меню',callback_data='backToMM')


InputSity = telebot.types.InlineKeyboardButton('Выбрать город',callback_data='insertSity')
BuyMenu = telebot.types.InlineKeyboardMarkup()
BuyMenu.add(InputSity)
BuyMenu.add(BactToMM)


CreateAuto = telebot.types.InlineKeyboardButton('Создать объявление', callback_data='createAuto')
LockAllMyAuto = telebot.types.InlineKeyboardButton('Просмотреть мои объявления', callback_data='lockAllMyAuto')
SellMenu = telebot.types.InlineKeyboardMarkup()
SellMenu.add(CreateAuto)
SellMenu.add(LockAllMyAuto)
SellMenu.add(BactToMM)


@bot.message_handler(commands = ['start'])
def start_message(message):
    bot.send_message(message.chat.id, '{0}'.format(message.chat.id), reply_markup=MainMenu)


@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
    buttons={ 'buyAuto'    : BuyAutoFunc,
              'sellAuto'   : SellAutoFunc,
              'insertSity' : InputSityFunc,
              'backToMM'   : BactToMMFunc }
    if call.message:
        stady = buttons[call.data](call)
    

def BuyAutoFunc(call):
    bot.edit_message_text(chat_id = call.message.chat.id,
                          message_id = call.message.message_id,
                          text = 'Меню покупок',
                          reply_markup = BuyMenu)
    return 1.1


def SellAutoFunc(call):
    bot.edit_message_text(chat_id = call.message.chat.id,
                          message_id = call.message.message_id,
                          text = 'Меню продаж',
                          reply_markup = SellMenu)
    return 2.1


def InputSityFunc(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Введите название города')
    return 1.2


def BactToMMFunc(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id, 
                          text='Главное меню', 
                          reply_markup=MainMenu)
    return 0.0


@bot.message_handler(content_types = ['text'])
def send_text(message):
    global stady
    if stady >= 1.0:
        readFuncs = {1.2 : SityRead}
        stady = readFuncs[stady](message)


def SityRead(message):
    global messagetext
    messagetext=message.text


bot.polling()
