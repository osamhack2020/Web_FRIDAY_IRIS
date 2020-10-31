from bot import bot, download_path, MYTOKEN, sess, file_handle_pool
import os
import telebot
from datetime import datetime, timedelta
import json
import requests as req
import pandas as pd
import math
from models.mealtime import get_date_id, set_date_id
from models.eatlog import find_cafeteria_id
def predict(chat_id):
    # 가능한 시간 now 기점 12시간 
    predict_date, h = datetime.now().strftime("%Y%m%d %H").split()
    if int(h) < 9:
        predict_h = "0900"
    elif int(h) < 12:
        predict_h = "1200"
    elif int(h) < 18:
        predict_h = "1800"
    else:
        predict_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
        predict_h = "0900"
    predict_map = {"0900":"breakfast", "1200":"lunch", "1800":"dinner"}
    _id = get_date_id(predict_date, predict_map[predict_h])
    if not _id:
        set_date_id(predict_date + "_" + predict_map[predict_h])
        _id = get_date_id(predict_date, predict_map[predict_h])
    params = {
        "pd_id": _id,
        "c_id": find_cafeteria_id(chat_id),
        "o_cnt": 45,
        "additional_h": 0
    }
    res = req.get("http://dl_core:5000/predict", params=params)
    res.encoding=None
    # 잘 오는거 확인
    # 이게 방식이 최소 전날 데이터는 받아야할듯?
    # 2일치 데이터는 받고 생각
    # res.text에서 json 데이터 안줬을때 예외처리 생각해야함
    res = json.loads(res.text)
    if res["status"] == "ok":
        bot.send_message(chat_id, res["msg"])
    elif res["status"] == "error":
        bot.send_message(chat_id, res["msg"])   