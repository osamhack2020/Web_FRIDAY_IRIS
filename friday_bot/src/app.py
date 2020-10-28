from bot import bot
import telebot
import requests
import os
import logging
from models.register import available_register_code, set_user_info
from views.register import check_register_code
from models.models import init_db
init_db()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

cur_path = os.path.dirname(os.path.abspath(__file__))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id # for untact session
    usr_name = message.chat.username
    if not usr_name:
        usr_name = message.chat.first_name + message.chat.last_name
    bot.send_message(chat_id, "안녕하세여 {}님 무엇을 도와 드릴까요?".format(usr_name))

@bot.message_handler(commands=['register'])
def register(message):
    chat_id = message.chat.id
    markup = telebot.types.ForceReply(selective=False)
    sent = bot.send_message(chat_id, "회원가입 인가 코드를 입력해주세요.", reply_markup=markup)
    bot.register_next_step_handler(sent, check_register_code)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    file_name, server_file_path = message.document.file_name, bot.get_file(message.document.file_id).file_path
    with open(os.path.join(cur_path, file_name.replace(' ', '-')), "wb") as f:
        res = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(MYTOKEN, server_file_path))
        f.write(res.content)

if __name__ == "__main__":
    bot.polling()
