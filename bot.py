import logging
import json
from telegram import Bot, ParseMode, Update, Poll
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define your bot token
BOT_TOKEN = '7882173382:AAGtuO4Q7qk54Vr6V16yu2bQsrPHzxRpnC8'

# Define the states for the conversation handler
ASK_CHANNEL, ASK_INTERVAL = range(2)

# List of quizzes to send
quizzes = [
    ("What is the capital of France?", ["Paris", "London", "Berlin", "Madrid"], 0),
    ("What is 2 + 2?", ["3", "4", "5", "6"], 1),
    ("What is the largest planet in our Solar System?", ["Earth", "Mars", "Jupiter", "Saturn"], 2)
]

# Dictionary to store user settings
user_settings = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to the Quiz Bot! Please provide the channel ID or username where you want to receive quizzes.')
    return ASK_CHANNEL

def ask_channel(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    channel_id = update.message.text
    user_settings[user_id] = {'channel_id': channel_id}
    update.message.reply_text('Thank you! Now please set the interval (in seconds) at which you want to receive quizzes.')
    return ASK_INTERVAL

def ask_interval(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    interval = int(update.message.text)
    user_settings[user_id]['interval'] = interval
    update.message.reply_text(f'Settings saved! You will receive quizzes in {user_settings[user_id]["channel_id"]} every {interval} seconds.')
    
    # Save user settings to a file
    with open('user_settings.json', 'w') as file:
        json.dump(user_settings, file)

    # Schedule the quiz sending job
    context.job_queue.run_repeating(send_quiz, interval=interval, first=0, context=user_id)
    return ConversationHandler.END

def send_quiz(context: CallbackContext):
    job = context.job
    user_id = job.context
    channel_id = user_settings[user_id]['channel_id']
    quiz = quizzes.pop(0)
    quizzes.append(quiz)
    question, options, correct_option = quiz
    context.bot.send_poll(
        chat_id=channel_id,
        question=question,
        options=options,
        type=Poll.QUIZ,
        correct_option_id=correct_option,
        is_anonymous=False
    )

def main():
    # Load user settings from file
    global user_settings
    try:
        with open('user_settings.json', 'r') as file:
            user_settings = json.load(file)
    except FileNotFoundError:
        user_settings = {}

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ASK_CHANNEL: [MessageHandler(Filters.text & ~Filters.command, ask_channel)],
            ASK_INTERVAL: [MessageHandler(Filters.text & ~Filters.command, ask_interval)]
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)

    try:
        updater.start_polling()
        updater.idle()
    except NetworkError as ne:
        logger.error(f"NetworkError occurred: {ne}")
    except InvalidToken as it:
        logger.error(f"InvalidToken error: {it}")
    except TelegramError as te:
        logger.error(f"TelegramError occurred: {te}")

if __name__ == '__main__':
    main()
