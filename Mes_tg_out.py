from telebot import TeleBot, types
bot = TeleBot('5887488636:AAEVw-vAIsv_1ShV7f0qbYJdj_mnkW7zk3w')

def format_message(chat_id, text):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    choose_a_lawyer = types.InlineKeyboardButton(text = 'Choose a lawyer', callback_data="lawyer")
    thank_you = types.InlineKeyboardButton(text = 'Thank you!', callback_data="thank")
    do_not_understand = types.InlineKeyboardButton(text = 'Not clear', callback_data="under")
    legal_position = types.InlineKeyboardButton(text = 'Used legal position', callback_data="legal")
    keyboard.add(choose_a_lawyer, thank_you, do_not_understand,legal_position)

    bot.send_message(chat_id, text, reply_markup=keyboard)

