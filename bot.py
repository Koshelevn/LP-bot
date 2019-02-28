from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import config
import ephem
import datetime
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('bot.log', 'w+', 'utf-8')] 
                    )

def greet_user(bot, update):
	text = "Вызван /start"
	logging.info(text)
	update.message.reply_text(text)

def get_constellation(bot, update):
	planet = update.message.text.split(" ")[1]
	try:
		func = getattr(ephem, planet)
		text = f"Поиск созвездия планеты {planet}"
		update.message.reply_text(ephem.constellation(func(datetime.datetime.now()))[1])
	except AttributeError:
		update.message.reply_text("Не такой планеты в ephem")
	except TypeError:
		update.message.reply_text("Сломать меня пытаешься?")
	

def talk_to_me(bot, update):
	user_text = "Привет {}! Ты написал {}".format(update.message.chat.first_name, update.message.text)
	logging.info("User: %s, Chat id %s, Message %s", update.message.chat.username, update.message.chat.id, update.message.text)
	update.message.reply_text(user_text)	

def main():
	mybot = Updater(config.API, request_kwargs = config.PROXY)
	logging.info('Бот запускается')
	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))
	dp.add_handler(CommandHandler("planet", get_constellation))
	mybot.start_polling()
	mybot.idle()


if __name__ == '__main__':
	main()