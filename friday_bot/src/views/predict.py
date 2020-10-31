from bot import bot, download_path, MYTOKEN, sess, file_handle_pool
import os
import telebot
from datetime import datetime
import json
import requests as req
import pandas as pd
import math

def predict(chat_id):
    res = req.get("http://dl_core:5000/predict")
    res.encoding=None
    # 잘 오는거 확인
    # 이게 방식이 최소 전날 데이터는 받아야할듯?
    # 2일치 데이터는 받고 생각
    # res.text에서 json 데이터 안줬을때 예외처리 생각해야함
    msg = json.loads(res.text)["msg"]
    bot.send_message(chat_id, msg)

