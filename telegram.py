import telebot
import dbalchemy_request
from telebot import types

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

HELP_COMMANDS = '''
Доступные команды:
/avtor - Ссылка на автора бота
/create - Создать запись 
/view - Посмотреть записи
/email - Добавить email 
/telephone - Добавить телефонный номер
/delete - Удалить запись
'''


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP_COMMANDS)



@bot.message_handler(commands=['avtor'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Vk", url='https://vk.com/polpopoy')
    markup.add(button1)
    bot.send_message(message.chat.id, f"Страница автора".format(message.from_user), reply_markup=markup)

#-----------------------------------------------------
global FCs
FCs = ['Нет записи', 'Нет записи', 'Нет записи', 'Нет записи', 'Нет записи',]
@bot.message_handler(commands=['create'])
def greeting(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
    msg = bot.send_message(message.chat.id, "Желаете создать запись?", reply_markup=rmk)
    bot.register_next_step_handler(msg, mas)

def mas(message):
    rmk = types.ReplyKeyboardRemove()
    if message.text == 'Да':
        bot.send_message(message.chat.id, 'Имя человека', reply_markup=rmk)
        bot.register_next_step_handler(message, name)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'До встречи', reply_markup=rmk)
    else:
        bot.send_message(message.chat.id, '404', reply_markup=rmk)

def name(message):
    name = message.text
    FCs.insert(0, name)
    bot.send_message(message.chat.id, 'Фамилия человека')
    bot.register_next_step_handler(message, surname)

def surname(message):
    surname = message.text
    FCs.insert(1, surname)
    bot.send_message(message.chat.id, 'Отчество человека')
    bot.register_next_step_handler(message, fathername)

def fathername(message):
    fathername = message.text
    FCs.insert(2, fathername)
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(types.KeyboardButton("Давай"), types.KeyboardButton("Достаточно"))
    msg = bot.send_message(message.chat.id, "Желаете дополнить информацию(телефон, email)?", reply_markup=rmk)
    bot.register_next_step_handler(message, complement_or_not)

def complement_or_not(message):
    if message.text == "Достаточно":
        rmkend = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Спасибо", reply_markup=rmkend)

    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rmk.add(types.KeyboardButton("Добавить телефон"), types.KeyboardButton("Добавить email"), types.KeyboardButton("Передумал(а)/Достаточно"))
    message = bot.send_message(message.chat.id, "Что желаете дополнить?", reply_markup=rmk)
    bot.register_next_step_handler(message, complement_userinfo)

def complement_userinfo(message):
    if message.text == "Добавить телефон":
        rmk1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rmk1.add(types.KeyboardButton("Назад"))
        bot.send_message(message.chat.id, 'Введите телефон', reply_markup=rmk1)
        bot.register_next_step_handler(message, complement_telephone)
    elif message.text == "Добавить email":
        rmk2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rmk2.add(types.KeyboardButton("Назад"))
        bot.send_message(message.chat.id, 'Введите email', reply_markup=rmk2)
        bot.register_next_step_handler(message, complement_email)
    elif message.text == "Передумал(а)/Достаточно":
        record_result(message)
    else:
        bot.send_message(message.chat.id, '404')

def complement_telephone(message):
    if message.text == "Назад":
        complement_or_not(message)
    else:
        FCs.insert(3, message.text)
        bot.send_message(message.chat.id, 'Телефон добавлен')
        complement_or_not(message)

def complement_email(message):
    if message.text == "Назад":
        complement_or_not(message)
    else:
        FCs.insert(4, message.text)
        bot.send_message(message.chat.id, 'Email добавлен')
        complement_or_not(message)

def record_result(message):
    global FCs
    recors = FCs
    dbalchemy_request.record_user(recors)
    rmkend = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Запись добавлена', reply_markup=rmkend)
    FCs = []
#-----------------------------------------------------


@bot.message_handler(commands=['view'])
def view(message):
    bot.send_message(message.chat.id, f'{dbalchemy_request.view()}' )


id_and_email = []
@bot.message_handler(commands=['email'])
def email(message):
    bot.send_message(message.chat.id, 'Введите id пользователя')
    bot.register_next_step_handler(message, id_add_)

def id_add_(message):
    id_user = message.text
    id_and_email.append(int(id_user))
    bot.send_message(message.chat.id, 'Введите email')
    bot.register_next_step_handler(message, email_add)

def email_add(message):
    email = message.text
    id_and_email.append(str(email))
    dbalchemy_request.add_user_email(id_and_email)
    bot.send_message(message.chat.id, 'Изменения внесены')



id_and_telephon = []
@bot.message_handler(commands=['telephone'])
def telephone(message):
    bot.send_message(message.chat.id, 'Введите id пользователя')
    bot.register_next_step_handler(message, id_add)

def id_add(message):
    id_user = message.text
    id_and_telephon.append(int(id_user))
    bot.send_message(message.chat.id, 'Введите телефон')
    bot.register_next_step_handler(message, telephone_add)

def telephone_add(message):
    telephone = message.text
    id_and_telephon.append(int(telephone))
    dbalchemy_request.add_user_telephone(id_and_telephon)
    bot.send_message(message.chat.id, 'Изменения внесены')


@bot.message_handler(commands=['delete'])
def delete(message):
    bot.send_message(message.chat.id, 'Введите id пользователя')
    bot.register_next_step_handler(message, id_delete)

def id_delete(message):
    id_user = message.text
    dbalchemy_request.delete(id_user)
    bot.send_message(message.chat.id, 'Пользователь удален')







bot.polling()














