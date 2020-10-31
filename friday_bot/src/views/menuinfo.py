from bot import bot, download_path, MYTOKEN, sess
import os
import telebot
from models.menuinfo import set_daily_menu, set_menu_info
from models.mealtime import find_date_id, set_date_id
from models.register import get_user_cafeteria_id
from datetime import datetime
import json
import requests
import pandas as pd

def reply_after_parse_m(chat_id, file_name):
    c_id = get_user_cafeteria_id(chat_id)
    df = pd.read_excel(os.path.join(download_path,file_name))
    menu_dict = df.fillna('').to_dict(orient='list')
    for date in menu_dict:
        date_id = find_date_id(date)
        if date_id == -1:
            set_date_id(date)
            date_id = find_date_id(date)
        for menu in menu_dict[date]:
            if menu:
                set_daily_menu(date_id, c_id, menu)
    bot.send_message(chat_id, "등록을 완료하였습니다")

def reply_after_parse_mi(chat_id, file_name):
    df = pd.read_excel(os.path.join(download_path,file_name))
    menu_dict = df.fillna('').to_dict(orient='list')
    for menu_name in menu_dict:
        info_serial = ",".join([i for i in menu_dict[menu_name] if i])
        set_menu_info(menu_name, info_serial)
    bot.send_message(chat_id, "등록을 완료하였습니다") 