import sys
sys.path.append("..")

from cred.cred import bot
from telebot.types import ReplyKeyboardRemove
from db.dbconn import cursor,conn

@bot.message_handler(func=lambda message: message.text == "🚘 Offer a Ride")
def offer_ride(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "📍 Please share your <b>Pickup Location</b> to get started:", 
                     parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_pickup_location)

def get_pickup_location(message):
    chat_id = message.chat.id
    if not message.location:
        bot.send_message(chat_id, "⚠️ Please share your <b>pick up location</b>.",parse_mode="HTML")
        return offer_ride(message)
    
    pickup_lat, pickup_lon = message.location.latitude, message.location.longitude
    bot.send_message(chat_id, "Now share your <b>Drop-off Location:</b>",parse_mode="HTML")
    bot.register_next_step_handler(message, get_drop_location, pickup_lat, pickup_lon)

def get_drop_location(message, pickup_lat, pickup_lon):
    chat_id = message.chat.id
    if not message.location:
        bot.send_message(chat_id, "⚠️ Please share your <b>drop location</b>.",parse_mode="HTML")
        return get_pickup_location(message)

    drop_lat, drop_lon = message.location.latitude, message.location.longitude
    bot.send_message(chat_id, "Enter <b>Time of Travel (e.g., 9:00 AM):</b>",parse_mode="HTML")
    bot.register_next_step_handler(message, get_time, pickup_lat, pickup_lon, drop_lat, drop_lon)

def get_time(message, pickup_lat, pickup_lon, drop_lat, drop_lon):
    chat_id = message.chat.id
    time = message.text
    bot.send_message(chat_id, "Enter <b>Number of Seats Available:</b>",parse_mode="HTML")
    bot.register_next_step_handler(message, get_seats, pickup_lat, pickup_lon, drop_lat, drop_lon, time)

def get_seats(message, pickup_lat, pickup_lon, drop_lat, drop_lon, time):
    chat_id = message.chat.id
    seats = int(message.text)
    bot.send_message(chat_id, "Enter <b>Fare per Person (₹):</b>",parse_mode="HTML")
    bot.register_next_step_handler(message, save_ride, pickup_lat, pickup_lon, drop_lat, drop_lon, time, seats)

def save_ride(message, pickup_lat, pickup_lon, drop_lat, drop_lon, time, seats):
    chat_id = message.chat.id
    fare = int(message.text)
    username = message.from_user.username or "Unknown"

    cursor.execute("""
        INSERT INTO rides (user_id, username, pickup_lat, pickup_lon, drop_lat, drop_lon, time, seats, fare)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (chat_id, username, pickup_lat, pickup_lon, drop_lat, drop_lon, time, seats, fare))
    conn.commit()

    bot.send_message(chat_id, f"✅ Ride Listed!\n⏰ Time: {time} \n🪑 Seats: {seats} \n💰 Fare: ₹{fare}",parse_mode="HTML")

