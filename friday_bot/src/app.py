from bot import bot
import telebot
import logging
from views.register import check_register_code
from views.main import check_password
from models.models import init_db
init_db()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

@bot.message_handler(commands=['login'])
def login(message):
    chat_id = message.chat.id
    markup = telebot.types.ForceReply(selective=False)
    sent = bot.send_message(chat_id, "비밀번호를 입력해주세요.", reply_markup=markup)
    bot.register_next_step_handler(sent, check_password)

@bot.message_handler(commands=['hide'])
def command_hide(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.chat.id, "⌨💤...", reply_markup=hide_markup)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    bot.polling()
