from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import config
import ephem
import datetime
import re
import csv

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('bot.log', 'w+', 'utf-8')] 
                    )
cities_players = {}

def greet_user(bot, update):
	text = "Вызван /start"
	logging.info(text)
	update.message.reply_text(text)

def get_constellation(bot, update):
	planet = update.message.text.split(" ")[1]
	try:
		func = getattr(ephem, planet)
		date_cons = func(datetime.datetime.now())
		update.message.reply_text(ephem.constellation(date_cons)[1])
	except AttributeError:
		update.message.reply_text("Не такой планеты в ephem")
	except TypeError:
		update.message.reply_text("Сломать меня пытаешься?")
	

def talk_to_me(bot, update):
	user_text = "Привет {}! Ты написал {}".format(update.message.chat.first_name, update.message.text)
	logging.info("User: %s, Chat id %s, Message %s", update.message.chat.username, update.message.chat.id, update.message.text)
	update.message.reply_text(user_text)	


def wordcount(bot, update):
	if not update.message.text:
		update.message.reply_text(f"{update.message.chat.first_name}, и что тут считать?")
	else:
		word_amount = re.findall('\w+', update.message.text)
		update.message.reply_text(f"{update.message.chat.first_name}, в твоем сообщении {len(word_amount)-1} слов()")

def full_moon(bot, update):
	user_date = update.message.text.split(" ")[1]
	try:
		answer = ephem.next_full_moon(user_date)
		update.message.reply_text(answer)
	except ValueError:
		update.message.reply_text("Даты выглядят так 'год-месяц-день'")


def cities(bot, update):
	if not update.message.chat.username in cities_players:
		with open('cities.csv', 'r', encoding="utf-8") as f:
			reader = csv.reader(f, delimiter = ";")
			cities_players[update.message.chat.username] = list(reader)[0]
	cities_left = cities_players[update.message.chat.username]
	user_city = update.message.text.split(" ")[1].lower()
	if user_city in cities_left:
		for city in cities_left:
			logging.info(f"{user_city} и {city}")
			if user_city[-1:] == city[0]:
				update.message.reply_text(f"{city.capitalize()}, ваш ход")
				cities_left.remove(city)
				cities_left.remove(user_city)
				break
		else:
			update.message.reply_text(f"{update.message.chat.first_name}, я сдаюсь")
			del cities_players[update.message.chat.username]
	else:
		update.message.reply_text(f"{update.message.chat.first_name}, не знаю такого города или он уже был в игре, попробуйте еще раз.")
		
	
def calc(bot, update):
	expression = update.message.text[5:]
	no_letters_expression = ''.join(filter(lambda x: not x.isalpha(), expression))
	print(expression)
	print(no_letters_expression)
	if expression == no_letters_expression:
		update.message.reply_text(eval(expression))
	else:
		update.message.reply_text("Что это за буквы?")
	

def main():
	mybot = Updater(config.API, request_kwargs = config.PROXY)
	logging.info('Бот запускается')
	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))
	dp.add_handler(CommandHandler("planet", get_constellation))
	dp.add_handler(CommandHandler(("wordcount"), wordcount))
	dp.add_handler(CommandHandler(("next_full_moon"), full_moon))
	dp.add_handler(CommandHandler(("cities"), cities))
	dp.add_handler(CommandHandler(("calc"), calc))
	mybot.start_polling()
	mybot.idle()


if __name__ == '__main__':
	main()