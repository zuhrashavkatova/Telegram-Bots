#############____________TRUE KORZINKA CODE_____________##############
import telebot
import mysql.connector
from telebot import types

# Establish MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="5members",
    database="korzinka"
)
mycursor = mydb.cursor()

 # bot token obtained from BotFather
TOKEN = '7005024345:AAEoA6Ov-nXKQKt3YN74RAZpo7zz4CnaG08'

# Create a new Telebot instance
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=5)
    register_button = types.KeyboardButton('Register \U0001F5C2')  # 🪪
    login_button = types.KeyboardButton('Login \U0001F512')  # 🔒
    products_button = types.KeyboardButton('Products \U0001F95B \U0001F357 \U0001F35E \U0001F9C8')  # 🥛 🍗 🍞 🧈
    cart_button = types.KeyboardButton('Cart \U0001F6D2')  # 🛒
    delete_button = types.KeyboardButton('Delete product \U0001F6AB')  # 🚫
    confirm_payment_button = types.KeyboardButton('Confirm payment \U0001F4B3')  # 💳
    keyboard.add(register_button, login_button, products_button, cart_button, delete_button, confirm_payment_button)
    bot.reply_to(message, "Welcome to our store! How can I assist you today?", reply_markup=keyboard)


# Define a handler for the login message
@bot.message_handler(func=lambda message: message.text == "Login \U0001F512")
def login_message(message):
    bot.reply_to(message, "Please enter your user ID and password separated by a space.")

# Define a handler for processing login
@bot.message_handler(func=lambda message: len(message.text.split()) == 2 and message.text.split()[0].isdigit())
def process_login(message):
    user_id, password = message.text.split()
    mycursor.execute("SELECT * FROM new_users WHERE user_id = %s AND password = %s", (user_id, password))
    user = mycursor.fetchone()
    if user:
        bot.reply_to(message, "Login successful.")
        # Provide admin options here
        provide_admin_options(message)
    else:
        bot.reply_to(message, "Invalid user ID and password. Please try again.")

def provide_admin_options(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    add_product_button = types.KeyboardButton('Add Product')
    change_product_button = types.KeyboardButton('Change Product')
    change_price_button = types.KeyboardButton('Change Price')
    change_quantity_button = types.KeyboardButton('Change Quantity')
    delete_product_button = types.KeyboardButton('Delete Product')
    total_sales_button = types.KeyboardButton('Total Sales')
    keyboard.add(add_product_button, change_product_button, change_price_button, change_quantity_button, delete_product_button, total_sales_button)
    bot.reply_to(message, "Admin Panel", reply_markup=keyboard)

# Add product handler
@bot.message_handler(func=lambda message: message.text == 'Add Product')
def add_product(message):
    bot.reply_to(message,
    "Please enter details of new product in the following format: \n<product_id>, <product_name>, <price>, <quantity>")
    bot.register_next_step_handler(message, process_add_product)
def process_add_product(message):
    product_data = message.text.split(',')
    if len(product_data) == 4:
        product_id, product_name, price, quantity = product_data
        try:
            price = float(price)
            quantity = int(quantity)
            # Insert the new product into the database
            mycursor.execute(
                "INSERT INTO new_products (product_id, product_name, price, quantity) VALUES (%s, %s, %s, %s)",
                (product_id.strip(), product_name.strip(), price, quantity))
            mydb.commit()
            bot.reply_to(message, "Product added successfully!")
        except ValueError:
            bot.reply_to(message, "Invalid price or quantity. Please enter numeric values.")
    else:
        bot.reply_to(message, "Invalid format. Please enter the details in the correct format.")

# Change product handler
@bot.message_handler(func=lambda message: message.text == 'Change Product')
def change_product(message):
    bot.reply_to(message, "Please enter the ID of the product you want to change:")
    bot.register_next_step_handler(message, process_change_product_id)
def process_change_product_id(message):
    product_id = message.text.strip()
    mycursor.execute("SELECT * FROM new_products WHERE product_id = %s", (product_id,))
    product = mycursor.fetchone()
    if product:
        bot.reply_to(message, f"The current details of the product are: \nProduct Name: {product[1]}\nPrice: {product[2]}\nQuantity: {product[3]}\nPlease enter the new details in the following format: <product_name>, <price>, <quantity>")
        bot.register_next_step_handler(message, process_change_product_details, product_id)
    else:
        bot.reply_to(message, "Product not found.")

def process_change_product_details(message, product_id):
    product_data = message.text.split(',')
    if len(product_data) == 3:
        product_name, price, quantity = product_data
        try:
            price = float(price)
            quantity = int(quantity)
            # Update the product details in the database
            mycursor.execute("UPDATE new_products SET product_name = %s, price = %s, quantity = %s WHERE product_id = %s", (product_name.strip(), price, quantity, product_id))
            mydb.commit()
            bot.reply_to(message, "Product details updated successfully!")
        except ValueError:
            bot.reply_to(message, "Invalid price or quantity. Please enter numeric values.")
    else:
        bot.reply_to(message, "Invalid format. Please enter the details in the correct format.")

# Change price handler
@bot.message_handler(func=lambda message: message.text == 'Change Price')
def change_price(message):
    bot.reply_to(message, "Please enter the name of the product whose price you want to change:")
    bot.register_next_step_handler(message, process_change_price_name)
def process_change_price_name(message):
    product_name = message.text.strip()
    mycursor.execute("SELECT * FROM new_products WHERE product_name = %s", (product_name,))
    product = mycursor.fetchone()
    if product:
        bot.reply_to(message, f"The current price of the product '{product_name}' is: {product[2]}\nPlease enter the new price:")
        bot.register_next_step_handler(message, process_change_price, product_name)
    else:
        bot.reply_to(message, "Product not found.")

def process_change_price(message, product_name):
    new_price = message.text.strip()
    try:
        new_price = float(new_price)
        # Update the price of the product in the database
        mycursor.execute("UPDATE new_products SET price = %s WHERE product_name = %s", (new_price, product_name))
        mydb.commit()
        bot.reply_to(message, "Price updated successfully!")
    except ValueError:
        bot.reply_to(message, "Invalid price. Please enter a numeric value.")

# Change quantity handler
@bot.message_handler(func=lambda message: message.text == 'Change Quantity')
def change_quantity(message):
    bot.reply_to(message, "Please enter the ID of the product whose quantity you want to change:")
    bot.register_next_step_handler(message, process_change_quantity_id)

def process_change_quantity_id(message):
    product_id = message.text.strip()
    mycursor.execute("SELECT * FROM new_products WHERE product_id = %s", (product_id,))
    product = mycursor.fetchone()
    if product:
        bot.reply_to(message, f"The current quantity of the product '{product[1]}' is: {product[3]}\nPlease enter the new quantity:")
        bot.register_next_step_handler(message, process_change_quantity, product_id)
    else:
        bot.reply_to(message, "Product not found.")

def process_change_quantity(message, product_id):
    new_quantity = message.text.strip()
    try:
        new_quantity = int(new_quantity)
        # Update the quantity of the product in the database
        mycursor.execute("UPDATE new_products SET quantity = %s WHERE product_id = %s", (new_quantity, product_id))
        mydb.commit()
        bot.reply_to(message, "Quantity updated successfully!")
    except ValueError:
        bot.reply_to(message, "Invalid quantity. Please enter an integer value.")

# Delete product handler
@bot.message_handler(func=lambda message: message.text == 'Delete Product')
def delete_product(message):
    bot.reply_to(message, "Please enter the ID of the product you want to delete:")
    bot.register_next_step_handler(message, process_delete_product)

def process_delete_product(message):
    product_id = message.text.strip()
    mycursor.execute("SELECT * FROM new_products WHERE product_id = %s", (product_id,))
    product = mycursor.fetchone()
    if product:
        mycursor.execute("DELETE FROM new_products WHERE product_id = %s", (product_id,))
        mydb.commit()
        bot.reply_to(message, "Product deleted successfully!")
    else:
        bot.reply_to(message, "Product not found.")

# Total sales handler
@bot.message_handler(func=lambda message: message.text == 'Total Sales')
def total_sales(message):
    # Fetch total sales from the database
    mycursor.execute("SELECT SUM(price) FROM cart")
    total_sales = mycursor.fetchone()[0]
    if total_sales:
        bot.reply_to(message, f"Total sales: ${total_sales}")
    else:
        bot.reply_to(message, "No sales yet.")

# Define a handler for the '/register' command
# @bot.message_handler(commands=['register'])
@bot.message_handler(func=lambda message: message.text == 'Register \U0001F5C2')
def register_message(message):
    def process_registration(message):
        registration_data = message.text.split()
        if len(registration_data) == 2:  # Assuming user ID and password are provided
            user_id, password = registration_data
            mycursor.execute("SELECT user_id FROM new_users WHERE user_id = %s", (user_id,))
            if mycursor.fetchone() is None:
                sql = "INSERT INTO new_users (user_id, password) VALUES (%s, %s)"
                val = (user_id, password)
                mycursor.execute(sql, val)
                mydb.commit()
                bot.reply_to(message, "You have been registered successfully!")
            else:
                bot.reply_to(message, "You are already registered.")
        else:
            bot.reply_to(message, "Please enter your ID and password would be only numbers and separated by a space.")
    bot.reply_to(message, "Enter your ID and password with only numbers and separated by a space.")
    bot.register_next_step_handler(message, process_registration)

# Define a handler for the '/products' command
# @bot.message_handler(commands=['products'])
@bot.message_handler(func=lambda message: message.text == 'Products \U0001F95B \U0001F357 \U0001F35E \U0001F9C8')
def show_products(message):
    # Fetch products from the database
    mycursor.execute("SELECT * FROM new_products")
    products = mycursor.fetchall()
    if products:
        # Create a keyboard with product IDs as buttons
        keyboard = types.InlineKeyboardMarkup()
        for product in products:
            product_info = f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Quantity: {product[3]}"
            button = types.InlineKeyboardButton(text=product_info, callback_data=f"product_{product[0]}")
            keyboard.add(button)

        bot.reply_to(message, "Please select a product:", reply_markup=keyboard)
    else:
        bot.reply_to(message, "No products available.")

# Define a callback handler for product selection
@bot.callback_query_handler(func=lambda call: call.data.startswith('product_'))
def select_product(call):
    # Extract product ID from callback data
    product_name = call.data.split('_')[1]
    # Ask the user for the quantity
    bot.send_message(call.message.chat.id, f"Enter the quantity for product {product_name}:")
    # Register the next step handler to get the quantity
    bot.register_next_step_handler(call.message, process_quantity_input, product_name)
def process_quantity_input(message, product_id):
    # Get the quantity entered by the user
    quantity = message.text.strip()
    if not quantity.isdigit():
        bot.send_message(message.chat.id, "Invalid quantity. Please enter a number.")
        return

    quantity = int(quantity)
    # Fetch product details from the database
    mycursor.execute("SELECT product_name, price, quantity FROM new_products WHERE product_id = %s", (product_id,))
    product_details = mycursor.fetchone()
    if product_details:
        product_name, price_per_unit, available_quantity = product_details
        if available_quantity is None or quantity > available_quantity:  # Check if available quantity is None or less than desired quantity
            bot.send_message(message.chat.id, f"Sorry, only {available_quantity} units of {product_name} are available.")
            return
        total_price = price_per_unit * quantity
        bot.send_message(message.chat.id, f"Product: {product_name}\nPrice per unit: {price_per_unit}\nQuantity: {quantity}\nTotal Price: {total_price}")
        # Add the product to the cart table
        mycursor.execute("SELECT COUNT(*) FROM cart")
        row_count = mycursor.fetchone()[0]
        # Use the row count as the cart_id
        cart_id = row_count + 1
        cart_data = (int(cart_id), product_id, product_name, str(message.from_user.id), total_price, quantity)
        print(cart_data)
        mycursor.execute("INSERT INTO cart (cart_id, product_id, product_name, user_id, price, quantity) VALUES (%s, %s, %s, %s, %s, %s)",cart_data)
        mydb.commit()
        bot.send_message(message.chat.id, f"Product '{product_name}' added to cart successfully!")
    else:
        bot.send_message(message.chat.id, "Product not found.")

# Define a handler for the '/cart' command
# @bot.message_handler(commands=['cart'])
@bot.message_handler(func=lambda message: message.text == 'Cart \U0001F6D2')
def view_cart(message):
    user_id = message.from_user.id
    mycursor.execute("SELECT * FROM cart WHERE user_id = %s", (user_id,))
    cart_items = mycursor.fetchall()
    if cart_items:
        cart_info = "\n".join([f"Cart Id: {item[0]}  Product ID: {item[1]} Product Name: {item[-1]} \nUser Id:{item[2]}  Total price: ${item[3]}  Quantity: {item[4]}" for item in cart_items])
        bot.reply_to(message, f"Your Cart:\n{cart_info}")
    else:
        bot.reply_to(message, "Your cart is empty.")

@bot.message_handler(func=lambda message: message.text == 'Delete product \U0001F6AB')
def delete_product(message):
    bot.reply_to(message, "Enter the product name to delete from the cart:")
    bot.register_next_step_handler(message, process_product_name_input)
def process_product_name_input(message):
    product_name_to_delete = message.text
    sql = "DELETE FROM cart WHERE product_name = %s AND user_id = %s"
    val = (product_name_to_delete, message.from_user.id)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount > 0:
        bot.reply_to(message, "Product deleted from your cart.")
    else:
        bot.reply_to(message, "Product not found in your cart or already deleted.")

# Define a handler for the '/confirm_payment' command
# @bot.message_handler(commands=['confirm_payment'])
@bot.message_handler(func=lambda message: message.text == 'Confirm Payment \U0001F4B3')
def confirm_payment(message):
    sql = "TRUNCATE TABLE cart"
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()
    bot.reply_to(message, "Payment confirmed. Thank you for your purchase!")
# Start the bot
bot.polling()




