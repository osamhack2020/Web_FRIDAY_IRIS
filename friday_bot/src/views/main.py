from bot import bot, download_path, MYTOKEN
import os
import telebot
import logging
from models.register import available_password, available_group_name, get_user_cafeteria_id, add_group, add_group_user
from models.eatlog import check_uneater, find_chat_id, set_chat_id, find_member_id, find_mid_at_map, find_member_name
from datetime import datetime
import json
import requests
sess = {} # 얘를 bot에 빼도 괜찮을 듯

def check_password(message):
    chat_id = message.chat.id
    if available_password(chat_id, message.text):
        sess[str(chat_id)] = {"last_login":datetime.now().strftime("%Y%m%d %H:%M")}
        bot.send_message(chat_id, json.dumps(sess))
        show_available_menu(chat_id)
    else:
        bot.send_message(chat_id, "비밀번호가 일치하는 계정이 없습니다.")
        # markup = telebot.types.ForceReply(selective=False)
        # sent = bot.send_message(chat_id, "비밀번호를 다시 입력해주세요.", reply_markup=markup)
        # bot.register_next_step_handler(sent, check_password)

def show_available_menu(chat_id):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(telebot.types.InlineKeyboardButton(text="인원 정보 등록하기", callback_data="a"))
    markup.add(telebot.types.InlineKeyboardButton(text="메뉴 정보 등록하기", callback_data="b"))
    markup.add(telebot.types.InlineKeyboardButton(text="미 식사자 조회하기", callback_data="c"))
    markup.add(telebot.types.InlineKeyboardButton(text="식수인원 예측하기", callback_data="d"))
    markup.add(telebot.types.InlineKeyboardButton(text="로그 아웃", callback_data="e"))
    
    sent = bot.send_message(chat_id, "무엇을 하시겠습니까?", reply_markup = markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_menu(call):
    chat_id = call.message.chat.id
    if call.message and call.data.isalpha():
        if call.data == "a":
            req_group(chat_id)
        if call.data == "c":
            report_uneater(chat_id)
        elif call.data == "e":
            logout(chat_id)
    elif call.message and call.data.isdigit():
        send_alert(chat_id)

def send_alert(chat_id):
    mid = find_mid_at_map(chat_id)
    name = find_member_name(mid)
    bot.send_message(chat_id, "{}님 식사하실 시간 입니다.".format(name))

def report_uneater(chat_id):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    l = check_uneater(1)
    for i, name in enumerate(l):
        mid = find_member_id(name)
        markup.add(telebot.types.InlineKeyboardButton(text=name, callback_data=mid))
    sent = bot.send_message(chat_id, "버튼을 누르면 식사 권유 메시지를 보냅니다.", reply_markup = markup)

def req_group(chat_id):
    if str(chat_id) not in sess:
        bot.send_message(chat_id, "로그인 후 이용해주세요")
    else:
        bot.send_message(chat_id, "인원 정보 파일을 보내주세요")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if str(message.chat.id) not in sess:
        bot.send_message(message.chat.id, "로그인 후 이용해주세요")
        return
    file_name, server_file_path = message.document.file_name, bot.get_file(message.document.file_id).file_path
    with open(os.path.join(download_path, file_name.replace(' ', '-')), "w+b") as f:
        res = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(MYTOKEN, server_file_path))
        f.write(res.content)
    bot.send_message(message.chat.id, "파일을 성공적으로 받았습니다.")
    bot.send_message(message.chat.id, "파일 등록을 시작합니다. 최대 2~3분 걸릴 수 있습니다.")
    reply_after_parse(message.chat.id, file_name)

def reply_after_parse(chat_id, file_name):
    c = get_user_cafeteria_id(chat_id)
    with open(os.path.join(download_path,file_name)) as f:
        cont = f.readlines()
    for ct in cont:
        g, m, k = ct.replace('\n', '').split(',')
        if not available_group_name(c, g):
            add_group(c, g)
        add_group_user(g, m, k)
    bot.send_message(chat_id, "등록을 완료하였습니다")

@bot.message_handler(commands=['conn_group'])
def send_ur_chat_id(message):
    chat_id = message.chat.id
    usr_name = message.chat.first_name + message.chat.last_name
    mid = find_member_id(usr_name)
    set_chat_id(chat_id, mid)
    bot.send_message(chat_id, "등록이 완료되었습니다.")

def logout(chat_id):
    sess.pop(str(chat_id))
    bot.send_message(chat_id, "로그아웃 완료")