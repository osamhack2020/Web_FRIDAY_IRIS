from bot import bot, download_path, MYTOKEN, sess
import os
import telebot
from models.menuinfo import set_daily_menu
from models.mealtime import find_date_id, set_date_id
from datetime import datetime
import json
import requests
import pandas as pd

def reply_after_parse_m(chat_id, file_name):
    df = pd.read_excel(os.path.join(download_path,file_name))
    menu_dict = df.fillna('').to_dict(orient='list')
    for date in menu_dict:
        date_id = find_date_id(date)
        if date_id == -1:
            set_date_id(date)
            date_id = find_date_id(date)
        for menu in menu_dict[date]:
            if menu:
                bot.send_message(chat_id, "{0} / {1}".format(date_id, menu))
                set_daily_menu(date_id, menu)
    bot.send_message(chat_id, "등록을 완료하였습니다")