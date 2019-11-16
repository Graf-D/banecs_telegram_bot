import telebot
from peewee import SqliteDatabase, fn

import conf
from banecbot.model import Anecdote, db
from banecbot.telegram_bot.chat_state import ChatState


if conf.PROXY:
    telebot.apihelper.proxy = {'https': conf.PROXY}

bot = telebot.TeleBot(conf.TG_ACCESS_TOKEN)
chat_states = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, conf.WELCOME_MESSAGE,
                     parse_mode='Markdown',
                     reply_markup=telebot.types.ReplyKeyboardRemove())


def send_anecdotes(chat_id):
    global chat_states
    anecs = list(Anecdote.select().order_by(fn.Random()).limit(2))
    try:
        chat_states[chat_id].last_anecs = anecs
    except KeyError:
        bot.send_message(chat_id, 'Что-то пошло не так. Нажмите /play еще раз',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

    for i, anec in enumerate(anecs):
        reply_text = '\n\n'.join([f'<b>АНЕКДОТ {i + 1}</b>', anec.text])
        bot.send_message(chat_id, reply_text, parse_mode='HTML')

    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                                 resize_keyboard=True,
                                                 one_time_keyboard=True)
    button_first = telebot.types.KeyboardButton(chr(0x261D) + 'Первый')
    button_second = telebot.types.KeyboardButton(chr(0x270C) + 'Второй')
    not_anec_msg = chr(0x1F612) + 'Что-то из этого вообще не анек'
    button_not_anec = telebot.types.KeyboardButton(not_anec_msg)
    keyboard.add(button_first, button_second, button_not_anec)
    bot.send_message(chat_id,
                     'Какой из этих анеков набрал больше лайков?',
                     reply_markup=keyboard)


@bot.message_handler(commands=['play'])
def start_play(message):
    global chat_states
    chat_states[message.chat.id] = ChatState(message.chat.id)
    send_anecdotes(message.chat.id)


@bot.message_handler(commands=['stop'])
def show_stats(message):
    chat_id = message.chat.id
    if chat_id not in chat_states.keys():
        bot.send_message(chat_id, 'Сначала надо начать игру, нажав /play',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        return

    if chat_states[chat_id].won % 10 in range(2, 5):
        word_form = 'раза'
    else:
        word_form = 'раз'
    msg = (f'Ты угадал(а) {chat_states[chat_id].won} {word_form} '
           f'и ошибся(лась) {chat_states[chat_id].lost}.')
    bot.send_message(chat_id, msg,
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.send_message(chat_id, 'Чтобы сыграть еще раз, нажми /play',
                     reply_markup=telebot.types.ReplyKeyboardRemove())


def draw_keyboard(chat_id, response_text):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                                 resize_keyboard=True,
                                                 one_time_keyboard=True)
    button_continue = telebot.types.KeyboardButton(chr(0x1F60E) +
                                                   'Несите еще!')
    button_stop = telebot.types.KeyboardButton(chr(0x1F645) + 'Хватит')
    keyboard.add(button_continue, button_stop)
    bot.send_message(chat_id, response_text, reply_markup=keyboard)


@bot.message_handler(func=lambda x: 'первый' in x.text.lower())
def first_is_chosen(message):
    global chat_states
    try:
        first_likes = chat_states[message.chat.id].last_anecs[0].likes
        second_likes = chat_states[message.chat.id].last_anecs[1].likes
    except KeyError:
        bot.reply_to(message, 'Что-то пошло не так. Нажмите /play еще раз',
                     reply_markup=telebot.types.ReplyKeyboardRemove())
        return
    if first_likes >= second_likes:
        chat_states[message.chat.id].won += 1
        response_text = (f'Верно! Первый анек набрал {first_likes} лайков, '
                         f'а второй – {second_likes}')
    else:
        chat_states[message.chat.id].lost += 1
        response_text = (f'Не-а. Первый анек набрал {first_likes} лайков, '
                         f'а второй – {second_likes}')
    
    draw_keyboard(message.chat.id, response_text)


@bot.message_handler(func=lambda x: 'второй' in x.text.lower())
def second_is_chosen(message):
    global chat_states
    try:
        first_likes = chat_states[message.chat.id].last_anecs[0].likes
        second_likes = chat_states[message.chat.id].last_anecs[1].likes
    except KeyError:
        bot.reply_to(message, 'Что-то пошло не так. Нажмите /play еще раз',
                     reply_markup=telebot.types.ReplyKeyboardRemove())
        return None
    if second_likes >= first_likes:
        chat_states[message.chat.id].won += 1
        response_text = (f'Верно! Второй анек набрал {second_likes} лайков, '
                         f'а первый – {first_likes}')
    else:
        chat_states[message.chat.id].lost += 1
        response_text = (f'Не-а. Второй анек набрал {second_likes} лайков, '
                         f'а первый – {first_likes}')

    draw_keyboard(message.chat.id, response_text)


@bot.message_handler(func=lambda x:
                     x.text == chr(0x1F612) + 'Что-то из этого вообще не анек')
def not_anec(message):
    bot.send_message(message.chat.id, 'Ок, вот другие посты!',
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    send_anecdotes(message.chat.id)


@bot.message_handler(func=lambda x: 'еще' in x.text.lower.replace('ё', 'е'))
def more_anecs(message):
    send_anecdotes(message.chat.id)


@bot.message_handler(func=lambda x: 'хватит' in x.text.lower())
def enough(message):
    show_stats(message)


def main():
    db.connect()
    try:
        bot.polling()
    finally:
        db.close()


if __name__ == '__main__':
    main()
