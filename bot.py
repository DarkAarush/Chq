import telebot

TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "@your_channel_username"

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
