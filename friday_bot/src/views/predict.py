from bot import bot, download_path, MYTOKEN, sess, file_handle_pool
import os
import telebot
from datetime import datetime
import json
import requests as req
import pandas as pd

def predict(chat_id):
    res = req.get("http://dl_core:5000/predict")
    bot.send_message(chat_id, res.text)