from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
import sys
import fileinput



# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

ADD = range(1)

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='/link, чтобы получить ссылку')


def kol(bot, update):
    f = open("file.txt", 'r')
    lines = f.readlines()
    bot.sendMessage(update.message.chat_id, text='Количество ссылок в базе сейчас: ' + str(len(lines)))
    f.close()


def link(bot, update):
    f = open("file.txt", 'r')
    lines = f.readlines()
    kol = len(lines)
    f.close()
    if kol == 0:
        bot.sendMessage(update.message.chat_id, text='Недостаточно ссылок, ожидайте пополнения базы')
    else:
        f = open("file.txt", 'r')
        lines = f.readlines()[0]
        bot.send_message(update.message.chat_id, lines)
        f.close()
        for line_number, line in enumerate(fileinput.input('file.txt', inplace=1)):
            if line_number == 0:
                continue
            else:
                sys.stdout.write(line)
        bot.sendMessage(update.message.chat_id, text='Напиши /link, если захочешь получить ссылку')

def add(bot, update):
    return ADD

def add_in_file(bot, update):
    text = update.message.text
    add_file = open('file.txt', 'a')
    f = open('file.txt', 'r')
    lines = f.readlines()
    kol = len(lines)
    if kol != 0:
        add_file.write('\n' + text)
    else:
        add_file.write(text)    
    add_file.close()
    f.close()
    bot.sendMessage(update.message.chat_id, text='Напиши /add, если понадобится добавить ссылки; /kol, чтобы узнать количство ссылок')

def cancel(bot, update):
    bot.sendMessage(update.message.chat_id, text='Что-то пошло не так')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("470924108:AAG8wP-6sVIjJQ6juHiOtcfFDodpdHjEA08")
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add)],

        states={

            ADD: [MessageHandler(Filters.text, add_in_file)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )


    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("kol", kol))
    dp.add_handler(CommandHandler("link", link))
    dp.add_handler(conv_handler)

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

