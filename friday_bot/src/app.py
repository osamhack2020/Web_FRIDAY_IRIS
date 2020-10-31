from bot import bot, file_handle_pool, MYTOKEN, sess, download_path, logger
import telebot
from views.register import check_register_code
from views.main import check_password, reply_after_parse_g, req_file
from views.menuinfo import reply_after_parse_m, reply_after_parse_mi
from models.models import init_db
import os
import requests
init_db()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id # for untact session
    usr_name = message.chat.username
    if not usr_name:
        usr_name = message.chat.first_name + message.chat.last_name
    bot.send_message(chat_id, "안녕하세여 {}님 무엇을 도와 드릴까요?".format(usr_name))
    bot.send_message(chat_id, "'/'를 치시면 사용가능한 명령어가 나옵니다.")
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

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    chat_id = message.chat.id
    if str(chat_id) not in sess:
        bot.send_message(chat_id, "로그인 후 이용해주세요")
        return
    file_name, server_file_path = message.document.file_name, bot.get_file(message.document.file_id).file_path
    with open(os.path.join(download_path, file_name.replace(' ', '-')), "w+b") as f:
        res = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(MYTOKEN, server_file_path))
        f.write(res.content)
    bot.send_message(chat_id, "파일을 성공적으로 받았습니다.")
    bot.send_message(chat_id, "파일 등록을 시작합니다. 최대 2~3분 걸릴 수 있습니다.")
    if len(file_handle_pool) > 0:   
        if file_handle_pool[0] == "set_group":
            reply_after_parse_g(chat_id, file_name)
            file_handle_pool.remove("set_group")
        elif file_handle_pool[0] == "set_menu":
            reply_after_parse_m(chat_id, file_name)
            file_handle_pool.remove("set_menu")
        elif file_handle_pool[0] == "set_menu_info":
            reply_after_parse_mi(chat_id, file_name)
            file_handle_pool.remove("set_menu_info")
            file_handle_pool.append("set_menu")
            req_file(chat_id)
        
@bot.message_handler(commands=['hide'])
def command_hide(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.chat.id, "⌨💤...", reply_markup=hide_markup)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    bot.polling()
