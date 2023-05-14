from telebot import TeleBot
import Use_in
from main import get_last_query_data

# створення бота
bot = TeleBot('5887488636:AAEVw-vAIsv_1ShV7f0qbYJdj_mnkW7zk3w')

#функція для повернення команди 
@bot.message_handler(commands=['start'])
def main(message):
    text = """
    Вітаю, це ZakonHelper bot!
Я Ваш особистий помічник у юридичних питаннях. За допомогою ресурсу zakononline.com.ua знаю судову практику та законодавство. 
Опишіть ситуацію, на яку шукаєте відповідь, і ми разом знайдемо рішення.
"""
    bot.send_message(message.chat.id, text)

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    data = callback.data.split(":")
    if data[0] == 'lawyer':
        bot.send_message(callback.message.chat.id, "Ми почали підбір, зв'яжемся з Вами.")
    elif data[0] == 'thank':
        bot.send_message(callback.message.chat.id, "Раді допомогти")
    elif data[0] == 'under':
        bot.send_message(callback.message.chat.id, "Ми вже працюємо над покращенням")
    elif data[0] == 'legal':
        lists = get_last_query_data()
        text = ""
        for list in lists:
            text = text + f"{list['url']}\n"
        bot.send_message(callback.message.chat.id, text)


@bot.message_handler(func=lambda message: True)
def message(message):
    Use_in.use_in(message.chat.id, message.text)

#    print (text , messenger_channel_id)

bot.polling(skip_pending= True)

