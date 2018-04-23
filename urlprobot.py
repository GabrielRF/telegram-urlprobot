import telebot
import time
import urllib
import unshortenit
import requests
import sys
import configparser
from pyshorteners import Shortener
from telebot import types

config = configparser.ConfigParser()
config.sections()
config.read('urlprobot.conf')

min_url_size = config['DEFAULTS']['min_url_size']
bot = telebot.TeleBot(config['DEFAULTS']['bot_token'])
bitly_token = config['DEFAULTS']['bitly']

def url_shortener(text):
    try:
        shortener = Shortener('Bitly', bitly_token=bitly_token)
        print(urllib.parse.quote_plus(text))
        return shortener.short(text)
    except:
        response = requests.get('http://tinyurl.com/api-create.php?url=' + text)
        return response.content.decode('utf-8')

def url_expander(url):
    unshortened_uri,status = unshortenit.unshorten(url)
    return unshortened_uri

opt98 = types.InlineQueryResultArticle('opt98', 'Type a valid url', 'Waiting...')
opt99 = types.InlineQueryResultArticle('opt99', 'Invalid url. Try with http://', 'Error')

## INLINE_QUERIES
## CPU Load too high. Need to be fixed 
# @bot.inline_handler(func=lambda m: True)
# def query_text(inline_query):
#     try:
#         if len(inline_query.query) <= min_url_size:
#             answer = [opt98]
#         else:
#             response = requests.get(inline_query.query)
#             if response.status_code == 200 and len(inline_query.query) > min_url_size:
#                 long_url = url_expander(inline_query.query)
#                 short_url = url_shortener(inline_query.query)
#                 opt1 = types.InlineQueryResultArticle('opt1', 'Long url', long_url, url=long_url)
#                 opt2 = types.InlineQueryResultArticle('opt2', 'Short url', short_url, url=short_url, disable_web_page_preview=True)
#                 if long_url in inline_query.query.split('?')[0].split('://')[1]:
#                     answer = [opt2]
#                 else:
#                     answer = [opt1, opt2]
#             else:
#                 answer = [opt99]
#
#         bot.answer_inline_query(inline_query.id, answer)
#     except requests.exceptions.MissingSchema:
#         answer = [opt99]
#         bot.answer_inline_query(inline_query.id, answer)
#     except requests.exceptions.InvalidSchema:
#         answer = [opt99]
#         bot.answer_inline_query(inline_query.id, answer)
#     except urllib.error.HTTPError:
#         pass
#     except Exception as e:
#         print(e)
#         pass

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome!\nText me a link.\n\nRate the bot:\nhttps://telegram.me/storebot?start=UrlProBot")

@bot.message_handler(commands=['info'])
def send_welcome(message):
    info = ('This bot is under constant development!\n'
        'If you have any question or suggestion,\n'
        'please, talk to me!\nTwitter: GabRF\n'
        'Telegram: @GabrielRF\n'
        'Website: http://gabrf.com\n'
        '\nRate the bot:\nhttps://telegram.me/storebot?start=UrlProBot'
        '\nSupport the project:\nhttp://grf.xyz/paypal'
        '\n\nThis bot is now open-source:'
        '\nhttps://github.com/GabrielRF/telegram-urlprobot')
    bot.reply_to(message, info)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_chat_action(message.chat.id, 'typing')
    print(message.from_user.id)
    try:
        response = requests.get(message.text)
        if response.status_code == 200:
            url = url_expander(message.text)
            bot.reply_to(message, 'Long url:\n'+ url_expander(url) + '\nShort url:\n' + url_shortener(url), disable_web_page_preview=True)
    except requests.exceptions.MissingSchema:
        bot.reply_to(message, 'Please, send me a valid link.\nhttp:// might be necessary.')
    except requests.exceptions.InvalidSchema:
        bot.reply_to(message, 'Please, send me a valid link.\nhttp:// might be necessary.')

bot.polling(none_stop=True)
