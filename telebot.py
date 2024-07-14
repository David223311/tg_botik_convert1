import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=('start', 'help'))
def help(message: telebot.types.Message):
    text = 'Привет! Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты цену которой хотите узнать>\
    <имя валюты в которой надо узнать цену первой валюты>\
    <количество первой валюты>\n Увидеть список всех доступных валют: /values'

    bot.reply_to(message, text)

    @bot.message_handler(commands=['values'])
    def values(message: telebot.types.Message):
        text = 'Доступные валюты:'
        for key in keys.keys():
            text = '\n'.join((
                text,
                key,
            ))
        bot.reply_to(message, text)

    @bot.message_handler(content_types=[
        'text',
    ])
    def convert(message: telebot.types.Message):
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException(
                'Слишком много параметров. Попробуйте исправить свой запрос')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)

        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.reply_to(message.chat.id, text)

    bot.polling(none_stop=True)
