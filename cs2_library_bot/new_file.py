#
# ########__________LIBRARY___BOT__LAST__CODE____REGISTER___#######
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import telebot
from telebot import types
from google_sheets import *

# # Google Sheets API setup
# SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# SAMPLE_SPREADSHEET_ID = "1bOCJvUa8wTdhbxSxEeb6IWi2drfcTMGZYXlwC3j4ZVo"
#
# TOKEN = "7005024345:AAEoA6Ov-nXKQKt3YN74RAZpo7zz4CnaG08"
# bot = telebot.TeleBot(TOKEN)
#
# # Global variable to store the total number of registered users
# user_counter = 0
# # Global variable to store the registration state for each user
# registration_status = {}
# def get_next_user_id():
#     """Generate the next user ID."""
#     global user_counter
#     user_counter += 1
#     return user_counter
#
# def add_user_to_google_sheets(user_id, username, password):
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())
#
#     try:
#         service = build("sheets", "v4", credentials=creds)
#         sheet = service.spreadsheets()
#         values = [[user_id, username, password]]
#         body = {"values": values}
#         result = (
#             sheet.values()
#             .append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Sheet1!A1", valueInputOption="USER_ENTERED", body=body)
#             .execute()
#         )
#         print("User added to Google Sheets:", result)
#     except HttpError as err:
#         print("Error adding user to Google Sheets:", err)
#
# # Start Menu Functionality: send initial options
# def start_menu(chat_id):
#     keyboard = types.ReplyKeyboardMarkup(row_width=1)
#     mu_library_button = types.KeyboardButton('MU_LIBRARY 🏢')
#     world_book_button = types.KeyboardButton('WORLD_BOOKS 🌍')
#     amazon_books_button = types.KeyboardButton('AMAZON_BOOKS 📚')
#     keyboard.add(mu_library_button, world_book_button, amazon_books_button)
#     bot.send_message(chat_id, "Choose one of the options below:", reply_markup=keyboard)
#
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     # keyboard = types.ReplyKeyboardMarkup(row_width=1)
#     # mu_library_button = types.KeyboardButton('MU_LIBRARY 🏢')
#     # world_book_button = types.KeyboardButton('WORLD_BOOKS 🌍')
#     # amazon_books_button = types.KeyboardButton('AMAZON_BOOKS 📚')
#     # keyboard.add(mu_library_button, world_book_button,amazon_books_button)
#     channel_link = "https://t.me/MillatUmidi_library"
#     join_message = f"ASSALOMU ALAYKUM\n\nWELCOME TO OUR BOT👋,\n\n✅ THIS BOT HELPS YOU SEARCHING  BOOKS YOU WANT 📚\n" \
#                    f"\n✅ YOU CAN SEARCH BOOKS FOR BOOKS OF MILLAT UMIDI UNIVERSITY 🏢 \nAND ALL THE BOOKS IN THE WORLD 🌍 !" \
#                    f"\n\nOUR CHANEL LINK 👇, PLEASE JOIN❗️\n{channel_link}\n"
#     bot.reply_to(message,join_message)
#     start_menu(message.chat.id)
#
# @bot.message_handler(func=lambda message: message.text == "MU_LIBRARY 🏢")
# def mu_library_meesage(message):
#     with open("mu_lib (1).png", "rb") as image_file:
#         bot.send_photo(message.chat.id, image_file)
#     mu_library_options(message)
# def mu_library_options(message):
#     keyboard = types.ReplyKeyboardMarkup(row_width=1)
#     register_button = types.KeyboardButton("✅ REGISTER 📝")
#     books_mu_library = types.KeyboardButton("✅ AVAILABLE BOOKS IN MU LIBRARY 📚")
#     books_mu_faculty = types.KeyboardButton("✅ BOOKS FOR MU FACULTIES 🗂")
#     back_button = types.KeyboardButton("Back ↩️")
#     keyboard.add(register_button,books_mu_library,books_mu_faculty,back_button)
#     bot.send_message(message.chat.id, "Hello, We are happy🥰 with your choice,\n 🤗Welcome to MILLAT UMIDI University",reply_markup=keyboard)
#
# @bot.message_handler(func=lambda message: message.text == "Back ↩️")
# def handle_back(message):
#     start_menu(message.chat.id)
#
# @bot.message_handler(func=lambda message: message.text == "✅ REGISTER 📝")
# def register_handler(message):
#     # Set registration status to True for this user
#     registration_status[message.chat.id] = True
#     bot.send_message(message.chat.id,
#     "Please enter your username and password separated by space (e.g., username password):")
#
# @bot.message_handler(func=lambda message: True)
# def process_message(message):
#     # Check if the user is in registration process
#     if registration_status.get(message.chat.id):
#         process_registration(message)
#     else:
#         # Handle other messages appropriately
#         if message.text == "MU_LIBRARY 🏢":
#             mu_library_options(message)
#         elif message.text == "✅ AVAILABLE BOOKS IN MU LIBRARY 📚":
#             send_search_options(message.chat.id, "For Book")
#         elif message.text == "✅ BOOKS FOR MU FACULTIES 🗂":
#             books_mu_faculty_options(message.chat.id)
#         elif message.text == "WORLD_BOOKS 🌍":
#             world_books_options(message)
#         elif message.text == "AMAZON_BOOKS 📚":
#             amazon_books_options(message)
#         # else:
#         #     bot.send_message(message.chat.id,
#         #                      "Sorry, I didn't understand that. Please choose one of the available options.")
# def process_registration(message):
#     registration_data = message.text.split()
#     if len(registration_data) == 2:
#         username, password = registration_data
#         user_id = get_next_user_id()
#         add_user_to_google_sheets(user_id, username, password)
#         send_registration_options(message.chat.id)
#         # Reset registration status for this user
#         registration_status[message.chat.id] = False
#     else:
#         bot.send_message(message.chat.id, "Invalid input. Please enter your username and password separated by space.")
#
# def send_registration_options(chat_id):
#     keyboard = types.InlineKeyboardMarkup()
#     for_book_button = types.InlineKeyboardButton("For Book📚", callback_data='For_Book')
#     for_coworking_room_button = types.InlineKeyboardButton("For Co-Working-Room🏢", callback_data='For_Co-Working-Room')
#     keyboard.add(for_book_button, for_coworking_room_button)
#     bot.send_message(chat_id, "Registration successful! Choose an option:", reply_markup=keyboard)
#
# # Callback handler for registration options
# @bot.callback_query_handler(func=lambda call: call.data.startswith('For_'))
# def register_options(call):
#     registering_options = call.data.split('_')[1]
#     if registering_options == "Book":
#         send_options_book(call.message.chat.id, "For Book")
#     elif registering_options == "Co-Working-Room":
#         send_options_room(call.message.chat.id, "For Co-Working-Room")
#
# # Function for sending options for Book
# def send_options_book(chat_id, registering_options):
#     keyboard = types.InlineKeyboardMarkup()
#     title_search = types.InlineKeyboardButton('Title', callback_data='title')
#     author_search = types.InlineKeyboardButton('Author', callback_data='author')
#     isbn_search = types.InlineKeyboardButton('ISBN', callback_data='isbn')
#     keyboard.add(title_search, author_search, isbn_search)
#     bot.send_message(chat_id, f"CHOOSE 👇, YOU CAN SEARCH BOOKS FOR {registering_options} 🗂:", reply_markup=keyboard)
#
# # Function for sending options for Co-Working-Room
# def send_options_room(chat_id, registering_options):
#     keyboard = types.InlineKeyboardMarkup()
#     c_rooms = types.InlineKeyboardButton("C build", callback_data='c_build')
#     b_rooms = types.InlineKeyboardButton("B build", callback_data='b_build')
#     keyboard.add(c_rooms, b_rooms)
#     bot.send_message(chat_id, f"CHOOSE BUILDING👇{registering_options}", reply_markup=keyboard)
#
# @bot.message_handler(func=lambda message: message.text == "✅ BOOKS FOR MU FACULTIES 🗂")
# def books_mu_faculty_options(chat_id):
#     keyboard = types.InlineKeyboardMarkup()
#     aaf_faculty = types.InlineKeyboardButton('AAF faculty', callback_data='faculty_aaf')
#     ba_faculty = types.InlineKeyboardButton('BA faculty', callback_data='faculty_ba')
#     btec_faculty = types.InlineKeyboardButton('BTEC faculty', callback_data='faculty_btec')
#     it_faculty = types.InlineKeyboardButton('IT faculty', callback_data='faculty_it')
#     elt_faculty = types.InlineKeyboardButton('ELT faculty', callback_data='faculty_elt')
#     keyboard.add(aaf_faculty, ba_faculty, btec_faculty, it_faculty, elt_faculty)
#     bot.send_message(chat_id, "MU FACULTIES 🗂,\nCHOOSE YOUR FACULTY 📲, 👇", reply_markup=keyboard)
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith('faculty_'))
# def faculty_selected(call):
#     faculty_name = call.data.split('_')[1]
#     if faculty_name == 'aaf':
#         send_search_options(call.message.chat.id, "AAF faculty")
#     elif faculty_name == 'ba':
#         send_search_options(call.message.chat.id, "BA faculty")
#     elif faculty_name == 'btec':
#         send_search_options(call.message.chat.id, "BTEC faculty")
#     elif faculty_name == 'it':
#         send_search_options(call.message.chat.id, "IT faculty")
#     elif faculty_name == 'elt':
#         send_search_options(call.message.chat.id, "ELT faculty")
# def send_search_options(chat_id, faculty_name):
#     keyboard = types.InlineKeyboardMarkup()
#     title_button = types.InlineKeyboardButton('📙 TITLE', callback_data='title')
#     isbn_button = types.InlineKeyboardButton('🔢 ISBN', callback_data='isbn')
#     author_button = types.InlineKeyboardButton('📝👤 AUTHOR', callback_data='author')
#     keyboard.add(title_button, isbn_button, author_button)
#     bot.send_message(chat_id, f"CHOOSE 👇,  YOU CAN SEARCH BOOKS FOR {faculty_name.upper()} 🗂:", reply_markup=keyboard)
#
# @bot.callback_query_handler(func=lambda call: call.data in ['title', 'isbn', 'author'])
# def search_option_selected(call):
#     bot.send_message(call.message.chat.id, f"You selected: {call.data} ✅")
#
# @bot.message_handler(func=lambda message: message.text == "✅ AVAILABLE BOOKS IN MU LIBRARY 📚")
# def books_in_mu_library(message):
#     keybord = types.InlineKeyboardMarkup()
#     search_title = types.InlineKeyboardButton('📙 TITLE', callback_data='search_by_title')
#     search_author = types.InlineKeyboardButton('📝👤 AUTHOR', callback_data='search_by_author')
#     search_isbn = types.InlineKeyboardButton(' 🔢 ISBN', callback_data='search_by_isbn')
#     keybord.add(search_title,search_author,search_isbn)
#     bot.send_message(message.chat.id, "CHOOSE 👇, YOUR CAN SEARCH BOOKS BY COMFORTABLE BUTTONS 📱", reply_markup=keybord)
#
# @bot.message_handler(func=lambda message: message.text == "WORLD_BOOKS 🌍")
# def world_books_message(message):
#     with open("world_books (2).png", "rb") as image_file:
#         bot.send_photo(message.chat.id, image_file)
#     world_books_options(message)
# def world_books_options(message):
#     keybord = types.ReplyKeyboardMarkup(row_width=1)
#     search_title = types.KeyboardButton("Search by TITLE 📙")
#     search_author = types.KeyboardButton("Search by AUTHOR 📝👤")
#     search_isbn = types.KeyboardButton("Search by ISBN 🔢")
#     back_button = types.KeyboardButton("Back ↩️")
#     keybord.add(search_title, search_author, search_isbn,back_button)
#     bot.send_message(message.chat.id, "HELLO 👋 \n✅ YOU CAN SEARCH ALL THE BOOKS IN THE WORLD 🌍\nCHOOSE YOUR OPTION 👇", reply_markup=keybord)
#
# @bot.message_handler(func=lambda message: message.text == "AMAZON_BOOKS 📚")
# def amazon_books_message(message):
#     with open("amazon_books.png", "rb") as image_file:
#         bot.send_photo(message.chat.id, image_file)
#     amazon_books_options(message)
# def amazon_books_options(message):
#     keybord = types.ReplyKeyboardMarkup(row_width=1)
#     search_title = types.KeyboardButton("Search by TITLE 📙")
#     search_author = types.KeyboardButton("Search by AUTHOR 📝👤")
#     search_isbn = types.KeyboardButton("Search by ISBN 🔢")
#     back_button = types.KeyboardButton("Back ↩️")
#     keybord.add(search_title, search_author, search_isbn,back_button)
#     bot.send_message(message.chat.id, "HELLO 👋\n✅ YOU CAN TAKE PRICE💳 OF BOOKS OR SOME INFORMATION ABOUT BOOKS 📚", reply_markup=keybord)
#
#
# import requests
# import json
# import boto3  # Assuming you're using Python and boto3 library for AWS interaction
#
# # Replace these with your actual Amazon credentials and Associate Tag
# ACCESS_KEY_ID = "975050125323"
# SECRET_ACCESS_KEY = "YOUR_SECRET_ACCESS_KEY"
# ASSOCIATE_TAG = "YOUR_ASSOCIATE_TAG"
# def get_books_by_title(title):
#     """
#     Searches for books using the ItemSearch operation based on the provided title.
#
#     Args:
#         title (str): The title of the book to search for.
#
#     Returns:
#         list: A list of book information dictionaries or None if no results found.
#     """
#
#     client = boto3.client('advertising-products-api',
#                           aws_access_key_id=ACCESS_KEY_ID,
#                           aws_secret_access_key=SECRET_ACCESS_KEY)
#
#     try:
#         response = client.item_search(
#             Keywords=title,
#             SearchIndex="Books",
#             AssociateTag=ASSOCIATE_TAG,
#             ResponseGroup="ItemAttributes,Images"
#         )
#
#         if response['Items']['TotalResults'] == 0:
#             return None
#
#         return response['Items']['Item']
#     except Exception as e:
#         print(f"Error searching books by title: {e}")
#         return None
#
# def get_book_by_isbn(isbn):
#     """
#     Retrieves detailed information about a specific book using the ItemLookup operation.
#
#     Args:
#         isbn (str): The ISBN of the book to search for.
#
#     Returns:
#         dict: A dictionary containing detailed book information or None if not found.
#     """
#
#     client = boto3.client('advertising-products-api',
#                           aws_access_key_id=ACCESS_KEY_ID,
#                           aws_secret_access_key=SECRET_ACCESS_KEY)
#
#     try:
#         response = client.item_lookup(
#             ItemId=isbn,
#             SearchIndex="Books",
#             AssociateTag=ASSOCIATE_TAG,
#             ResponseGroup="ItemAttributes,Images"
#         )
#
#         return response['Items']['Item'][0]
#     except Exception as e:
#         print(f"Error searching book by ISBN: {e}")
#         return None
#
# def format_book_message(book):
#     """
#     Formats the extracted book information into a user-friendly message.
#
#     Args:
#         book (dict): A dictionary containing book information.
#
#     Returns:
#         str: A formatted message with book details.
#     """
#
#     title = book['ItemAttributes']['Title']
#     author = book['ItemAttributes']['Author']
#     price = book['ItemAttributes']['ListPrice']['Amount']
#     image_url = book['ItemAttributes']['LargeImage']['URL']
#
#     message = f"Title: {title}\n"
#     message += f"Author: {author}\n"
#     message += f"Price: ${price}\n"
#     message += f"Image: {image_url}"
#
#     return message
#
# @bot.message_handler(func=lambda message: message.text == "AMAZON_BOOKS 📚")
# def amazon_books_message(message):
#     keyboard = types.ReplyKeyboardMarkup(row_width=1)
#     search_title = types.KeyboardButton("Search by TITLE 📙")
#     search_author = types.KeyboardButton("Search by AUTHOR 📝👤")
#     search_isbn = types.KeyboardButton("Search by ISBN 🔢")
#     back_button = types.KeyboardButton("Back ↩️")
#     keyboard.add(search_title, search_author, search_isbn, back_button)
#     bot.send_message(message.chat.id, "HELLO 👋\n✅ YOU CAN TAKE PRICE💳 OF BOOKS OR SOME INFORMATION ABOUT BOOKS 📚", reply_markup=keyboard)
#
# @bot.message_handler(func=lambda message: message.text == "Search by TITLE 📙")
# def search_by_title(message):
#     bot.send_message(message.chat.id, "Enter the book title:")
#
# @bot.message_handler(func=lambda message: True)  # Handle any other message as a search term
# def handle_search(message):
#     search_term = message.text
#     books = get_books_by_title(search_term)
#
#     if books is None:
#         bot.send_message(message.chat.id, f"No books found matching '{search_term}'.")
#     else:
#         for book in books:
#             book_message = format_book_message(book)
#             bot.send_message(message.chat.id, book_message)
#
#
# bot.polling(timeout=60)

import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import telebot
from telebot import types

# Google Sheets API setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SAMPLE_SPREADSHEET_ID = "1bOCJvUa8wTdhbxSxEeb6IWi2drfcTMGZYXlwC3j4ZVo"

# Telegram bot setup
TOKEN = "7005024345:AAEoA6Ov-nXKQKt3YN74RAZpo7zz4CnaG08"
bot = telebot.TeleBot(TOKEN)

# Dictionary to store registration status for each user
registration_status = {}

# Start Menu Functionality: send initial options
def start_menu(chat_id):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    mu_library_button = types.KeyboardButton('MU_LIBRARY 🏢')
    world_book_button = types.KeyboardButton('WORLD_BOOKS 🌍')
    amazon_books_button = types.KeyboardButton('AMAZON_BOOKS 📚')
    keyboard.add(mu_library_button, world_book_button, amazon_books_button)
    bot.send_message(chat_id, "Choose one of the options below:", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start_message(message):
    # keyboard = types.ReplyKeyboardMarkup(row_width=1)
    # mu_library_button = types.KeyboardButton('MU_LIBRARY 🏢')
    # world_book_button = types.KeyboardButton('WORLD_BOOKS 🌍')
    # amazon_books_button = types.KeyboardButton('AMAZON_BOOKS 📚')
    # keyboard.add(mu_library_button, world_book_button,amazon_books_button)
    channel_link = "https://t.me/MillatUmidi_library"
    join_message = f"ASSALOMU ALAYKUM\n\nWELCOME TO OUR BOT👋,\n\n✅ THIS BOT HELPS YOU SEARCHING  BOOKS YOU WANT 📚\n" \
                   f"\n✅ YOU CAN SEARCH BOOKS FOR BOOKS OF MILLAT UMIDI UNIVERSITY 🏢 \nAND ALL THE BOOKS IN THE WORLD 🌍 !" \
                   f"\n\nOUR CHANEL LINK 👇, PLEASE JOIN❗️\n{channel_link}\n"
    bot.reply_to(message,join_message)
    start_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "MU_LIBRARY 🏢")
def mu_library_meesage(message):
    with open("mu_lib (1).png", "rb") as image_file:
        bot.send_photo(message.chat.id, image_file)
    mu_library_options(message)
def mu_library_options(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    register_button = types.KeyboardButton("✅ REGISTER 📝")
    books_mu_library = types.KeyboardButton("✅ AVAILABLE BOOKS IN MU LIBRARY 📚")
    books_mu_faculty = types.KeyboardButton("✅ BOOKS FOR MU FACULTIES 🗂")
    back_button = types.KeyboardButton("Back ↩️")
    keyboard.add(register_button,books_mu_library,books_mu_faculty,back_button)
    bot.send_message(message.chat.id, "Hello, We are happy🥰 with your choice,\n 🤗Welcome to MILLAT UMIDI University",reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Back ↩️")
def handle_back(message):
    start_menu(message.chat.id)

# Function to get Google Sheets credentials
def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

# Function to add registration data to Google Sheets
def add_registration_to_google_sheets(user_id, surname, name, phone, book_name, date):
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet_id = SAMPLE_SPREADSHEET_ID
    range_name = 'Registrations'  # Specify the range where you want to add the registration data
    value_input_option = 'RAW'
    row = [user_id, surname, name, phone, book_name, date]
    body = {'values': [row]}
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()

# Function to add room booking data to Google Sheets
def add_room_booking_to_google_sheets(user_id, building, room_number, date):
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    sheet_id = SAMPLE_SPREADSHEET_ID
    range_name = 'RoomBookings'  # Specify the range where you want to add the room booking data
    value_input_option = 'RAW'
    row = [user_id, building, room_number, date]
    body = {'values': [row]}
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()


# Handler for the registration button
@bot.message_handler(func=lambda message: message.text == "✅ REGISTER 📝")
def register_handler(message):
    registration_status[message.chat.id] = True
    send_registration_options(message.chat.id)


# Function to send registration options
def send_registration_options(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    booking_books_button = types.InlineKeyboardButton("Booking Books📚", callback_data='booking_books')
    booking_coworking_room_button = types.InlineKeyboardButton("Booking Co-Working Room🏢",
                                                               callback_data='booking_coworking_room')
    keyboard.add(booking_books_button, booking_coworking_room_button)
    bot.send_message(chat_id, "Choose an option:", reply_markup=keyboard)


# Callback handler for registration options
@bot.callback_query_handler(func=lambda call: call.data.startswith('booking_'))
def register_options(call):
    booking_option = call.data.split('_')[1]
    if booking_option == "books":
        send_booking_form(call.message.chat.id, "For Book")
    elif booking_option == "coworking_room":
        send_building_options(call.message.chat.id, "For Co-Working Room")


# Function to send options for Booking Books
def send_booking_form(chat_id, registering_options):
    bot.send_message(chat_id, "Please enter the following details for booking books:")
    bot.send_message(chat_id, "Surname:")
    registration_status[chat_id] = "booking_books_surname"


# Function to send options for Booking Co-Working Room
def send_building_options(chat_id, registering_options):
    keyboard = types.InlineKeyboardMarkup()
    c_building_button = types.InlineKeyboardButton("C Building", callback_data='c_building')
    b_building_button = types.InlineKeyboardButton("B Building", callback_data='b_building')
    keyboard.add(c_building_button, b_building_button)
    bot.send_message(chat_id, "Choose a building:", reply_markup=keyboard)


# Callback handler for building selection
@bot.callback_query_handler(func=lambda call: call.data in ['c_building', 'b_building'])
def building_selected(call):
    building = call.data.split('_')[0]
    send_room_options(call.message.chat.id, building)


# Function to send options for room selection
def send_room_options(chat_id, building):
    bot.send_message(chat_id, f"Please enter the following details for booking a room in {building} Building:")
    bot.send_message(chat_id, "Room Number:")
    registration_status[chat_id] = f"booking_{building}_room_number"


# Function to handle messages during registration process
@bot.message_handler(func=lambda message: True)
def process_registration_message(message):
    chat_id = message.chat.id
    if chat_id in registration_status:
        registration_step = registration_status[chat_id]
        if registration_step == "booking_books_surname":
            registration_status[chat_id] = "booking_books_name"
            bot.send_message(chat_id, "Name:")
        elif registration_step == "booking_books_name":
            registration_status[chat_id] = "booking_books_phone"
            bot.send_message(chat_id, "Phone Number:")
        elif registration_step == "booking_books_phone":
            registration_status[chat_id] = "booking_books_book_name"
            bot.send_message(chat_id, "Book's Name:")
        elif registration_step == "booking_books_book_name":
            registration_status[chat_id] = "booking_books_date"
            bot.send_message(chat_id, "Date (YYYY-MM-DD):")
        elif registration_step == "booking_books_date":
            registration_status[chat_id] = "booking_books_password"
            bot.send_message(chat_id, "Password for registration:")
        elif registration_step == "booking_books_password":
            handle_booking_books_registration(message)
        elif registration_step.startswith("booking"):
            handle_room_booking_registration(message)


# Function to handle booking books registration
def handle_booking_books_registration(message):
    # Extract user input
    surname = message.text
    name = registration_status[message.chat.id.split('_')[1]]
    phone = registration_status[message.chat.id.split('_')[1]]
    book_name = registration_status[message.chat.id.split('_')[1]]
    date = registration_status[message.chat.id.split('_')[1]]

    # Add registration data to Google Sheets
    add_registration_to_google_sheets(message.chat.id, surname, name, phone, book_name, date)

    # Inform user about successful registration
    bot.send_message(message.chat.id, "You have successfully booked the book. You can take it now.")

    # Clear registration status
    del registration_status[message.chat.id]


# Function to handle room booking registration
def handle_room_booking_registration(message):
    # Extract user input
    room_number = message.text

    # Determine the building from registration status
    building = registration_status[message.chat.id].split('_')[1]
    date = registration_status[message.chat.id.split('_')[1]]
    # Add room booking data to Google Sheets
    add_room_booking_to_google_sheets(message.chat.id, building, room_number, date)

    # Inform user about successful room booking
    bot.send_message(message.chat.id, f"You have successfully booked a room in {building} Building.")

    # Clear registration status
    del registration_status[message.chat.id]


# Start the bot
bot.polling()




@bot.message_handler(func=lambda message: message.text == "✅ BOOKS FOR MU FACULTIES 🗂")
def books_mu_faculty_options(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    aaf_faculty = types.InlineKeyboardButton('AAF faculty', callback_data='faculty_aaf')
    ba_faculty = types.InlineKeyboardButton('BA faculty', callback_data='faculty_ba')
    btec_faculty = types.InlineKeyboardButton('BTEC faculty', callback_data='faculty_btec')
    it_faculty = types.InlineKeyboardButton('IT faculty', callback_data='faculty_it')
    elt_faculty = types.InlineKeyboardButton('ELT faculty', callback_data='faculty_elt')
    keyboard.add(aaf_faculty, ba_faculty, btec_faculty, it_faculty, elt_faculty)
    bot.send_message(chat_id, "MU FACULTIES 🗂,\nCHOOSE YOUR FACULTY 📲, 👇", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('faculty_'))
def faculty_selected(call):
    faculty_name = call.data.split('_')[1]
    if faculty_name == 'aaf':
        send_search_options(call.message.chat.id, "AAF faculty")
    elif faculty_name == 'ba':
        send_search_options(call.message.chat.id, "BA faculty")
    elif faculty_name == 'btec':
        send_search_options(call.message.chat.id, "BTEC faculty")
    elif faculty_name == 'it':
        send_search_options(call.message.chat.id, "IT faculty")
    elif faculty_name == 'elt':
        send_search_options(call.message.chat.id, "ELT faculty")
def send_search_options(chat_id, faculty_name):
    keyboard = types.InlineKeyboardMarkup()
    title_button = types.InlineKeyboardButton('📙 TITLE', callback_data='title')
    isbn_button = types.InlineKeyboardButton('🔢 ISBN', callback_data='isbn')
    author_button = types.InlineKeyboardButton('📝👤 AUTHOR', callback_data='author')
    keyboard.add(title_button, isbn_button, author_button)
    bot.send_message(chat_id, f"CHOOSE 👇,  YOU CAN SEARCH BOOKS FOR {faculty_name.upper()} 🗂:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['title', 'isbn', 'author'])
def search_option_selected(call):
    bot.send_message(call.message.chat.id, f"You selected: {call.data} ✅")
