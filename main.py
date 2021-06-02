import telebot

from interactive_conditional_samples import interact_model

bot = telebot.TeleBot('1389288964:AAED1oFsgrBK_TTcXJAKC53lc3y65kAQQJg')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    answer_text = " ".join(message.text.lower().split()[:-1])
    bot.send_message(message.from_user.id, interact_model(input_text=answer_text, length=int(message.text.split()[-1])))

def main():
    global bot
    bot.polling(none_stop=True, interval=0)

if __name__ == "__main__":
    main()