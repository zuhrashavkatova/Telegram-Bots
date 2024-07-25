# import random
# import time
# import sqlite3
#
# import telebot
# from nltk import chat
# from telebot import types
#
# # Initialize the bot
# bot = telebot.TeleBot("6837439077:AAGaEwhRZCEuN6UGgIF8KKQkNG-DxemOvJg")
#
# # Database connection
# conn = sqlite3.connect("rps_game_data.db")
# cursor = conn.cursor()
#
# # Create table if not exists
# cursor.execute("""CREATE TABLE IF NOT EXISTS game_records (
#     game_no INTEGER PRIMARY KEY AUTOINCREMENT,
#     winner TEXT,
#     time REAL,
#     score_user1 INTEGER,
#     score_user2 INTEGER,
#     user1_id INTEGER,
#     user2_id INTEGER
# )""")
# conn.commit()
#
# # Game modes
# MODE_AI = 1
# MODE_USER = 2
#
# # Game states
# STATE_WAITING = 1
# STATE_PLAYING = 2
# STATE_END = 3
# STATE_WAITING_USER = 4  # Added state for waiting for another player in User vs User mode
#
# # Score band (change to 3 or 5 as desired)
# SCORE_BAND = 5
#
# # Game timer and choice timer (in seconds)
# GAME_TIMER = 30
# CHOICE_TIMER = 5
#
# # Game information
# game_info = {}
#
# # Define game logic function
# def determine_winner(user_choice, bot_choice):
#     if user_choice == bot_choice:
#         return None  # It's a tie
#     elif (user_choice == 1 and bot_choice == 3) or \
#          (user_choice == 2 and bot_choice == 1) or \
#          (user_choice == 3 and bot_choice == 2):
#         return 'user'  # User wins
#     else:
#         return 'bot'  # Bot wins
#
# # Initialize scores
# scores = {}
#
# # Handler for /start command
# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     scores[message.chat.id] = 0  # Initialize scores for new users
#     bot.send_message(message.chat.id, 'Welcome to the Rock-Paper-Scissors game!\n'
#                                       'Choose a mode:\n'
#                                       '1. User vs AI\n'
#                                       '2. User vs User')
#     game_info[message.chat.id] = {'mode': None, 'scores': scores, 'state': STATE_WAITING}
#
# # Handle mode selection
# @bot.message_handler(func=lambda message: True)
# def handle_mode(message):
#     chat_id = message.chat.id
#     if game_info[chat_id]['state'] == STATE_WAITING:
#         try:
#             mode = int(message.text)
#             if mode in [MODE_AI, MODE_USER]:
#                 game_info[chat_id]['mode'] = mode
#                 if mode == MODE_AI:
#                     bot.send_message(chat.id, "Playing against AI. Choose your move:")
#                     start_game(chat_id, MODE_AI)
#                 else:
#                     bot.send_message(chat.id, "Waiting for another player...")
#                     game_info[chat_id]['state'] = STATE_WAITING_USER
#             else:
#                 bot.send_message(chat.id, "Invalid mode. Please choose 1 or 2.")
#         except ValueError:
#             bot.send_message(chat.id, "Invalid mode. Please choose 1 or 2.")
#
# # Handle waiting for user in User vs User mode
# @bot.message_handler(func=lambda message: True)
# def handle_waiting_user(message):
#     chat_id = message.chat.id
#     if game_info[chat_id]['state'] == STATE_WAITING_USER:
#         if message.chat.id not in game_info:  # Second player joined
#             game_info[message.chat.id] = {'mode': MODE_USER, 'scores': {message.chat.id: 0}, 'state': STATE_PLAYING}
#             start_game(chat_id, MODE_USER, list(game_info.keys())[0])  # Pass the first player's chat ID as opponent_id
#
# # Start game logic
# def start_game(chat_id, mode, opponent_id=None):
#     game_info[chat_id]['state'] = STATE_PLAYING
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     keyboard.add("👊 Rock")
#     keyboard.add("📃 Paper")
#     keyboard.add("✂️ Scissors")
#     bot.send_message(chat.id, 'Choose your move:', reply_markup=keyboard)
#
#     # Set timers
#     game_start_time = time.time()
#     choice_deadline = game_start_time + CHOICE_TIMER
#
#     while time.time() < choice_deadline:
#         # Handle user choice
#         @bot.message_handler(func=lambda message: message.chat.id == chat_id)
#         def handle_choice(message):
#             user_choice = message.text.lower()
#             if user_choice in ["rock", "paper", "scissors"]:
#                 # Process user choice and end game
#                 user_choice_num = {"rock": 1, "paper": 2, "scissors": 3}.get(user_choice)
#                 end_game(chat_id, user_choice_num, mode, opponent_id, game_start_time)
#                 return
#
#     # User didn't choose within time limit
#     if game_info[chat_id]['state'] == STATE_PLAYING:
#         bot.send_message(chat_id, "Time's up! You lose by default.")
#         end_game(chat_id, None, mode, opponent_id, game_start_time, user_failed=True)
#
# # End game logic
# def end_game(chat_id, user_choice, mode, opponent_id, game_start_time, user_failed=False):
#     game_info[chat_id]['state'] = STATE_END
#
#     if mode == MODE_AI:
#         bot_choice = random.randint(1, 3)
#         winner = determine_winner(user_choice, bot_choice)
#     else:
#         opponent_choice = game_info[opponent_id]['choice']
#         winner = determine_winner(user_choice, opponent_choice)
#
#     if winner == 'user':
#         scores[chat_id] += 1
#     elif winner == 'bot' and not user_failed:
#         scores[opponent_id] += 1  # Update opponent's score in User vs User mode
#
#     game_time = time.time() - game_start_time
#     store_game_data(chat_id, opponent_id, winner, game_time, scores[chat_id], scores.get(opponent_id, 0))
#
#     # Show results
#     if winner == 'user':
#         result_message = f"You won! 🎉\nYour score: {scores[chat_id]}\n"
#     elif winner == 'bot':
#         result_message = f"You lost! 😞\nYour score: {scores[chat_id]}\n"
#     else:
#         result_message = f"It's a tie! 🤝\nYour score: {scores[chat_id]}\n"
#
#     if mode == MODE_AI:
#         result_message += f"Bot's score: {scores[opponent_id]}\n"
#     else:
#         result_message += f"Opponent's score: {scores.get(opponent_id, 0)}\n"
#
#     result_message += f"Game time: {game_time:.2f} seconds\n"
#     bot.send_message(chat_id, result_message)
#
#     # Play again prompt (optional)
#     play_again = input("Do you want to play again? (y/n): ").lower()
#     if play_again == 'y':
#         # Reset game state and scores if needed
#         if mode == MODE_USER or user_failed:
#             game_info[chat_id] = {'mode': None, 'scores': {chat_id: 0}, 'state': STATE_WAITING}
#         else:
#             game_info[chat_id]['scores'] = {chat_id: 0}
#         start_game(chat_id, mode, opponent_id)  # Continue with the same opponent in User vs User mode
#     else:
#         bot.send_message(chat_id, "Thanks for playing!")
#         game_info[chat_id]['state'] = STATE_WAITING
#
# # Store game data in database
# def store_game_data(chat_id, opponent_id, winner, time, score_user1, score_user2):
#     cursor.execute(
#         "INSERT INTO game_records (winner, time, score_user1, score_user2, user1_id, user2_id) VALUES (?, ?, ?, ?, ?, ?)",
#         (winner, time, score_user1, score_user2, chat_id, opponent_id))
#     conn.commit()
#
# bot.polling()


#
# import sys
# import random
# import time
# import sqlite3
# from telebot import TeleBot, types
#
# # Initialize the bot
# bot = TeleBot("6837439077:AAGaEwhRZCEuN6UGgIF8KKQkNG-DxemOvJg")
#
# # Database connection
# conn = sqlite3.connect("rps_game_data.db")
# cursor = conn.cursor()
#
# # Create table if not exists
# cursor.execute("""CREATE TABLE IF NOT EXISTS game_records (
#     game_no INTEGER PRIMARY KEY AUTOINCREMENT,
#     winner TEXT,
#     time REAL,
#     score_user1 INTEGER,
#     score_user2 INTEGER,
#     user1_id INTEGER,
#     user2_id INTEGER
# )""")
# conn.commit()
#
# # Game modes
# MODE_AI = 1
# MODE_USER = 2
#
# # Game states
# STATE_WAITING = 1
# STATE_PLAYING = 2
# STATE_END = 3
# STATE_WAITING_USER = 4
#
# # Score band
# SCORE_BAND = 5
#
# # Game timer and choice timer (in seconds)
# GAME_TIMER = 30
# CHOICE_TIMER = 5
#
# # Game information
# game_info = {}
#
# # Define game logic function
# def determine_winner(user_choice, bot_choice):
#     if user_choice == bot_choice:
#         return None  # It's a tie
#     elif (user_choice == 1 and bot_choice == 3) or \
#          (user_choice == 2 and bot_choice == 1) or \
#          (user_choice == 3 and bot_choice == 2):
#         return 'user'  # User wins
#     else:
#         return 'bot'  # Bot wins
#
# # Initialize scores
# scores = {}
#
# # Handler for /start command
# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     scores[message.chat.id] = 0  # Initialize scores for new users
#     bot.send_message(message.chat.id, 'Welcome to the Rock-Paper-Scissors game!\n'
#                                       'Choose a mode:\n'
#                                       '1. User vs AI\n'
#                                       '2. User vs User')
#     game_info[message.chat.id] = {'mode': None, 'scores': scores, 'state': STATE_WAITING}
#
# # Handle mode selection
# @bot.message_handler(func=lambda message: True)
# def handle_mode(message):
#     chat_id = message.chat.id
#     if game_info[chat_id]['state'] == STATE_WAITING:
#         try:
#             mode = int(message.text)
#             if mode in [MODE_AI, MODE_USER]:
#                 game_info[chat_id]['mode'] = mode
#                 if mode == MODE_AI:
#                     bot.send_message(chat_id, "Playing against AI. Choose your move:")
#                     start_game(chat_id, MODE_AI)
#                 else:
#                     bot.send_message(chat_id, "Waiting for another player...")
#                     game_info[chat_id]['state'] = STATE_WAITING_USER
#             else:
#                 bot.send_message(chat_id, "Invalid mode. Please choose 1 or 2.")
#         except ValueError:
#             bot.send_message(chat_id, "Invalid mode. Please choose 1 or 2.")
#
# # Handle waiting for user in User vs User mode
# @bot.message_handler(func=lambda message: True)
# def handle_waiting_user(message):
#     chat_id = message.chat.id
#     if game_info[chat_id]['state'] == STATE_WAITING_USER:
#         if message.chat.id not in game_info:  # Second player joined
#             game_info[message.chat.id] = {'mode': MODE_USER, 'scores': {message.chat.id: 0}, 'state': STATE_PLAYING}
#             start_game(chat_id, MODE_USER, list(game_info.keys())[0])  # Pass the first player's chat ID as opponent_id
#
# # Start game logic
# def start_game(chat_id, mode, opponent_id=None):
#     game_info[chat_id]['state'] = STATE_PLAYING
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     keyboard.add("👊 Rock")
#     keyboard.add("📃 Paper")
#     keyboard.add("✂️ Scissors")
#     bot.send_message(chat_id, 'Choose your move:', reply_markup=keyboard)
#
#     # Set timers
#     game_start_time = time.time()
#     choice_deadline = game_start_time + CHOICE_TIMER
#
#     while time.time() < choice_deadline:
#         # Handle user choice
#         @bot.message_handler(func=lambda message: message.chat.id == chat_id)
#         def handle_choice(message):
#             user_choice = message.text.lower()
#             if user_choice in ["rock", "paper", "scissors"]:
#                 # Process user choice and end game
#                 user_choice_num = {"rock": 1, "paper": 2, "scissors": 3}.get(user_choice)
#                 end_game(chat_id, user_choice_num, mode, opponent_id, game_start_time)
#                 return
#
#     # User didn't choose within time limit
#     if game_info[chat_id]['state'] == STATE_PLAYING:
#         bot.send_message(chat_id, "Time's up! You lose by default.")
#         end_game(chat_id, None, mode, opponent_id, game_start_time, user_failed=True)
#
# # End game logic
# def end_game(chat_id, user_choice, mode, opponent_id, game_start_time, user_failed=False):
#     game_info[chat_id]['state'] = STATE_END
#
#     if mode == MODE_AI:
#         bot_choice = random.randint(1, 3)
#         winner = determine_winner(user_choice, bot_choice)
#     else:
#         opponent_choice = game_info[opponent_id]['choice']
#         winner = determine_winner(user_choice, opponent_choice)
#
#     if winner == 'user':
#         scores[chat_id] += 1
#     elif winner == 'bot' and not user_failed:
#         scores[opponent_id] += 1  # Update opponent's score in User vs User mode
#
#     game_time = time.time() - game_start_time
#     store_game_data(chat_id, opponent_id, winner, game_time, scores[chat_id], scores.get(opponent_id, 0))
#
#     # Show results
#     if winner == 'user':
#         result_message = f"You won! 🎉\nYour score: {scores[chat_id]}\n"
#     elif winner == 'bot':
#         result_message = f"You lost! 😞\nYour score: {scores[chat_id]}\n"
#     else:
#         result_message = f"It's a tie! 🤝\nYour score: {scores[chat_id]}\n"
#
#     if mode == MODE_AI:
#         result_message += f"Bot's score: {scores[opponent_id]}\n"
#     else:
#         result_message += f"Opponent's score: {scores.get(opponent_id, 0)}\n"
#
#     result_message += f"Game time: {game_time:.2f} seconds\n"
#     bot.send_message(chat_id, result_message)
#
#     # Play again prompt (optional)
#     play_again = input("Do you want to play again? (y/n): ").lower()
#     if play_again == 'y':
#         # Reset game state and scores if needed
#         if mode == MODE_USER or user_failed:
#             game_info[chat_id] = {'mode': None, 'scores': {chat_id: 0}, 'state': STATE_WAITING}
#         else:
#             game_info[chat_id]['scores'] = {chat_id: 0}
#         start_game(chat_id, mode, opponent_id)  # Continue with the same opponent in User vs User mode
#     else:
#         bot.send_message(chat_id, "Thanks for playing!")
#         game_info[chat_id]['state'] = STATE_WAITING
#
# # Store game data in database
# def store_game_data(chat_id, opponent_id, winner, time, score_user1, score_user2):
#     cursor.execute(
#         "INSERT INTO game_records (winner, time, score_user1, score_user2, user1_id, user2_id) VALUES (?, ?, ?, ?, ?, ?)",
#         (winner, time, score_user1, score_user2, chat_id, opponent_id))
#     conn.commit()
#
# bot.polling()









####___by_fotima

# import telebot
# from telebot import types
# import random
#
# TOKEN = '6837439077:AAGaEwhRZCEuN6UGgIF8KKQkNG-DxemOvJg'
#
# bot = telebot.TeleBot(TOKEN)
#
# # Dictionary to store user choices for the game between users
# user_choices_users = {}
#
# # Dictionary to store user choices for the game with the bot
# user_choices_bot = {}
#
# # Function to determine the winner in rock-paper-scissors game
# def determine_winner(choice1, choice2):
#     if choice1 == choice2:
#         return None  # It's a tie
#     elif (choice1 == "rock" and choice2 == "scissors") or \
#          (choice1 == "paper" and choice2 == "rock") or \
#          (choice1 == "scissors" and choice2 == "paper"):
#         return 'user1'  # User 1 wins
#     else:
#         return 'user2'  # User 2 wins
#
# # Handler for /start command
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     itembtn1 = types.InlineKeyboardButton('Play with Bot', callback_data='play_with_bot')
#     itembtn2 = types.InlineKeyboardButton('Play between Users', callback_data='play_between_users')
#     markup.add(itembtn1, itembtn2)
#     bot.send_message(message.chat.id, "Welcome! Choose an option to play:", reply_markup=markup)
#
# # Handler for user's choice to play with the bot
# @bot.callback_query_handler(func=lambda call: call.data == 'play_with_bot')
# def play_with_bot(call):
#     user_choices_bot[call.message.chat.id] = []
#     markup = types.InlineKeyboardMarkup(row_width=3)
#     itembtn1 = types.InlineKeyboardButton('👊 Rock', callback_data='rock')
#     itembtn2 = types.InlineKeyboardButton('📃 Paper', callback_data='paper')
#     itembtn3 = types.InlineKeyboardButton('✂️ Scissors', callback_data='scissors')
#     markup.add(itembtn1, itembtn2, itembtn3)
#     bot.send_message(call.message.chat.id, "Please select your choice to play with the bot:", reply_markup=markup)
#
# # Handler for user's choice to play between users
# @bot.callback_query_handler(func=lambda call: call.data == 'play_between_users')
# def play_between_users(call):
#     user_choices_users[call.message.chat.id] = []
#     markup = types.InlineKeyboardMarkup(row_width=3)
#     itembtn1 = types.InlineKeyboardButton('👊 Rock', callback_data='rock')
#     itembtn2 = types.InlineKeyboardButton('📃 Paper', callback_data='paper')
#     itembtn3 = types.InlineKeyboardButton('✂️ Scissors', callback_data='scissors')
#     markup.add(itembtn1, itembtn2, itembtn3)
#     bot.send_message(call.message.chat.id, "Player 1, please select your choice to play between users:", reply_markup=markup)
#
#
# # Handler for user's choice in the game with the bot
# @bot.message_handler(func=lambda message: message.text.lower() in ['rock', 'paper', 'scissors'] and message.chat.id in user_choices_bot)
# def handle_choice_bot(message):
#     user_choice = message.text.lower()
#     bot_choice = random.choice(['rock', 'paper', 'scissors'])
#
#     winner = determine_winner(user_choice, bot_choice)
#
#     if winner == 'user1':
#         bot.reply_to(message, f"You chose {user_choice}. Bot chose {bot_choice}. You win!")
#     elif winner == 'user2':
#         bot.reply_to(message, f"You chose {user_choice}. Bot chose {bot_choice}. You lose!")
#     else:
#         bot.reply_to(message, f"You chose {user_choice}. Bot chose {bot_choice}. It's a tie!")
#
# # Handler for user's choice in the game between users
# @bot.message_handler(func=lambda message: message.text.lower() in ['rock', 'paper', 'scissors'] and message.chat.id in user_choices_users)
# def handle_choice_users(message):
#     user_choice = message.text.lower()
#     chat_id = message.chat.id
#
#     if len(user_choices_users[chat_id]) == 0:
#         user_choices_users[chat_id].append(user_choice)
#         markup = types.ReplyKeyboardMarkup(row_width=1)
#         itembtn1 = types.KeyboardButton('rock')
#         itembtn2 = types.KeyboardButton('paper')
#         itembtn3 = types.KeyboardButton('scissors')
#         markup.add(itembtn1, itembtn2, itembtn3)
#         bot.send_message(chat_id, "Player 2, please select your choice to play between users:", reply_markup=markup)
#     elif len(user_choices_users[chat_id]) == 1:
#         user_choices_users[chat_id].append(user_choice)
#         play_round_users(chat_id)
#
# # Function to play a round of the game between users
#
# def play_round_users(chat_id):
#     choices = user_choices_users[chat_id]
#     user_choices_users[chat_id] = []  # Reset choices for the next game
#
#     user1_choice = choices[0]
#     user2_choice = choices[1]
#
#     winner = determine_winner(user1_choice, user2_choice)
#
#     if winner == 'user1':
#         bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. Player 1 wins!")
#     elif winner == 'user2':
#         bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. Player 2 wins!")
#     else:
#         bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. It's a tie!")
#
# # Start the bot
# bot.polling()



####____last_code_by chatpt
# import telebot
# from telebot import types
# import random
# import sqlite3
# import time
#
# # Define constants
# TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
# SCORE_BAND = 3  # Change to 5 if desired
# GAME_TIMER = 30  # Game timer in seconds
# CHOICE_TIMER = 5  # Choice timer in seconds
#
# # Initialize the bot
# bot = telebot.TeleBot(TOKEN)
#
# # Database connection
# conn = sqlite3.connect("rps_game_data.db")
# cursor = conn.cursor()
#
# # Create table if not exists
# cursor.execute("""CREATE TABLE IF NOT EXISTS game_records (
#     game_no INTEGER PRIMARY KEY AUTOINCREMENT,
#     winner TEXT,
#     time REAL,
#     score_user1 INTEGER,
#     score_user2 INTEGER,
#     user1_id INTEGER,
#     user2_id INTEGER
# )""")
# conn.commit()
#
# # Game modes
# MODE_AI = 1
# MODE_USER = 2
#
# # Game states
# STATE_WAITING = 1
# STATE_PLAYING = 2
# STATE_END = 3
# STATE_WAITING_USER = 4
#
# # Dictionary to store game information
# game_info = {}
#
# # Dictionary to store user choices for the game between users
# user_choices_users = {}
#
# # Dictionary to store user choices for the game with the bot
# user_choices_bot = {}
#
#
# # Function to determine the winner in rock-paper-scissors game
# def determine_winner(choice1, choice2):
#     if choice1 == choice2:
#         return None  # It's a tie
#     elif (choice1 == "rock" and choice2 == "scissors") or \
#             (choice1 == "paper" and choice2 == "rock") or \
#             (choice1 == "scissors" and choice2 == "paper"):
#         return 'user1'  # User 1 wins
#     else:
#         return 'user2'  # User 2 wins
#
#
# # Handler for /start command
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup(row_width=1)
#     itembtn1 = types.KeyboardButton('User vs AI')
#     itembtn2 = types.KeyboardButton('User vs User')
#     markup.add(itembtn1, itembtn2)
#     bot.send_message(message.chat.id, "Welcome! Choose a mode to play:", reply_markup=markup)
#
#
# # Handler for mode selection
# @bot.message_handler(func=lambda message: message.text in ['User vs AI', 'User vs User'])
# def mode_selection(message):
#     chat_id = message.chat.id
#     mode = message.text
#
#     if mode == 'User vs AI':
#         game_info[chat_id] = {'mode': MODE_AI, 'state': STATE_WAITING, 'scores': {chat_id: 0}}
#         bot.send_message(chat_id, "Playing against AI. Choose your move:")
#         start_game(chat_id, MODE_AI)
#     elif mode == 'User vs User':
#         game_info[chat_id] = {'mode': MODE_USER, 'state': STATE_WAITING, 'scores': {chat_id: 0}}
#         bot.send_message(chat_id, "Waiting for another player...")
#         game_info[chat_id]['state'] = STATE_WAITING_USER
#
#
# # Handler for user's choice in the game with the bot
# @bot.message_handler(func=lambda message: message.text.lower() in ['rock', 'paper', 'scissors'] and message.chat.id in user_choices_bot)
# def handle_choice_bot(message):
#     chat_id = message.chat.id
#     user_choice = message.text.lower()
#     bot_choice = random.choice(['rock', 'paper', 'scissors'])
#
#     winner = determine_winner(user_choice, bot_choice)
#
#     if winner == 'user1':
#         bot.reply_to(message, f"You chose {user_choice}. Bot chose {bot_choice}. You win!")
#         game_info[chat_id]['scores'][chat_id] += 1
#     elif winner == 'user2':
#         bot.reply_to(message, f"You chose {user_choice}. Bot chose {bot_choice}. You lose!")
#     else:
#         bot.reply_to(message, f"You chose {user_choice}. Bot chose {bot_choice}. It's a tie!")
#
#     if winner:
#         end_game(chat_id, winner)
#
#
# # Handler for user's choice in the game between users
# @bot.message_handler(func=lambda message: message.text.lower() in ['rock', 'paper', 'scissors'] and message.chat.id in user_choices_users)
# def handle_choice_users(message):
#     chat_id = message.chat.id
#     user_choice = message.text.lower()
#
#     if len(user_choices_users[chat_id]) == 0:
#         user_choices_users[chat_id].append(user_choice)
#         markup = types.ReplyKeyboardMarkup(row_width=1)
#         itembtn1 = types.KeyboardButton('rock')
#         itembtn2 = types.KeyboardButton('paper')
#         itembtn3 = types.KeyboardButton('scissors')
#         markup.add(itembtn1, itembtn2, itembtn3)
#         bot.send_message(chat_id, "Player 2, please select your choice to play between users:", reply_markup=markup)
#     elif len(user_choices_users[chat_id]) == 1:
#         user_choices_users[chat_id].append(user_choice)
#         play_round_users(chat_id)
#
#
# # Function to play a round of the game between users
# def play_round_users(chat_id):
#     choices = user_choices_users[chat_id]
#     user_choices_users[chat_id] = []  # Reset choices for the next game
#
#     user1_choice = choices[0]
#     user2_choice = choices[1]
#
#     winner = determine_winner(user1_choice, user2_choice)
#
#     if winner == 'user1':
#         bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. Player 1 wins!")
#         game_info[chat_id]['scores'][chat_id] += 1
#     elif winner == 'user2':
#         bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. Player 2 wins!")
#     else:
#         bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. It's a tie!")
#
#     if winner:
#         end_game(chat_id, winner)
#
#
# # Function to start the game
# def start_game(chat_id, mode):
#     game_info[chat_id]['state'] = STATE_PLAYING
#     user_choices_bot[chat_id] = []
#
#     # Set timer for the game
#     game_start_time = time.time()
#     game_end_time = game_start_time + GAME_TIMER
#
#     while time.time() < game_end_time:
#         if time.time() >= game_end_time:
#             bot.send_message(chat_id, "Time's up! You lose by default.")
#             end_game(chat_id, 'user2')  # User 2 (bot) wins
#             break
#
#         # Handle user's choice
#         @bot.message_handler(func=lambda message: message.chat.id == chat_id and message.text.lower() in ['rock', 'paper', 'scissors'])
#         def handle_user_choice(message):
#             user_choices_bot[chat_id].append(message.text.lower())
#             user_choice_time = time.time()
#
#             # Set timer for user's choice
#             while time.time() < user_choice_time + CHOICE_TIMER:
#                 pass  # Wait for user's choice
#
#             if len(user_choices_bot[chat_id]) == 0:
#                 bot.send_message(chat_id, "Time's up! You lose by default.")
#                 end_game(chat_id, 'user2')  # User 2 (bot) wins
#             else:
#                 user_choice = user_choices_bot[chat_id][0]
#                 bot_choice = random.choice(['rock', 'paper', 'scissors'])
#                 winner = determine_winner(user_choice, bot_choice)
#
#                 if winner == 'user1':
#                     bot.send_message(chat_id, f"You chose {user_choice}. Bot chose {bot_choice}. You win!")
#                     game_info[chat_id]['scores'][chat_id] += 1
#                 elif winner == 'user2':
#                     bot.send_message(chat_id, f"You chose {user_choice}. Bot chose {bot_choice}. You lose!")
#                 else:
#                     bot.send_message(chat_id, f"You chose {user_choice}. Bot chose {bot_choice}. It's a tie!")
#
#                 end_game(chat_id, winner)
#         break
# # Function to end the game
# def end_game(chat_id, winner):
#     game_info[chat_id]['state'] = STATE_END
#
#     game_time = time.time() - game_info[chat_id]['start_time']
#     user1_score = game_info[chat_id]['scores'][chat_id]
#     user2_score = game_info[chat_id]['scores'].get(opponent_id, 0) if game_info[chat_id]['mode'] == MODE_USER else None
#
#     store_game_data(chat_id, None, winner, game_time, user1_score, user2_score)
#
#     # Show results
#     if winner == 'user1':
#         result_message = f"You won! 🎉\nYour score: {user1_score}\n"
#     elif winner == 'user2':
#         result_message = f"You lost! 😞\nYour score: {user1_score}\n"
#     else:
#         result_message = f"It's a tie! 🤝\nYour score: {user1_score}\n"
#
#     if game_info[chat_id]['mode'] == MODE_AI:
#         result_message += f"Bot's score: {user2_score}\n"
#     else:
#         result_message += f"Opponent's score: {user2_score}\n"
#
#     result_message += f"Game time: {game_time:.2f} seconds\n"
#     bot.send_message(chat_id, result_message)
#
#
# # Store game data in database
# def store_game_data(chat_id, opponent_id, winner, time, score_user1, score_user2):
#     cursor.execute(
#         "INSERT INTO game_records (winner, time, score_user1, score_user2, user1_id, user2_id) VALUES (?, ?, ?, ?, ?, ?)",
#         (winner, time, score_user1, score_user2, chat_id, opponent_id))
#     conn.commit()
#
# # Show Records
# def show_records():
#     cursor.execute("SELECT * FROM game_records")
#     records = cursor.fetchall()
#     # Process records and show analytics
#
#
# # Start the bot
# bot.polling()



#
# import telebot
# from telebot import types
# import random
#
# TOKEN = '6837439077:AAGaEwhRZCEuN6UGgIF8KKQkNG-DxemOvJg'
#
# bot = telebot.TeleBot(TOKEN)
#
# # Dictionary to store user choices for the game between users
# user_choices_users = {}
#
# # Dictionary to store user choices for the game with the bot
# user_choices_bot = {}
#
#
# # Function to determine the winner in rock-paper-scissors game
# def determine_winner(choice1, choice2):
#     if choice1 == choice2:
#         return None  # It's a tie
#     elif (choice1 == "rock 🪨" and choice2 == "scissors ✂️") or \
#             (choice1 == "paper 📃" and choice2 == "rock 🪨") or \
#             (choice1 == "scissors ✂️" and choice2 == "paper 📃"):
#         return 'user1'  # User 1 wins
#     else:
#         return 'user2'  # User 2 wins
#
# # Handler for /start command
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     itembtn1 = types.InlineKeyboardButton('Play with Bot 🤖', callback_data="play_with_bot")
#     itembtn2 = types.InlineKeyboardButton('Play between Users 👥', callback_data="play_between_users")
#     markup.add(itembtn1, itembtn2)
#     bot.send_message(message.chat.id, "Welcome! Choose an option to play:", reply_markup=markup)
#
# # Handler for user's choice to play with the bot
# @bot.message_handler(func=lambda message: message.text == 'Play with Bot 🤖')
# def play_with_bot(message):
#     user_choices_bot[message.chat.id] = []
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     itembtn1 = types.InlineKeyboardButton('rock 🪨', callback_data="rock")
#     itembtn2 = types.InlineKeyboardButton('paper 📃', callback_data="paper")
#     itembtn3 = types.InlineKeyboardButton('scissors ✂️', callback_data="scissors")
#     itembtn4 = types.InlineKeyboardButton('back', callback_data="back")
#     markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
#     bot.send_message(message.chat.id, "Please select your choice to play with the bot:", reply_markup=markup)
#
#
# # Handler for user's choice to play between users
# @bot.message_handler(func=lambda message: message.text == 'Play between Users 👥')
# def play_between_users(message):
#     user_choices_users[message.chat.id] = []
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     itembtn1 = types.InlineKeyboardButton('rock 🪨', callback_data="rock")
#     itembtn2 = types.InlineKeyboardButton('paper 📃', callback_data="paper")
#     itembtn3 = types.InlineKeyboardButton('scissors ✂️', callback_data="scissors")
#     itembtn4 = types.InlineKeyboardButton('back', callback_data="back")
#     markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
#     bot.send_message(message.chat.id, "Player 1, please select your choice to play between users:", reply_markup=markup)
#
#
# # Handler for user's choice in the game with the bot
# @bot.message_handler(
#     func=lambda message: message.text.lower() in ['rock 🪨', 'paper 📃', 'scissors ✂️'] and message.chat.id in user_choices_bot)
# def handle_choice_bot(message):
#     user_choice = message.text.lower()
#     bot_choice = random.choice(['rock 🪨', 'paper 📃', 'scissors ✂️'])
#
#     winner = determine_winner(user_choice, bot_choice)
#
#     if winner == 'user1':
#         bot.reply_to(message, f"You chose {user_choice}. Bot chose {bot_choice}. You win!")
#     elif winner == 'user2':
#         bot.reply_to(message, f"You chose {user_choice}. Bot chose {bot_choice}. You lose!")
#     else:
#         bot.reply_to(message, f"You chose {user_choice}. Bot chose {bot_choice}. It's a tie!")
#
#
# # Handler for user's choice in the game between users
# @bot.message_handler(func=lambda message: message.text.lower() in ['rock 🪨', 'paper 📃',
#                                                                    'scissors ✂️'] and message.chat.id in user_choices_users)
# def handle_choice_users(message):
#     user_choice = message.text.lower()
#     chat_id = message.chat.id
#     if len(user_choices_users[chat_id]) == 0:
#         user_choices_users[chat_id].append(user_choice)
#         markup = types.InlineKeyboardMarkup(row_width=1)
#         itembtn1 = types.InlineKeyboardButton('rock 🪨', callback_data="rock")
#         itembtn2 = types.InlineKeyboardButton('paper 📃', callback_data="paper")
#         itembtn3 = types.InlineKeyboardButton('scissors ✂️', callback_data="scissors")
#         itembtn4 = types.InlineKeyboardButton('back', callback_data="back")
#         markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
#         bot.send_message(chat_id, "Player 2, please select your choice to play between users:", reply_markup=markup)
#     elif len(user_choices_users[chat_id]) == 1:
#         user_choices_users[chat_id].append(user_choice)
#         play_round_users(chat_id)
#
# # Function to play a round of the game between users
# def play_round_users(chat_id):
#         choices = user_choices_users[chat_id]
#         user_choices_users[chat_id] = []  # Reset choices for the next game
#         user1_choice = choices[0]
#         user2_choice = choices[1]
#         winner = determine_winner(user1_choice, user2_choice)
#
#         if winner == 'user1':
#             bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. Player 1 wins!")
#         elif winner == 'user2':
#             bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. Player 2 wins!")
#         else:
#             bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. It's a tie!")
#
# # Handler for user's choice to finish the game
# @bot.message_handler(func=lambda message: message.text == 'back')
# def finish_game(message):
#     chat_id = message.chat.id
#
#     # Check if the game was with the bot or between users and remove the user's choice data accordingly
#     if chat_id in user_choices_bot:
#         del user_choices_bot[chat_id]
#     elif chat_id in user_choices_users:
#         del user_choices_users[chat_id]
#
#     markup = types.ReplyKeyboardMarkup(row_width=1)
#     itembtn1 = types.KeyboardButton('Play with Bot 🤖')
#     itembtn2 = types.KeyboardButton('Play between Users 👥')
#     markup.add(itembtn1, itembtn2)
#     bot.send_message(chat_id, "choose again please!", reply_markup=markup)
#
# bot.polling()
#
#



#
#
# import telebot
# from telebot import types
# import random
#
# TOKEN = '6837439077:AAGaEwhRZCEuN6UGgIF8KKQkNG-DxemOvJg'
#
# bot = telebot.TeleBot(TOKEN)
#
# # Dictionary to store user choices for the game between users
# user_choices_users = {}
#
# # Dictionary to store user choices for the game with the bot
# user_choices_bot = {}
#
#
# # Function to determine the winner in rock-paper-scissors game
# def determine_winner(choice1, choice2):
#     if choice1 == choice2:
#         return None  # It's a tie
#     elif (choice1 == "rock 🪨" and choice2 == "scissors ✂️") or \
#             (choice1 == "paper 📃" and choice2 == "rock 🪨") or \
#             (choice1 == "scissors ✂️" and choice2 == "paper 📃"):
#         return 'user1'  # User 1 wins
#     else:
#         return 'user2'  # User 2 wins
#
# # Handler for /start command
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     itembtn1 = types.InlineKeyboardButton('Play with Bot 🤖', callback_data="play_with_bot")
#     itembtn2 = types.InlineKeyboardButton('Play between Users 👥', callback_data="play_between_users")
#     markup.add(itembtn1, itembtn2)
#     bot.send_message(message.chat.id, "Welcome! Choose an option to play:", reply_markup=markup)
#
# # Handler for user's choice to play with the bot
# @bot.callback_query_handler(func=lambda call: call.data == 'play_with_bot')
# def play_with_bot(call):
#     user_choices_bot[call.message.chat.id] = []
#     markup = types.InlineKeyboardMarkup(row_width=3)
#     itembtn1 = types.InlineKeyboardButton('rock 🪨', callback_data="rock")
#     itembtn2 = types.InlineKeyboardButton('paper 📃', callback_data="paper")
#     itembtn3 = types.InlineKeyboardButton('scissors ✂️', callback_data="scissors")
#     markup.add(itembtn1, itembtn2, itembtn3)
#     bot.send_message(call.message.chat.id, "Please select your choice to play with the bot:", reply_markup=markup)
#
#
# # Handler for user's choice to play between users
# @bot.callback_query_handler(func=lambda call: call.data == 'play_between_users')
# def play_between_users(call):
#     user_choices_users[call.message.chat.id] = []
#     markup = types.InlineKeyboardMarkup(row_width=3)
#     itembtn1 = types.InlineKeyboardButton('rock 🪨', callback_data="rock")
#     itembtn2 = types.InlineKeyboardButton('paper 📃', callback_data="paper")
#     itembtn3 = types.InlineKeyboardButton('scissors ✂️', callback_data="scissors")
#     markup.add(itembtn1, itembtn2, itembtn3)
#     bot.send_message(call.message.chat.id, "Player 1, please select your choice to play between users:", reply_markup=markup)
#
#
# # Handler for user's choice in the game with the bot
# @bot.callback_query_handler(func=lambda call: call.data in ['rock', 'paper', 'scissors'] and call.message.chat.id in user_choices_bot)
# def handle_choice_bot(call):
#     user_choice = call.data
#     bot_choice = random.choice(['rock', 'paper', 'scissors'])
#
#     winner = determine_winner(user_choice, bot_choice)
#
#     if winner == 'user1':
#         bot.send_message(call.message.chat.id, f"You chose {user_choice}. Bot chose {bot_choice}. You win!")
#     elif winner == 'user2':
#         bot.send_message(call.message.chat.id, f"You chose {user_choice}. Bot chose {bot_choice}. You lose!")
#     else:
#         bot.send_message(call.message.chat.id, f"You chose {user_choice}. Bot chose {bot_choice}. It's a tie!")
#
#
# # Handler for user's choice in the game between users
# @bot.callback_query_handler(func=lambda call: call.data in ['rock', 'paper', 'scissors'] and call.message.chat.id in user_choices_users)
# def handle_choice_users(call):
#     user_choice = call.data
#     chat_id = call.message.chat.id
#     if len(user_choices_users[chat_id]) == 0:
#         user_choices_users[chat_id].append(user_choice)
#         markup = types.InlineKeyboardMarkup(row_width=3)
#         itembtn1 = types.InlineKeyboardButton('rock 🪨', callback_data="rock")
#         itembtn2 = types.InlineKeyboardButton('paper 📃', callback_data="paper")
#         itembtn3 = types.InlineKeyboardButton('scissors ✂️', callback_data="scissors")
#         markup.add(itembtn1, itembtn2, itembtn3)
#         bot.send_message(chat_id, "Player 2, please select your choice to play between users:", reply_markup=markup)
#     elif len(user_choices_users[chat_id]) == 1:
#         user_choices_users[chat_id].append(user_choice)
#         play_round_users(chat_id)
#
# # Function to play a round of the game between users
# def play_round_users(chat_id):
#         choices = user_choices_users[chat_id]
#         user_choices_users[chat_id] = []  # Reset choices for the next game
#
#         user1_choice = choices[0]
#         user2_choice = choices[1]
#
#         winner = determine_winner(user1_choice, user2_choice)
#
#         if winner == 'user1':
#             bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. Player 1 wins!")
#         elif winner == 'user2':
#             bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. Player 2 wins!")
#         else:
#             bot.send_message(chat_id, f"Player 1 chose {user1_choice}. Player 2 chose {user2_choice}. It's a tie!")
#
# # Handler for user's choice to finish the game
# @bot.callback_query_handler(func=lambda call: call.data == 'back')
# def finish_game(call):
#     chat_id = call.message.chat.id
#
#     # Check if the game was with the bot or between users and remove the user's choice data accordingly
#     if chat_id in user_choices_bot:
#         del user_choices_bot[chat_id]
#     elif chat_id in user_choices_users:
#         del user_choices_users[chat_id]
#
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     itembtn1 = types.InlineKeyboardButton('Play with Bot 🤖', callback_data="play_with_bot")
#     itembtn2 = types.InlineKeyboardButton('Play between Users 👥', callback_data="play_between_users")
#     markup.add(itembtn1, itembtn2)
#     bot.send_message(chat_id, "Choose again please!", reply_markup=markup)
#
# bot.polling()

#
# import telebot
# from telebot import types
#
# TOKEN = '6837439077:AAGaEwhRZCEuN6UGgIF8KKQkNG-DxemOvJg'
#
# bot = telebot.TeleBot(TOKEN)
#
# # Dictionary to store user choices for the game between users
# user_choices_users = {}
#
# # Function to determine the winner in rock-paper-scissors game
# def determine_winner(choice1, choice2):
#     if choice1 == choice2:
#         return None  # It's a tie
#     elif (choice1 == "rock 🪨" and choice2 == "scissors ✂️") or \
#             (choice1 == "paper 📃" and choice2 == "rock 🪨") or \
#             (choice1 == "scissors ✂️" and choice2 == "paper 📃"):
#         return 'user1'  # User 1 wins
#     else:
#         return 'user2'  # User 2 wins
#
# # Handler for /start command
# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, "Welcome! Please forward this message to the other player.")
#     bot.send_message(message.chat.id, "Once the other player is ready, type /play to start the game.")
#
# # Handler for /play command
# @bot.message_handler(commands=['play'])
# def play(message):
#     if message.chat.id in user_choices_users:
#         bot.send_message(message.chat.id, "A game is already in progress. Please wait for it to finish.")
#     else:
#         user_choices_users[message.chat.id] = {'choice': None}
#         bot.send_message(message.chat.id, "You have joined the game. Please select your choice: rock 🪨, paper 📃, or scissors ✂️.")
#
# # Handler for user's choice in the game between users
# @bot.message_handler(func=lambda message: message.text.lower() in ['rock 🪨', 'paper 📃', 'scissors ✂️'] and
#                                             message.chat.id in user_choices_users)
# def handle_choice_users(message):
#     user_choice = message.text.lower()
#     user_id = message.chat.id
#
#     if user_choices_users[user_id]['choice'] is None:
#         user_choices_users[user_id]['choice'] = user_choice
#         bot.send_message(user_id, "Waiting for the other player to make their choice...")
#     else:
#         bot.send_message(user_id, "You have already made your choice. Please wait for the other player to make theirs.")
#
#     # Check if both players have made their choices
#     if all(user['choice'] is not None for user in user_choices_users.values()):
#         play_round_users()
#
# # Function to play a round of the game between users
# def play_round_users():
#     user1_id, user2_id = user_choices_users.keys()
#
#     user1_choice = user_choices_users[user1_id]['choice']
#     user2_choice = user_choices_users[user2_id]['choice']
#
#     winner = determine_winner(user1_choice, user2_choice)
#
#     if winner == 'user1':
#         bot.send_message(user1_id, f"You chose {user1_choice}. Other player chose {user2_choice}. You win!")
#         bot.send_message(user2_id, f"Other player chose {user1_choice}. You chose {user2_choice}. You lose!")
#     elif winner == 'user2':
#         bot.send_message(user1_id, f"You chose {user1_choice}. Other player chose {user2_choice}. You lose!")
#         bot.send_message(user2_id, f"Other player chose {user1_choice}. You chose {user2_choice}. You win!")
#     else:
#         bot.send_message(user1_id, f"You chose {user1_choice}. Other player chose {user2_choice}. It's a tie!")
#         bot.send_message(user2_id, f"Other player chose {user1_choice}. You chose {user2_choice}. It's a tie!")
#
#     # Clear choices for the next round
#     user_choices_users.clear()
#
# bot.polling()



#######_____by__ocean
# import telebot
# import random
# import threading
# from telebot import types
# import mysql.connector
#
# user_choose = {'player_1': None, 'player_2': None}
# player_choices = {}
# player_timers = {}
# message_status = {}
# user2_name = None
# user1_id = False
# user2_id = None
# user_name = None
# # Connection
# conn = mysql.connector.connect(
#     host='127.0.0.1',
#     user='root',
#     password='5members',
#     database='game_bot_data'
# )
# cursor = conn.cursor()
#
# bot = telebot.TeleBot("6837439077:AAGaEwhRZCEuN6UGgIF8KKQkNG-DxemOvJg")
#
# @bot.message_handler(commands=['start'])
# def start_quiz(message):
#     birinchi_knopka(message, 'Welcome to Rock, Paper, Scissors! To play, choose one of this options')
#
# def birinchi_knopka(message, text):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     login_n = types.InlineKeyboardButton("User vs AI", callback_data="user_ai")
#     signup_p = types.InlineKeyboardButton("User vs User", callback_data="user1_user2")
#     markup.row(login_n, signup_p)
#     bot.send_message(message.chat.id, text, reply_markup=markup)
#
# def user_vs_user(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     login_n = types.InlineKeyboardButton("🔐 Login", callback_data="login")
#     signup_p = types.InlineKeyboardButton("✍️ Sign up", callback_data="signup")
#     markup.row(login_n, signup_p)
#     bot.send_message(message.chat.id, "Please choose one of this options to play with your friend", reply_markup=markup)
#
#
# # callback function
# @bot.callback_query_handler(func=lambda call: True)
# def handle_answer(call):
#     global user_choose
#     global player_choices
#     global player_timers
#     global message_status
#     if call.data == "confirm":
#         message_status[call.message.message_id] = True  # Set this message as confirmed
#         bot.answer_callback_query(call.id, "Confirmed!")
#         bot.edit_message_text("Confirmed successfully!", call.message.chat.id, call.message.message_id)
#         bot.send_message(user1_id, 'Confirmed!')
#         start_game_command(call.message)
#     elif call.data == "login":
#         bot.send_message(call.message.chat.id, "👤 Please enter your username!")
#         bot.register_next_step_handler(call.message, user_name_check)
#     elif call.data == "signup":
#         bot.send_message(call.message.chat.id, "👤 Please enter your username!")
#         bot.register_next_step_handler(call.message, user_name_set)
#     elif call.data == "user_ai":
#         knopka(call.message)
#     elif call.data == "user1_user2":
#         user_vs_user(call.message)
#     elif call.data == "rock":
#         play_game(call.message, 'rock')
#     elif call.data == "paper":
#         play_game(call.message, 'paper')
#     elif call.data == "scissors":
#         play_game(call.message, 'scissors')
#     elif call.data == "rock_user_1":
#         user_choose["player_1"] = 'rock'
#         if user_choose["player_2"] == None:
#             pass
#         else:
#             result = check_winner(user_choose["player_1"], user_choose["player_2"])
#             fatal_result(result)
#     elif call.data == "paper_user_1":
#         user_choose["player_1"] = 'paper'
#         if user_choose["player_2"] == None:
#             pass
#         else:
#             result = check_winner(user_choose["player_1"], user_choose["player_2"])
#             fatal_result(result)
#     elif call.data == "scissors_user_1":
#         user_choose["player_1"] = 'scissors'
#         if user_choose["player_2"] == None:
#             pass
#         else:
#             result = check_winner(user_choose["player_1"], user_choose["player_2"])
#             fatal_result(result)
#     elif call.data == "rock_user_2":
#         user_choose["player_2"] = 'rock'
#         if user_choose["player_1"] == None:
#             pass
#         else:
#             result = check_winner(user_choose["player_1"], user_choose["player_2"])
#             fatal_result(result)
#     elif call.data == "paper_user_2":
#         user_choose["player_2"] = 'paper'
#         if user_choose["player_1"] == None:
#             pass
#         else:
#             result = check_winner(user_choose["player_1"], user_choose["player_2"])
#             fatal_result(result)
#     elif call.data == "scissors_user_2":
#         user_choose["player_2"] = 'scissors'
#         if user_choose["player_1"] == None:
#             pass
#         else:
#             result = check_winner(user_choose["player_1"], user_choose["player_2"])
#             fatal_result(result)
#     elif call.data == 'new_challenge':
#         user_choose = {'player_1': None, 'player_2': None}
#         start_game_command(call.message)
#     elif call.data == 'back_to_menu':
#         user_choose = {'player_1': None, 'player_2': None}
#         bot.send_message(call.message.chat.id, "Please entre your friend's user name")
#         bot.register_next_step_handler(call.message, confirmation_user2)
#
#
# def fatal_result(nimadur):
#     markup = types.InlineKeyboardMarkup()
#     new_test = types.InlineKeyboardButton("New Challenge", callback_data="new_challenge")
#     back_to_menu = types.InlineKeyboardButton("Back to menu", callback_data="back_to_menu")
#     markup.row(new_test)
#     markup.row(back_to_menu)
#
#     total = 0
#     if nimadur == 'tie':
#         total_result = f'Tie! 😮‍💨\n Total result: \n\n'
#         cursor.execute("insert into all_data(user_name, user_score, winn) values (%s, 3, 'tie')", (user_name,))
#         cursor.execute("insert into all_data(user_name, user_score, winn) values (%s, 3, 'tie')", (user2_name,))
#         conn.commit()
#         cursor.execute("update user_data set user_score = user_score + 3 where user_name = %s", (user2_name,))
#         cursor.execute("update user_data set user_score = user_score + 3 where user_name = %s", (user_name,))
#         conn.commit()
#         cursor.execute(
#             "select count(user_score), sum(user_score), winn from all_data where user_name = %s or user_name = %s group by winn;",
#             (user_name, user2_name))
#         result = cursor.fetchall()
#         total_result += f'Winner score = {result[0][1]}\n'
#         total_result += f'Looser score = {result[1][1]}\n'
#         total_result += f'Tie_score {result[1][1]}\n'
#         total += result[0][0]
#         total += result[1][0]
#         total_result += f'Total Number of games = {total}\n\n'
#         cursor.execute(
#             "select user_name, sum(user_score) from user_data where user_name = %s or user_name = %s group by user_name;",
#             (user_name, user2_name))
#         result = cursor.fetchall()
#         total_result += f'Users score:\n\n{result[0][0]}: {result[0][1]}\n {result[1][0]}: {result[1][1]}'
#         bot.send_message(user1_id, total_result, reply_markup=markup)
#         bot.send_message(user2_id, total_result, reply_markup=markup)
#
#     elif nimadur == 'player_1':
#         total_result = f'Player 1 woooon! 😎\n Total result: \n\n'
#         cursor.execute("insert into all_data(user_name, user_score, winn) values (%s, 5, 'True')", (user_name,))
#         cursor.execute("insert into all_data(user_name, user_score, winn) values (%s, 0, 'False')", (user2_name,))
#         conn.commit()
#         cursor.execute("update user_data set user_score = user_score + 0 where user_name = %s", (user2_name,))
#         cursor.execute("update user_data set user_score = user_score + 5 where user_name = %s", (user_name,))
#         conn.commit()
#         cursor.execute(
#             "select count(user_score), sum(user_score), winn from all_data where user_name = %s or user_name = %s group by winn;",
#             (user_name, user2_name))
#         result = cursor.fetchall()
#         total_result += f'Winner score = {result[0][1]}\n'
#         total_result += f'Looser score = {result[1][1]}\n'
#         total_result += f'Tie_score {result[1][1]}\n'
#         total += result[0][0]
#         total += result[1][0]
#         total_result += f'Total Number of games = {total}\n\n'
#         cursor.execute(
#             "select user_name, sum(user_score) from user_data where user_name = %s or user_name = %s group by user_name;",
#             (user_name, user2_name))
#         result = cursor.fetchall()
#         total_result += f'Users score:\n\n{result[0][0]}: {result[0][1]}\n {result[1][0]}: {result[1][1]}'
#         bot.send_message(user1_id, total_result, reply_markup=markup)
#         bot.send_message(user2_id, total_result, reply_markup=markup)
#
#     elif nimadur == 'player_2':
#         total_result = f'Player 2 woooon! 🥱\n Total result: \n\n'
#         cursor.execute("insert into all_data(user_name, user_score, winn) values (%s, 0, 'True')", (user_name,))
#         cursor.execute("insert into all_data(user_name, user_score, winn) values (%s, 5, 'False')", (user2_name,))
#         conn.commit()
#         cursor.execute("update user_data set user_score = user_score + 5 where user_name = %s", (user2_name,))
#         cursor.execute("update user_data set user_score = user_score + 0 where user_name = %s", (user_name,))
#         conn.commit()
#         cursor.execute(
#             "select count(user_score), sum(user_score), winn from all_data where user_name = %s or user_name = %s group by winn;",
#             (user_name, user2_name))
#         result = cursor.fetchall()
#         total_result += f'Winner score = {result[0][1]}\n'
#         total_result += f'Looser score = {result[1][1]}\n'
#         total_result += f'Tie_score {result[1][1]}\n'
#         total += result[0][0]
#         total += result[1][0]
#         total_result += f'Total Number of games = {total}\n\n'
#         cursor.execute(
#             "select user_name, sum(user_score) from user_data where user_name = %s or user_name = %s group by user_name;",
#             (user_name, user2_name))
#         result = cursor.fetchall()
#         total_result += f'Users score:\n\n{result[0][0]}: {result[0][1]}\n {result[1][0]}: {result[1][1]}'
#         bot.send_message(user1_id, total_result, reply_markup=markup)
#         bot.send_message(user2_id, total_result, reply_markup=markup)
#
#
# def knopka(message):
#     markup = types.InlineKeyboardMarkup(row_width=3)
#     rock = types.InlineKeyboardButton('Rock ✊', callback_data="rock")
#     paper = types.InlineKeyboardButton('Paper ✋', callback_data="paper")
#     scissors = types.InlineKeyboardButton('scissors ✌️', callback_data="scissors")
#
#     markup.row(rock, paper, scissors)
#     bot.send_message(message.chat.id, "To play, just send me your choice: rock, paper, or scissors.",
#                      reply_markup=markup)
#
#
# # user name check from mysql
#
# @bot.message_handler(content_types=["text"])
# def user_name_check(message):
#     global user_name
#     global user1_id
#     user_name = message.text.strip()
#     cursor.execute("SELECT user_name, user_id FROM user_data WHERE user_name = %s", (user_name,))
#     result = cursor.fetchall()
#     if result == []:
#         bot.send_message(message.chat.id, "User not found ❌")
#         bot.send_message(message.chat.id, "Please enter the correct one ✅")
#         bot.register_next_step_handler(message, user_name_check)
#     else:
#         user1_id = result[0][1]
#         bot.send_message(message.chat.id, "Please entre your friend's user name")
#         bot.register_next_step_handler(message, confirmation_user2)
#
#
# # set new user to mysql
# @bot.message_handler(content_types=["text"])
# def user_name_set(message):
#     global user_name
#     global user1_id
#     user_name = message.text.strip()
#     user1_id = message.from_user.id
#     print(user1_id)
#     user_id = str(user1_id)
#     cursor.execute("SELECT user_name FROM user_data WHERE user_name = %s", (user_name,))
#     result = cursor.fetchall()
#     if result == []:
#         sql_query = "INSERT INTO user_data (user_name, user_id, user_score) VALUES (%s, %s, 0)"
#         values = (user_name, user1_id)
#         cursor.execute(sql_query, values)
#         conn.commit()
#         bot.send_message(message.chat.id, "Please entre your friend's user name")
#         bot.register_next_step_handler(message, confirmation_user2)
#     else:
#         bot.send_message(message.chat.id, "User already exist ❌")
#         bot.send_message(message.chat.id, "Please enter the correct one ✅")
#         bot.register_next_step_handler(message, user_name_check)
#
#
# def determine_winner(user_choice, computer_choice):
#     if user_choice == computer_choice:
#         return "It's a tie! 😮‍💨"
#     elif (user_choice == "rock" and computer_choice == "scissors") or \
#             (user_choice == "paper" and computer_choice == "rock") or \
#             (user_choice == "scissors" and computer_choice == "paper"):
#         return "You win! 🥳"
#     else:
#         return "Computer wins! 😭"
#
#
# def play_game(message, user_ch):
#     user_choice = user_ch
#     computer_choice = random.choice(["rock", "paper", "scissors"])
#     result = determine_winner(user_choice, computer_choice)
#
#     bot.reply_to(message, f"You chose {user_choice}. The computer chose {computer_choice}.\n{result}")
#     knopka(message)
#
#
# def timeout(user_id, message_id):
#     threading.Timer(30.0, check_confirmation, args=(user_id, message_id)).start()
#
#
# def check_confirmation(user_id, message_id):
#     if message_id in message_status and not message_status[message_id]:
#         bot.send_message(user_id, "You lost! You didn't confirm in time.")
#         del message_status[message_id]
#
#
# @bot.message_handler(content_types=["text"])
# def confirmation_user2(message):
#     global user2_id
#     global user2_name
#     user2_name = message.text.strip()
#     cursor.execute("SELECT user_name, user_id FROM user_data WHERE user_name = %s", (user2_name,))
#     result = cursor.fetchall()
#     if result == []:
#         bot.send_message(message.chat.id, "User not found ❌")
#         bot.send_message(message.chat.id, "Please enter the correct one ✅")
#         bot.register_next_step_handler(message, user_name_check)
#     else:
#         user2_id = result[0][1]
#         print(user2_id)
#     markup = types.InlineKeyboardMarkup()
#     button = types.InlineKeyboardButton("Confirm", callback_data="confirm")
#     markup.add(button)
#     sent_message = bot.send_message(user2_id, "Press confirm within 30 seconds!", reply_markup=markup)
#     message_status[sent_message.message_id] = False  # Track this message as not confirmed
#     timeout(user2_id, sent_message.message_id)
#
#
# # Function to handle the start of the game
# def start_game(player_1):
#     markup = types.InlineKeyboardMarkup(row_width=3)
#     rock_button = types.InlineKeyboardButton('Rock ✊', callback_data="rock_user_1")
#     paper_button = types.InlineKeyboardButton('Paper ✋', callback_data="paper_user_1")
#     scissors_button = types.InlineKeyboardButton('Scissors ✌️', callback_data="scissors_user_1")
#     markup.row(rock_button, paper_button, scissors_button)
#     bot.send_message(player_1, "Player 1, choose one of the options.", reply_markup=markup)
#
#
# def start_timer(user_id):
#     player_timers[user_id] = threading.Timer(10.0, handle_timeout, args=[user_id])
#     player_timers[user_id].start()
#
#
# def handle_timeout(user_id):
#     if 'rock' not in player_choices or 'scissors' not in player_choices or 'paper' not in player_choices:
#         bot.send_message(user_id, "You lost! You didn't choose within the time limit.")
#
#
# def send_message_to_second_player(chat_id):
#     markup = types.InlineKeyboardMarkup(row_width=3)
#     rock_button = types.InlineKeyboardButton('Rock ✊', callback_data="rock_user_2")
#     paper_button = types.InlineKeyboardButton('Paper ✋', callback_data="paper_user_2")
#     scissors_button = types.InlineKeyboardButton('Scissors ✌️', callback_data="scissors_user_2")
#     markup.row(rock_button, paper_button, scissors_button)
#     bot.send_message(chat_id, "Player 2, choose one of the options.", reply_markup=markup)
#
#
# # Function to determine the winner
# def check_winner(player1_choice, player2_choice):
#     if player1_choice == player2_choice:
#         return "tie"
#     elif (player1_choice == 'rock' and player2_choice == 'scissors') or \
#             (player1_choice == 'paper' and player2_choice == 'rock') or \
#             (player1_choice == 'scissors' and player2_choice == 'paper'):
#         return "player_1"
#     else:
#         return "player_2"
#
#
# def start_game_command(message):
#     player1_id = user1_id
#     print(user1_id)
#     player2_id = user2_id
#     print(user2_id)
#     start_game(player1_id)
#     start_timer(message)
#     send_message_to_second_player(player2_id)
#
# bot.polling()










# ###  true code
import telebot
from telebot import types
import random
import mysql.connector
from mysql.connector import Error

API_TOKEN = '6837439077:AAGaEwhRZCEuN6UGgIF8KKQkNG-DxemOvJg'
bot = telebot.TeleBot(API_TOKEN)

def create_connection():
    return mysql.connector.connect(
        host='localhost',
        database='korzinka',
        user='root',
        password='5members'
    )

def create_table():
    connection = create_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS game_results (
            game_no INT AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT,
            opponent_id BIGINT,
            username VARCHAR(255),
            opponent_username VARCHAR(255),
            winner VARCHAR(255),
            user_score INT,
            opponent_score INT,
            tie BOOLEAN,
            game_time_seconds INT,
            game_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            game_end TIMESTAMP
        )""")
        connection.commit()
    finally:
        cursor.close()
        connection.close()

create_table()

choices = {"Rock": "ROCK✊", "Paper": "PAPER✋", "Scissors": "SCISSORS✌️"}
user_game_states = {}
user_queue = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('Play with bot 🤖'), types.KeyboardButton('Play between two users 👥'))
    # markup.row(types.KeyboardButton('Records 📊'), types.KeyboardButton('Analytics 📈'))
    bot.send_message(message.chat.id, "ASSALOMU ALAYKUM 👋\n ☺️ ARE YOU READY PLAY ROCK, PAPER, SCISSORS?", reply_markup=markup)

# @bot.message_handler(func=lambda message: message.text == 'Records 📊')
# def show_records(message):
#     send_statistics(message)
#
# @bot.message_handler(func=lambda message: message.text == 'Analytics 📈')
# def show_analytics(message):
#     send_analytics(message)

def send_statistics(message):
    user_id = message.from_user.id
    stats = fetch_statistics(user_id)
    if stats and stats['total_games'] > 0:
        response = (f"📊 Your Game Statistics 📊\n"
                    f"Total Games: {stats['total_games']}\n"
                    f"Wins: {stats['wins']}\n"
                    f"Losses: {stats['losses']}\n"
                    f"Ties: {stats['ties']}")
    else:
        response = "No game statistics available. Start playing to gather data!"
    bot.send_message(message.chat.id, response)

def fetch_statistics(user_id):
    connection = create_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                COUNT(*) AS total_games,
                SUM(CASE WHEN winner = %s THEN 1 ELSE 0 END) AS wins,
                SUM(CASE WHEN winner != %s AND winner != 'Tie' THEN 1 ELSE 0 END) AS losses,
                SUM(CASE WHEN tie = TRUE THEN 1 ELSE 0 END) AS ties
            FROM game_results
            WHERE user_id = %s
        """, (user_id, user_id, user_id))
        stats = cursor.fetchone()
        return stats if stats else {'total_games': 0, 'wins': 0, 'losses': 0, 'ties': 0}
    finally:
        cursor.close()
        connection.close()

def send_analytics(message):
    user_id = message.from_user.id
    analytics = fetch_analytics(user_id)
    if analytics:
        response = (f"📈 Detailed Analytics 📈\n"
                    f"Highest Score: {analytics['highest_score']}\n"
                    f"Lowest Score: {analytics['lowest_score']}\n"
                    f"Average Score: {analytics['average_score']:.2f}\n"
                    f"Total Games: {analytics['total_games']}")
    else:
        response = "No detailed analytics available. Start playing to gather data!"
    bot.send_message(message.chat.id, response)

def fetch_analytics(user_id):
    connection = create_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                MAX(user_score) AS highest_score,
                MIN(user_score) AS lowest_score,
                AVG(user_score) AS average_score,
                COUNT(*) AS total_games
            FROM game_results
            WHERE user_id = %s
        """, (user_id,))
        analytics = cursor.fetchone()
        return analytics if analytics['total_games'] > 0 else None
    finally:
        cursor.close()
        connection.close()

@bot.message_handler(func=lambda message: message.text in ['Play with bot 🤖', 'Play between two users 👥'])
def game_setup(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    mode = 'AI' if message.text == 'Play with bot 🤖' else 'PvP'
    opponent_id = 'AI' if mode == 'AI' else None

    if mode == 'PvP':
        if len(user_queue) > 0:
            opponent_id = user_queue.pop(0)
        else:
            user_queue.append(user_id)
            bot.send_message(chat_id, "PLEASE WAIT SECOND GAMER 👩🏼‍💻")
            return

    user_game_states[user_id] = {'opponent': opponent_id, 'user_score': 0, 'opponent_score': 0, 'round': 1, 'chat_id': chat_id}
    if opponent_id != 'AI':
        user_game_states[opponent_id] = {'opponent': user_id, 'user_score': 0, 'opponent_score': 0, 'round': 1, 'chat_id': bot.get_chat(opponent_id).id}
        bot.send_message(user_game_states[opponent_id]['chat_id'], "Your match is ready!")
        send_options(user_game_states[opponent_id]['chat_id'])
    send_options(chat_id)

def send_options(chat_id):
    markup = types.InlineKeyboardMarkup()
    for key, emoji in choices.items():
        markup.add(types.InlineKeyboardButton(text=f"{emoji} {key}", callback_data=key))
    bot.send_message(chat_id, "CHOOSE YOUR OPTION 👇", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in choices)
def handle_choice(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    user_move = call.data
    user_state = user_game_states.get(user_id)

    if user_state['opponent'] == 'AI':
        opponent_move = random.choice(list(choices.keys()))
        result = determine_winner(user_move, opponent_move)
        update_scores_and_respond(user_id, chat_id, user_move, opponent_move, result, ai=True)
    else:
        opponent_id = user_state['opponent']
        opponent_state = user_game_states.get(opponent_id)
        opponent_move = opponent_state.get('move', None)
        if opponent_move:
            result = determine_winner(user_move, opponent_move)
            update_scores_and_respond(user_id, chat_id, user_move, opponent_move, result)
            update_scores_and_respond(opponent_id, opponent_state['chat_id'], opponent_move, user_move, 'opponent' if result == 'user' else 'user')
            opponent_state.pop('move', None)
            user_state.pop('move', None)
        else:
            user_state['move'] = user_move
            bot.answer_callback_query(call.id, "PLEASE WAIT FOR YOUR OPPONENT.")

def determine_winner(user_move, opponent_move):
    rules = {'Rock': 'Scissors', 'Paper': 'Rock', 'Scissors': 'Paper'}
    if user_move == opponent_move:
        return 'tie'
    elif rules[user_move] == opponent_move:
        return 'user'
    else:
        return 'opponent'

def update_scores_and_respond(user_id, chat_id, user_move, opponent_move, result, ai=False):
    user = user_game_states[user_id]
    user['user_score'] += 1 if result == 'user' else 0
    user['opponent_score'] += 1 if result == 'opponent' else 0
    round_end_msg = "Round over! " if user['round'] == 3 else ""

    message = f"{round_end_msg} YOUR CHOICE: {choices[user_move]}  SECOND MEMBER CHOICE: {choices[opponent_move]}"
    if result == 'user':
        message += " YOU WIN 🥳"
    elif result == 'opponent':
        message += "YOU LOSE 😔, Don't be upset"
    else:
        message += " IT IS TIE 😮‍💨"

    bot.send_message(chat_id, message)
    if user['round'] >= 3:
        finalize_game(user_id, 'AI' if ai else user['opponent'])
    else:
        user['round'] += 1
        send_options(chat_id)

def finalize_game(user_id, opponent):
    user = user_game_states[user_id]
    chat_id = user['chat_id']
    user_score = user['user_score']
    opponent_score = user['opponent_score']
    if opponent == 'AI':
        winner = 'User' if user_score > opponent_score else 'AI' if user_score < opponent_score else 'Tie'
        save_game_results_to_db(user_id, bot.get_chat(user_id).username, None, 'AI', winner, user_score, opponent_score)
    else:
        opponent_data = user_game_states[opponent]
        opponent_chat_id = opponent_data['chat_id']
        winner = 'User' if user_score > opponent_score else 'Opponent' if user_score < opponent_score else 'Tie'
        save_game_results_to_db(user_id, bot.get_chat(user_id).username, opponent, bot.get_chat(opponent).username, winner, user_score, opponent_score)
        bot.send_message(opponent_chat_id, f"GAME OVER! SCORES - YOU: {opponent_score}, SECOND GAMER: {user_score}. WINNER: {winner} 🏆")
        user_game_states.pop(opponent, None)

    bot.send_message(chat_id, f"GAME OVER! SCORES - YOU: {user_score}, SECOND GAMER: {'AI' if opponent == 'AI' else opponent_score}. WINNER: {winner} 🤩")
    user_game_states.pop(user_id, None)

def save_game_results_to_db(user_id, username, opponent_id, opponent_username, winner, user_score, opponent_score):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO game_results (user_id, username, opponent_id, opponent_username, winner, user_score, opponent_score) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (user_id, username, opponent_id, opponent_username, winner, user_score, opponent_score))
        connection.commit()
    finally:
        cursor.close()
        connection.close()

bot.polling()



#
# import telebot
# from telebot import types
# import random
# import mysql.connector
# from mysql.connector import Error
#
# API_TOKEN = '6837439077:AAGaEwhRZCEuN6UGgIF8KKQkNG-DxemOvJg'
# bot = telebot.TeleBot(API_TOKEN)
#
# def create_connection():
#     return mysql.connector.connect(
#         host='localhost',
#         database='korzinka',
#         user='root',
#         password='5members'
#     )
#
# def create_table():
#     connection = create_connection()
#     try:
#         cursor = connection.cursor()
#         cursor.execute("""
#         CREATE TABLE IF NOT EXISTS game_results (
#             game_no INT AUTO_INCREMENT PRIMARY KEY,
#             user_id BIGINT,
#             opponent_id BIGINT,
#             username VARCHAR(255),
#             opponent_username VARCHAR(255),
#             winner VARCHAR(255),
#             user_score INT,
#             opponent_score INT,
#             tie BOOLEAN,
#             game_time_seconds INT,
#             game_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             game_end TIMESTAMP
#         )""")
#         connection.commit()
#     finally:
#         cursor.close()
#         connection.close()
#
# create_table()
#
# choices = {"Rock": "ROCK✊", "Paper": "PAPER✋", "Scissors": "SCISSORS✌️"}
# user_game_states = {}
# user_queue = []
#
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     itembtn1 = types.InlineKeyboardButton('Play with bot 🤖', callback_data="play_with_bot")
#     itembtn2 = types.InlineKeyboardButton('Play between two users 👥', callback_data="play_between_users")
#     markup.add(itembtn1, itembtn2)
#     bot.send_message(message.chat.id, "ASSALOMU ALAYKUM 👋\n ☺️ ARE YOU READY PLAY ROCK, PAPER, SCISSORS?", reply_markup=markup)
#
# # @bot.message_handler(func=lambda message: message.text == 'Records 📊')
# # def show_records(message):
# #     send_statistics(message)
# #
# # @bot.message_handler(func=lambda message: message.text == 'Analytics 📈')
# # def show_analytics(message):
# #     send_analytics(message)
#
# def send_statistics(message):
#     user_id = message.from_user.id
#     stats = fetch_statistics(user_id)
#     if stats and stats['total_games'] > 0:
#         response = (f"📊 Your Game Statistics 📊\n"
#                     f"Total Games: {stats['total_games']}\n"
#                     f"Wins: {stats['wins']}\n"
#                     f"Losses: {stats['losses']}\n"
#                     f"Ties: {stats['ties']}")
#     else:
#         response = "No game statistics available. Start playing to gather data!"
#     bot.send_message(message.chat.id, response)
#
# def fetch_statistics(user_id):
#     connection = create_connection()
#     try:
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT
#                 COUNT(*) AS total_games,
#                 SUM(CASE WHEN winner = %s THEN 1 ELSE 0 END) AS wins,
#                 SUM(CASE WHEN winner != %s AND winner != 'Tie' THEN 1 ELSE 0 END) AS losses,
#                 SUM(CASE WHEN tie = TRUE THEN 1 ELSE 0 END) AS ties
#             FROM game_results
#             WHERE user_id = %s
#         """, (user_id, user_id, user_id))
#         stats = cursor.fetchone()
#         return stats if stats else {'total_games': 0, 'wins': 0, 'losses': 0, 'ties': 0}
#     finally:
#         cursor.close()
#         connection.close()
#
# def send_analytics(message):
#     user_id = message.from_user.id
#     analytics = fetch_analytics(user_id)
#     if analytics:
#         response = (f"📈 Detailed Analytics 📈\n"
#                     f"Highest Score: {analytics['highest_score']}\n"
#                     f"Lowest Score: {analytics['lowest_score']}\n"
#                     f"Average Score: {analytics['average_score']:.2f}\n"
#                     f"Total Games: {analytics['total_games']}")
#     else:
#         response = "No detailed analytics available. Start playing to gather data!"
#     bot.send_message(message.chat.id, response)
#
# def fetch_analytics(user_id):
#     connection = create_connection()
#     try:
#         cursor = connection.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT
#                 MAX(user_score) AS highest_score,
#                 MIN(user_score) AS lowest_score,
#                 AVG(user_score) AS average_score,
#                 COUNT(*) AS total_games
#             FROM game_results
#             WHERE user_id = %s
#         """, (user_id,))
#         analytics = cursor.fetchone()
#         return analytics if analytics['total_games'] > 0 else None
#     finally:
#         cursor.close()
#         connection.close()
#
# @bot.message_handler(func=lambda message: message.text in ['Play with bot 🤖', 'Play between two users 👥'])
# def game_setup(message):
#     user_id = message.from_user.id
#     chat_id = message.chat.id
#     mode = 'AI' if message.text == 'Play with bot 🤖' else 'PvP'
#     opponent_id = 'AI' if mode == 'AI' else None
#
#     if mode == 'PvP':
#         if len(user_queue) > 0:
#             opponent_id = user_queue.pop(0)
#         else:
#             user_queue.append(user_id)
#             bot.send_message(chat_id, "PLEASE WAIT SECOND GAMER 👩🏼‍💻")
#             return
#
#     user_game_states[user_id] = {'opponent': opponent_id, 'user_score': 0, 'opponent_score': 0, 'round': 1, 'chat_id': chat_id}
#     if opponent_id != 'AI':
#         user_game_states[opponent_id] = {'opponent': user_id, 'user_score': 0, 'opponent_score': 0, 'round': 1, 'chat_id': bot.get_chat(opponent_id).id}
#         bot.send_message(user_game_states[opponent_id]['chat_id'], "Your match is ready!")
#         send_options(user_game_states[opponent_id]['chat_id'])
#     send_options(chat_id)
#
# def send_options(chat_id):
#     markup = types.InlineKeyboardMarkup()
#     for key, emoji in choices.items():
#         markup.add(types.InlineKeyboardButton(text=f"{emoji} {key}", callback_data=key))
#     bot.send_message(chat_id, "CHOOSE YOUR OPTION 👇", reply_markup=markup)
#
# @bot.callback_query_handler(func=lambda call: call.data in choices)
# def handle_choice(call):
#     user_id = call.from_user.id
#     chat_id = call.message.chat.id
#     user_move = call.data
#     user_state = user_game_states.get(user_id)
#
#     if user_state['opponent'] == 'AI':
#         opponent_move = random.choice(list(choices.keys()))
#         result = determine_winner(user_move, opponent_move)
#         update_scores_and_respond(user_id, chat_id, user_move, opponent_move, result, ai=True)
#     else:
#         opponent_id = user_state['opponent']
#         opponent_state = user_game_states.get(opponent_id)
#         opponent_move = opponent_state.get('move', None)
#         if opponent_move:
#             result = determine_winner(user_move, opponent_move)
#             update_scores_and_respond(user_id, chat_id, user_move, opponent_move, result)
#             update_scores_and_respond(opponent_id, opponent_state['chat_id'], opponent_move, user_move, 'opponent' if result == 'user' else 'user')
#             opponent_state.pop('move', None)
#             user_state.pop('move', None)
#         else:
#             user_state['move'] = user_move
#             bot.answer_callback_query(call.id, "PLEASE WAIT FOR YOUR OPPONENT.")
#
# def determine_winner(user_move, opponent_move):
#     rules = {'Rock': 'Scissors', 'Paper': 'Rock', 'Scissors': 'Paper'}
#     if user_move == opponent_move:
#         return 'tie'
#     elif rules[user_move] == opponent_move:
#         return 'user'
#     else:
#         return 'opponent'
#
# def update_scores_and_respond(user_id, chat_id, user_move, opponent_move, result, ai=False):
#     user = user_game_states[user_id]
#     user['user_score'] += 1 if result == 'user' else 0
#     user['opponent_score'] += 1 if result == 'opponent' else 0
#     round_end_msg = "Round over! " if user['round'] == 3 else ""
#
#     message = f"{round_end_msg} YOUR CHOICE: {choices[user_move]}  SECOND MEMBER CHOICE: {choices[opponent_move]}"
#     if result == 'user':
#         message += " YOU WIN 🥳"
#     elif result == 'opponent':
#         message += "YOU LOSE 😔, Don't be upset"
#     else:
#         message += " IT IS TIE 😮‍💨"
#
#     bot.send_message(chat_id, message)
#     if user['round'] >= 3:
#         finalize_game(user_id, 'AI' if ai else user['opponent'])
#     else:
#         user['round'] += 1
#         send_options(chat_id)
#
# def finalize_game(user_id, opponent):
#     user = user_game_states[user_id]
#     chat_id = user['chat_id']
#     user_score = user['user_score']
#     opponent_score = user['opponent_score']
#     if opponent == 'AI':
#         winner = 'User' if user_score > opponent_score else 'AI' if user_score < opponent_score else 'Tie'
#         save_game_results_to_db(user_id, bot.get_chat(user_id).username, None, 'AI', winner, user_score, opponent_score)
#     else:
#         opponent_data = user_game_states[opponent]
#         opponent_chat_id = opponent_data['chat_id']
#         winner = 'User' if user_score > opponent_score else 'Opponent' if user_score < opponent_score else 'Tie'
#         save_game_results_to_db(user_id, bot.get_chat(user_id).username, opponent, bot.get_chat(opponent).username, winner, user_score, opponent_score)
#         bot.send_message(opponent_chat_id, f"GAME OVER! SCORES - YOU: {opponent_score}, SECOND GAMER: {user_score}. WINNER: {winner} 🏆")
#         user_game_states.pop(opponent, None)
#
#     bot.send_message(chat_id, f"GAME OVER! SCORES - YOU: {user_score}, SECOND GAMER: {'AI' if opponent == 'AI' else opponent_score}. WINNER: {winner} 🤩")
#     user_game_states.pop(user_id, None)
#
# def save_game_results_to_db(user_id, username, opponent_id, opponent_username, winner, user_score, opponent_score):
#     connection = create_connection()
#     cursor = connection.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO game_results (user_id, username, opponent_id, opponent_username, winner, user_score, opponent_score) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#             (user_id, username, opponent_id, opponent_username, winner, user_score, opponent_score))
#         connection.commit()
#     finally:
#         cursor.close()
#         connection.close()
#
# bot.polling()
#
