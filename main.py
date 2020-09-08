import telebot
import json
import sqlite3
import csv

token = '1024091588:AAFYiRd5sm5z4Ol2aF1lxFqayR8o1XNxIo0'
bot = telebot.TeleBot(token)
stady = 0
conn = None
db_name = ''
table_name = ''
a = 10


Json_in_SQL = telebot.types.InlineKeyboardButton('Json in SQL', callback_data='json_sql')
CSV_in_SQL = telebot.types.InlineKeyboardButton('CSV in SQL', callback_data='csv_sql')
MainMenu = telebot.types.InlineKeyboardMarkup()
MainMenu.add(Json_in_SQL)
MainMenu.add(CSV_in_SQL)


Json_in_Base = telebot.types.InlineKeyboardButton('Json in data base', callback_data='json_in_base')
Json_in_Data = telebot.types.InlineKeyboardButton('Json in data for data base', callback_data='json_in_data')
json_Menu = telebot.types.InlineKeyboardMarkup()
json_Menu.add(Json_in_Base)
json_Menu.add(Json_in_Data)


CSV_in_Base = telebot.types.InlineKeyboardButton('CSV in data base', callback_data='csv_in_base')
CSV_in_Data = telebot.types.InlineKeyboardButton('CSV in data for data base', callback_data='csv_in_data')
csv_Menu = telebot.types.InlineKeyboardMarkup()
csv_Menu.add(CSV_in_Base)
csv_Menu.add(CSV_in_Data)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Menu', reply_markup=MainMenu)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global stady
    buttons = {
        'json_sql':      json_in_sql_func,
        'json_in_base':  json_in_base_return,
        'json_in_data':  json_in_data_return,
        'csv_sql':       csv_in_sql_func,
        'csv_in_base':   csv_in_base_return,
        'csv_in_data':   csv_in_data_return
    }
    if call.message:
        stady = buttons[call.data](call)


def json_in_sql_func(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='JSON menu',
                          reply_markup=json_Menu)
    return 1


def csv_in_sql_func(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='CSV menu',
                          reply_markup=csv_Menu)
    return 2


def json_in_base_return(call):
    print_send_file(call=call)
    return 11


def json_in_data_return(call):
    print_send_file(call=call)
    return 12


def csv_in_base_return(call):
    print_send_file(call=call)
    return 21


def csv_in_data_return(call):
    print_send_file(call=call)
    return 22


def print_send_file(call):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Send File')


@bot.message_handler(content_types=['text'])
def send_text(message):
    global stady
    read_funcs = {
    '110': num_file,
    '210': csv_in_base_func
    }
    stady = read_funcs[str(stady)](message=message)


def num_file():
    conn.execute('CREATE TABLE "users" (id, first_name, last_name, birthday)')
    return 100


@bot.message_handler(content_types=['file'])
def send_text(message):
    global stady
    read_funcs = {
    '11': json_in_base_func,
    '12': json_in_data_func,
    '21': csv_in_base_func,
    '22': csv_in_data_func
    }
    stady = read_funcs[str(stady)](message=message)


def json_in_base_func(message):
    global conn
    conn = sqlite3.connect(str(message.chat.id))
    data = json.load(message.file)
    print(data)
    return 110


def json_in_data_func(message):
    return 120


def csv_in_base_func(message):
    reader = download_csv(message=message)
    return 210


def csv_in_data_func(message):
    global table_name
    reader = download_csv(message=message)
    sql = sql = "INSERT INTO %s (" % table_name
    with open(message.id, 'w') as f:
        for i in reader:
            for item in i:
                sql += "%s," % str(item)
            break
        sql[len(sql) - 1] = ')'
        sql += ' values ('
        sql_base = sql
        for i in reader[1:]:
            sql = sql_base
            for item in i:
                sql += "'%s', " % str(item)
            sql[len(sql) - 1] = ')\n'
            f.write(sql)
    return 220


def download_csv(message):
    raw = message.document.file_id
    path = raw+".csv"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as f:
        f.write(downloaded_file)
    with open(raw, 'r') as f:
        reader = csv.reader(f)
        return reader


bot.polling()
