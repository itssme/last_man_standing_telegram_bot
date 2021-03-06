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
    update.message.reply_text("Help:\n/add_me  to add yourself to the players list\n/new_round  to star the round\nGamerules:\n1. If your number is grater than 90 you will get kicked\n2. If the number 88 appears 2 times I will leave\n/battle for a 1 vs 1 battle")

def add_me(bot, update):
    global users
    print("added")

    alread_in = False
    for i in range(0, len(users)):
        if (update.message.from_user.first_name == users[i][0] and update.message.from_user.id == users[i][1]):
            alread_in = True

    if (alread_in):
        print("[!] did not add user " + update.message.from_user.first_name + " alread added")
    else:
        users.append((update.message.from_user.first_name, update.message.from_user.id))
        print("[!] did add user " + update.message.from_user.first_name)
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
            print("[!] starting new round")
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
            print("[!] error in new round (quit)")

def battle(bot, update):
    # a 1v1 battle!
    global users

    try:
        if (len(users) == 2):
            Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str(users[0][0] + " and " + users[1][0] + " are playing against each other!"))
            t.sleep(2)
            Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str("Whoever gets the higher number 3 times in a row wins!"))

            won = False
            player_1_wins = 0
            player_2_wins = 0
            need_wins = 3

            while (not won):
                t.sleep(3)

                for i in range(0, r.randint(10, 200)):
                    player_1 = r.randint(0, 100)
                    player_2 = r.randint(0, 100)

                Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str("The numbers are:\n" + users[0][0] + " -> " + str(player_1) + "\n" + users[1][0] + " -> " + str(player_2)))

                if (player_1 == player_2):
                    Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str("There was no winner this round\nNow you will have to get 4 numbers in a row!"))
                    need_wins += 1
                    player_1_wins = 0
                    player_2_wins = 0

                elif (player_1 > player_2):
                    player_1_wins += 1
                    player_2_wins = 0
                    Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str(users[0][0] + " won this turn! " + str(need_wins - player_1_wins) + " wins to go\n"))
                else:
                    player_2_wins += 1
                    player_1_wins = 0
                    Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str(users[1][0] + " won this turn! " + str(need_wins - player_2_wins) + " wins to go\n"))

                if (player_1_wins == need_wins):
                    won = True
                    Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str(users[0][0] + " wins the battle"))
                elif (player_2_wins == need_wins):
                    won = True
                    Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str(users[1][0] + " wins the battle"))
                else:
                    print("no winner yet")

                print("one turn")
    except:
        print("[!] error exiting the battle")
        users = []

    users = []


def uff(bot, update):

    go = r.randint(0,100)

    if (go > 80):
        print("go " + str(go))
        Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str("The uff has happened\nThe bot will roll a number between 0 and 100\nIf the number is greater than 75 you will get kicked!"))

        for i in range(10, r.randint(20, 100)):
            go = r.randint(0,100)

        t.sleep(4)
        Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str("The number is " + str(go)))

        if (go > 75):
            Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str("Enjoy your kick :P"))
            t.sleep(2)
            Bot.kick_chat_member(bot, chat_id=update.message.chat.id, user_id=update.message.from_user.id)
        else:
            Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str("You had luck this time"))

    Bot.sendMessage(bot, chat_id=update.message.chat.id, text=str("The uff has not happened"))

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
    dp.add_handler(CommandHandler("battle", battle))

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
