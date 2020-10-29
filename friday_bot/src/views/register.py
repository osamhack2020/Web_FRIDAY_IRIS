from bot import bot
import os
import telebot
import logging
from models.register import available_register_code, set_user_info, available_cafeteria, add_cafeteria

pool = {}

def check_register_code(message):
    chat_id = message.chat.id
    usr_input = message.text
    if available_register_code(usr_input):
        bot.send_message(chat_id, "인증 성공")
        usr_name = message.chat.username
        if not usr_name:
            usr_name = message.chat.first_name + message.chat.last_name
        pool[str(chat_id)] = {}
        req_user_nickname(chat_id, usr_name)
    else:
        bot.send_message(chat_id, "유효하지 않은 코드입니다.")
        markup = telebot.types.ForceReply(selective=False)
        sent = bot.send_message(chat_id, "회원가입 인가 코드를 입력해주세요.", reply_markup=markup)
        bot.register_next_step_handler(sent, check_register_code)

def req_user_nickname(chat_id, cur_name):
    markup = telebot.types.ReplyKeyboardMarkup()
    agree_btn = telebot.types.KeyboardButton('예')
    disagree_btn = telebot.types.KeyboardButton('아니요')
    markup.row(agree_btn, disagree_btn)
    sent = bot.send_message(chat_id, "현재 닉네임을 사용하시겠습니까? {}".format(cur_name), reply_markup=markup)
    bot.register_next_step_handler(sent, switch_nickname_selection)

def switch_nickname_selection(message):
    chat_id = message.chat.id
    if message.text == "예":
        set_user_nickname(message)
    elif message.text == "아니요":
        get_user_nickname(chat_id)
    else:
        pass

def get_user_nickname(chat_id):
    markup = telebot.types.ForceReply(selective=False)
    sent = bot.send_message(chat_id, "사용할 닉네임을 입력해주세요", reply_markup=markup)
    bot.register_next_step_handler(sent, set_user_nickname)

def set_user_nickname(message):
    chat_id = message.chat.id
    usr_name = message.chat.username
    if not usr_name:
        usr_name = message.chat.first_name + message.chat.last_name
    if message.text == "예":
        pool[str(chat_id)]['nickname'] = usr_name
    else:
        pool[str(chat_id)]['nickname'] = message.text
    req_user_cafeteria(chat_id)

def req_user_cafeteria(chat_id):
    markup = telebot.types.ForceReply(selective=False)
    sent = bot.send_message(chat_id, "관리하는 구내식당 이름을 입력해주세요", reply_markup=markup)
    bot.register_next_step_handler(sent, set_user_cafeteria)

def set_user_cafeteria(message):
    chat_id = message.chat.id
    if not available_cafeteria(message.text):
        add_cafeteria(message.text)
    pool[str(chat_id)]['cafeteria'] = message.text
    req_user_authkey(chat_id)

def req_user_authkey(chat_id):
    markup = telebot.types.ForceReply(selective=False)
    sent = bot.send_message(chat_id, "사용하실 비밀번호를 입력해주세요", reply_markup=markup)
    bot.register_next_step_handler(sent, set_user_password)

def set_user_password(message):
    chat_id = message.chat.id
    pool[str(chat_id)]['password'] = message.text
    set_user_info(chat_id, pool[str(chat_id)])
    pool.pop(str(chat_id))
    bot.send_message(chat_id, "회원가입이 완료되었습니다.")
