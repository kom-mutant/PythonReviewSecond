import config
import telebot
import requests
import parserbystayer

TOKEN = "1729021146:AAF6RPtBZnvmniwpsayFzrcjVsxQ7J2yZ8k"
abot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['get_news'])
def get_news(message):
    bot.send_message(new_docs(5))

@bot.message_handler(commands=['get_topics'])
def get_topics(message):
    bot.send_message(new_topics(5))


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
