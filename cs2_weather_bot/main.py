# json_object = json.dumps(city_weather, indet=1)
# with open('weather_data.json', 'w') as f:
#     f.write(json_object)
# for x, y in city_weather.items():
#     print(x,y)





# import json
# import requests
# from telegram import Chat as TGChat
# API_key = 'de7cbe734e7e1b3827bdde85fc351fb2'
# TOKEN = "7005024345:AAEoA6Ov-nXKQKt3YN74RAZpo7zz4CnaG08"
# url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=de7cbe734e7e1b3827bdde85fc351fb2'
# url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=de7cbe734e7e1b3827bdde85fc351fb2'
# city = ("asdasdasd")
# city_weather = requests.get(url.format(city)).json()
#
# from telegram.ext import *
# from telegram.ext import Updater, CommandHandler, MessageHandler, filters
# # from telegram import ParseMode
# def get_weather(city):
#     status = False
#     city_weather = requests.get(url.format(city)).json()
#     if city_weather["code'"] == "404":
#         status = city_weather
#     else:
#         my_dict = {
#             "name": city_weather["name"],
#             "description": city_weather["weather"][0]["description"],
#             "icon": city_weather["weather"][0]["icon"],
#             "temperature": city_weather["main"]["temp"]
#         }
#         status = my_dict
#     return status

# def start(update, context):
#     update.message.reply_text("Hello! I am bot. What is your city")
# def handle_message(update, context):
#     city = update.message.text.strip()
#     data = get_weather(city)
#     for x in data:
#         update.message.reply_text(f"{x}  {data[x]}!")
#
# def main():
#     updater = Updater("TOKEN", use_context=True)
#
#     dp = updater.dispatcher
#
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(MessageHandler(filters.text & ~filters.command, handle_message))
#
#     updater.start_polling()
#     updater.idle()
#
# if __name__ == '__main__':
#     main()


# import json
# import requests
# import telebot
#
# API_key = 'de7cbe734e7e1b3827bdde85fc351fb2'
# TOKEN = "7005024345:AAEoA6Ov-nXKQKt3YN74RAZpo7zz4CnaG08"
# url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=de7cbe734e7e1b3827bdde85fc351fb2'
#
# bot = telebot.TeleBot(TOKEN)
#
# def get_weather(city):
#     status = False
#     city_weather = requests.get(url.format(city)).json()
#     if city_weather.get("cod") == "404":
#         status = city_weather
#     else:
#         my_dict = {
#             "name": city_weather["name"],
#             "description": city_weather["weather"][0]["description"],
#             "icon": city_weather["weather"][0]["icon"],
#             "temperature": city_weather["main"]["temp"]
#         }
#         status = my_dict
#     return status
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.reply_to(message, "Hello! I am bot. What is your city")
#
# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     city = message.text.strip()
#     data = get_weather(city)
#     if isinstance(data, dict):
#         for key, value in data.items():
#             bot.reply_to(message, f"{key}: {value}")
#     else:
#         bot.reply_to(message, "City not found")
#
# bot.polling()

# import telebot
# import requests
#
# API_key = "de7cbe734e7e1b3827bdde85fc351fb2"
# TOKEN = "7005024345:AAEoA6Ov-nXKQKt3YN74RAZpo7zz4CnaG08"
#
# bot = telebot.TeleBot(TOKEN)
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.reply_to(message, "Welcome to the Weather Bot! Please enter the city name:")
#
# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     city = message.text.strip()
#     weather_data = get_weather(city)
#     if weather_data:
#         icon_url, temperature, description, city_name, country = weather_data
#         # Send weather information as text
#         response_message = f"{city_name}, {country}\n"
#         response_message += f"Temperature: {temperature:.2f} C\n"
#         response_message += f"Description: {description}"
#         bot.reply_to(message, response_message)
#
#         # Send weather icon as a photo
#         icon_image = requests.get(icon_url)
#         bot.send_photo(message.chat.id, icon_image.content)
#     else:
#         bot.reply_to(message, "City not found. Please enter a valid city name.")
#
# def get_weather(city):
#     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
#     res = requests.get(url)
#     if res.status_code == 404:
#         return None
#     weather = res.json()
#     icon_id = weather['weather'][0]['icon']
#     temperature = weather['main']['temp'] - 273.15
#     description = weather['weather'][0]['description']
#     city_name = weather['name']
#     country = weather['sys']['country']
#     icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
#     return icon_url, temperature, description, city_name, country
#
# bot.polling()


import telebot
import requests

API_KEY = "de7cbe734e7e1b3827bdde85fc351fb2"
TOKEN = "7005024345:AAEoA6Ov-nXKQKt3YN74RAZpo7zz4CnaG08"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to the Weather Bot! Please enter the city name:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    city = message.text.strip()
    weather_data = get_weather(city)
    if weather_data:
        icon_url, temperature, description, city_name, country_code = weather_data
        # Get the country flag emoji
        country_flag = get_country_flag(country_code)
        # Send weather information as text
        response_message = f"{city_name}, {country_flag}\n"
        response_message += f"Temperature: {temperature:.2f} C\n"
        response_message += f"Description: {description}"
        bot.reply_to(message, response_message)

        # Send weather icon as a photo
        icon_image = requests.get(icon_url)
        bot.send_photo(message.chat.id, icon_image.content)
    else:
        bot.reply_to(message, "City not found. Please enter a valid city name.")

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        icon_id = data['weather'][0]['icon']
        temperature = data['main']['temp'] - 273.15
        description = data['weather'][0]['description']
        city_name = data['name']
        country_code = data['sys']['country']
        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
        return icon_url, temperature, description, city_name, country_code
    else:
        return None

def get_country_flag(country_code):
    # Simple mapping of country codes to flag emojis
    country_flags = {
        "US": "🇺🇸",
        "UK": "🇬🇧",
        "FR": "🇫🇷",
        # Add more country codes and flag emojis as needed
    }
    return country_flags.get(country_code, "🌍")  # Return globe emoji if country code not found

bot.polling()


