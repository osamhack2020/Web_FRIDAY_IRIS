from bot import bot, loc_handle_pool, file_handle_pool
import os
import telebot
import logging
from models.register import available_register_code, set_user_info, available_cafeteria, add_cafeteria
import math
pool = {}

def grid(v1, v2) :

    RE = 6371.00877 # 지구 반경(km)
    GRID = 5.0      # 격자 간격(km)
    SLAT1 = 30.0    # 투영 위도1(degree)
    SLAT2 = 60.0    # 투영 위도2(degree)
    OLON = 126.0    # 기준점 경도(degree)
    OLAT = 38.0     # 기준점 위도(degree)
    XO = 43         # 기준점 X좌표(GRID)
    YO = 136        # 기1준점 Y좌표(GRID)

    DEGRAD = math.pi / 180.0
    RADDEG = 180.0 / math.pi

    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)
    rs = {}

    ra = math.tan(math.pi * 0.25 + (v1) * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)

    theta = v2 * DEGRAD - olon
    if theta > math.pi :
        theta -= 2.0 * math.pi
    if theta < -math.pi :
        theta += 2.0 * math.pi
    theta *= sn
    rs['x'] = math.floor(ra * math.sin(theta) + XO + 0.5)
    rs['y'] = math.floor(ro - ra * math.cos(theta) + YO + 0.5)

    return int(str(rs["x"]).split('.')[0]), int(str(rs["y"]).split('.')[0])

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
    req_cafeteria_loc(chat_id)

def req_cafeteria_loc(chat_id):
    loc_handle_pool.append("set_cafeteria")
    bot.send_message(chat_id, "해당 식당의 위치 데이터를 보내주세요")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    if len(loc_handle_pool) > 0:
        if loc_handle_pool[0] == "set_cafeteria":
            x, y = grid(message.location.latitude, message.location.longitude)
            bot.send_message(message.chat.id, "x:{0} , y:{1}".format(x,y))
            req_user_authkey(message.chat.id)
    else:
        bot.send_message(message.chat.id, "비 정상 접근입니다.")

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
