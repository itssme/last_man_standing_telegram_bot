from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import random as r
import time   as t
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, message
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

users = []
running = False

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text("already started")

def help(bot, update):
    update.message.reply_text("Help:\n/add_me  to add yourself to the players list\n/new_round  to star the round\nGamerules:\n1. If your number is grater than 90 you will get kicked\n2. If the number 88 appears 2 times I will leave")

def echo(bot, update):
    pass

def add_me(bot, update):
    global users
    print("added")

    alread_in = False
    for i in range(0, len(users)):
        if (update.message.from_user.first_name == users[i][0] and update.message.from_user.id == users[i][1]):
            alread_in = True

    if (alread_in):
        print("Did not add user " + update.message.from_user.first_name + " alread added")
    else:
        users.append((update.message.from_user.first_name, update.message.from_user.id))
        print("Did add user " + update.message.from_user.first_name)
        update.message.reply_text("added user " + update.message.from_user.first_name)

def new_round(bot, update):
    global users
    global running

    if (not running):
        try:
            running = True
            chat_id_l = update.message.chat.id
            Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str("Lets start a new round!"))

            random_num = []
            print("starting new round")
            print(users)

            while len(users) > 1:
                try:
                    t.sleep(5)
                    random_num = []
                    msg = ""
                    for i in range(0, len(users)):
                        random_num.append(r.randint(0,100))

                    for i in range(0, len(users)):
                        msg += str(random_num[i]) + " -> " + users[i][0] + "\n"

                    Bot.sendMessage(bot, chat_id=update.message.chat.id, text=msg)

                    _88_times = 0

                    for i in range(0, len(users)):
                        if (random_num[i] > 90):
                            Bot.kick_chat_member(bot, chat_id=chat_id_l, user_id=users[i][1])
                            users.remove(users[i])
                        elif (random_num[i] == 88):
                            _88_times += 1

                    if (_88_times >= 2):
                        Bot.leave_chat(bot, chat_id=update.message.chat.id)

                    print(users)
                except:
                    print("[!] ignoring error in new round")

            Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str("The round is finished!\nWho is the last man standing?"))
            running = False
            users = []
        except:
            running = False
            print("Error in new round")


def uff(bot, update):
    pass # TODO: make something cool here


def echo(bot, update):
    if (update.message.text.lower() == "uff"):
        uff(bot, update)



def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("your bot token") # add your bot token here

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("new_round", new_round))
    dp.add_handler(CommandHandler("add_me", add_me))
    dp.add_handler(CommandHandler("uff", uff))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
