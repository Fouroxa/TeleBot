from credits import token
import telebot
import wikipedia
import requests
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

state_storage = StateMemoryStorage()


class MyStates(StatesGroup):
    wiki = State()
    weather = State()


wikipedia.set_lang('ru')

token = token
bot = telebot.TeleBot(token, state_storage=state_storage)


def command_start(message):
    bot.reply_to(message, f"Hello, {message.from_user.full_name}!")


def command_help(message):
    bot.reply_to(message, "Важная информация!!\n"
                          "/start Бот выводит приветствие.\n"
                          "/wiki Бот входит в состояние поиска значение слова.\n"
                          "/weather Бот входит в состояние поиска погоды.\n"
                          "/cancel Бот выходит из любого состояния.\n"
                          "Если вы вошли в состояние(wiki, weather) и нашли нужную информация, то чтобы бот вернулся к нормальному режиму, надо использовать команду /cancel")


# def command_whoayou(message):
#     message_user = message.from_user
#     bot.reply_to(message, message_user.full_name)


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


def wiki(message):
    bot.set_state(message.from_user.id, MyStates.wiki, message.chat.id)
    bot.reply_to(message, "Отправьте мне любое слово, и я найду его значение на Wikipedia")


def any_state(message):
    bot.send_message(message.chat.id, "Я вышел из текущего состояния.")
    bot.delete_state(message.from_user.id, message.chat.id)


def handle_text(message):
    bot.reply_to(message, get_wiki(message.text))
    bot.reply_to(message,
                 f"\n Более подробную информацию вы можете узнать здесь {wikipedia.page(message.text).url}")


def get_weather(city):
    response = requests.get(f'https://wttr.in/{city.title()}?format={"Температура: "}+%c+%t\n{"Скорость ветра: "}+%w\n{"Влажность воздуха: "}+%h\n{"Давление: "}+%P')
    return response.text


@bot.message_handler(commands=["weather"])
def weather(message):
    bot.set_state(message.from_user.id, MyStates.weather, message.chat.id)
    bot.reply_to(message, "Отправьте мне город, и я покажу тебе погоду в нем.")

def give_weather(message):
    bot.reply_to(message, get_weather(message.text))



bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.register_message_handler(any_state, state='*', commands=['cancel'])
bot.register_message_handler(wiki, commands=["wiki"])
bot.register_message_handler(weather, commands=["weather"])
bot.register_message_handler(handle_text, state=MyStates.wiki, content_types=["text"])
bot.register_message_handler(give_weather, state=MyStates.weather, content_types=['text'])
bot.register_message_handler(command_start, commands=["start"])
bot.register_message_handler(command_help, commands=['help'])
# bot.register_message_handler(command_whoayou, commands=['whoayou'])
bot.polling(non_stop=True)
