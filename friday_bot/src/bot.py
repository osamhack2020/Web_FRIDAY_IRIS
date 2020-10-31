import telebot
from secret import token
import os
MYTOKEN = token
bot = telebot.TeleBot(MYTOKEN)
cur_path = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists('downloads'):
    os.makedirs('downloads')
download_path = os.path.join(cur_path, 'downloads')
sess = {}
file_handle_pool = []
loc_handle_pool = []