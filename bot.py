import telebot

TOKEN = "5647751734:AAGf0uUjBf1C7NyqOeeMf1UXy4tQfXAZwro"
CHANNEL_ID = "@sscupscquizstore"

bot = telebot.TeleBot(TOKEN)

question = "What is the capital of France?"
options = ["Berlin", "Madrid", "Paris", "Rome"]
correct_option_id = 2  # Index starts from 0

bot.send_poll(
    chat_id=CHANNEL_ID,
    question=question,
    options=options,
    type="quiz",
    correct_option_id=correct_option_id,
    explanation="Paris is the capital of France."
)

bot.polling()
