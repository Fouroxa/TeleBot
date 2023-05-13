from credits import token
import telebot
import wikipedia
import requests



wikipedia.set_lang('ru')

token = token
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def command_start(message):
    bot.reply_to(message, "Hello, world!")


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.reply_to(message, "Важная информация!!")


@bot.message_handler(commands=['whoayou'])
def command_whoayou(message):
    message_user = message.from_user
    bot.reply_to(message, message_user.full_name)


@bot.message_handler(commands=["wiki"])
def wiki(message):
    bot.reply_to(message, "Отправьте мне любое слово, и я найду его значение на Wikipedia")


def get_wiki(heading):
    try:
        ny = wikipedia.page(heading)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split(".")
        wikimas = wikimas[:-1]
        wikitext2 = " ".join(wikimas)
        return wikitext2
    except wikipedia.exceptions.PageError:
        return "В энциклопедии нет информация об этом."


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.reply_to(message, get_wiki(message.text))
    bot.reply_to(message,
                 f"\n Более подробную информацию вы можете узнать здесь {wikipedia.page(message.text).url}")


@bot.message_handler(commands=["weather"])
def command_weather(message):
    bot.reply_to(message, "Weather is fine!!" )


bot.polling(non_stop=True)

