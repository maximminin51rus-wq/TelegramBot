import telebot
import random
import os

# Вставь свой токен
TOKEN = 'ТВОЙ_ТОКЕН_ЗДЕСЬ'
bot = telebot.TeleBot(TOKEN)
FILE_NAME = "games.txt"

def load_games():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

def save_game(game):
    with open(FILE_NAME, "a", encoding="utf-8") as f:
        f.write(game + "\n")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Бот запущен!\n/addgame [название]\n/newgame — выбрать игру\n/list — список\n/clear — ОЧИСТИТЬ ВСЁ")

@bot.message_handler(commands=['addgame'])
def add(message):
    game_name = message.text.replace('/addgame', '').strip()
    if game_name:
        save_game(game_name)
        bot.reply_to(message, f"✅ Игра '{game_name}' добавлена!")
    else:
        bot.reply_to(message, "Напиши название после команды, например: /addgame Doors")

@bot.message_handler(commands=['newgame'])
def pick(message):
    games = load_games()
    if games:
        chosen = random.choice(games)
        bot.send_message(message.chat.id, f"🎲 Сегодня играем в: **{chosen}**", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Список пуст! Добавь игры через /addgame")

@bot.message_handler(commands=['list'])
def show(message):
    games = load_games()
    if games:
        bot.reply_to(message, "Текущий список игр:\n" + "\n".join([f"• {g}" for g in games]))
    else:
        bot.reply_to(message, "Список пока пуст.")

# НОВАЯ КОМАНДА: ОЧИСТКА СПИСКА
@bot.message_handler(commands=['clear'])
def clear_list(message):
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME) # Просто удаляем файл с играми
        bot.reply_to(message, "🗑 Список игр полностью очищен!")
    else:
        bot.reply_to(message, "Список и так пуст.")

bot.polling(none_stop=True)
