from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from django.conf import settings
from .models import Message, Token, CustomUser


def get_telegram_bot(user):
    try:
        token = settings.TELEGRAM_BOT_TOKEN
        return Bot(token)
    except AttributeError:
        raise ValueError("TELEGRAM_BOT_TOKEN is missing in settings.")

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f"Hi {user.first_name}! I'm your bot. Send me a message and I'll echo it back to you.")

def echo(update: Update, context: CallbackContext):
    user = update.effective_user
    message_text = update.message.text

    update.message.reply_text(f"{user.username}, I received a message from you:\n{message_text}")

    user_obj = CustomUser.objects.get(username=user.username)
    Message.objects.create(user=user_obj, body=message_text)

def error(update: Update, context: CallbackContext):
    context.error("Error occurred: %s", context.error)

def telegram_polling():
    bot = get_telegram_bot(None)  

    updater = Updater(bot=bot, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.text & ~filters.command, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    telegram_polling()
