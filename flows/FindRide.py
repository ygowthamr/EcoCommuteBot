import sys
sys.path.append("..")

from cred.cred import bot
from telebot.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from db.dbconn import cursor
from haversine import haversine

@bot.message_handler(func=lambda message: message.text == "👤 Find a Ride")
def find_ride(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Share your <b>Pickup Location:</b>",parse_mode="HTML",reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_find_pickup)

def get_find_pickup(message):
    chat_id = message.chat.id
    if not message.location:
        bot.send_message(chat_id, "⚠️ Please share your <b>pickup location</b>.",parse_mode="HTML")
        return find_ride(message)

    pickup_lat, pickup_lon = message.location.latitude, message.location.longitude
    bot.send_message(chat_id, "Please share your <b>Drop Location</b>:",parse_mode="HTML")
    bot.register_next_step_handler(message, get_find_drop, pickup_lat, pickup_lon)

def get_find_drop(message, pickup_lat, pickup_lon):
    chat_id = message.chat.id
    if not message.location:
        bot.send_message(chat_id, "⚠️ Please share your <b>live location</b>.",parse_mode="HTML")
        return get_find_pickup(message)

    drop_lat, drop_lon = message.location.latitude, message.location.longitude
    bot.send_message(chat_id, "Enter <b>Number of Seats Required:</b>",parse_mode="HTML")
    bot.register_next_step_handler(message, search_rides, pickup_lat, pickup_lon, drop_lat, drop_lon)

def search_rides(message, pickup_lat, pickup_lon, drop_lat, drop_lon):
    chat_id = message.chat.id
    required_seats = int(message.text)  # Convert text input to integer

    cursor.execute("SELECT * FROM rides")
    rides = cursor.fetchall()

    best_match = None
    min_distance = float("inf")

    for ride in rides:
        try:
            # Extract values correctly from the tuple
            ride_pickup = (float(ride[3]), float(ride[4]))  # pickup_lat, pickup_lon
            ride_drop = (float(ride[5]), float(ride[6]))    # drop_lat, drop_lon
            ride_seats = int(ride[8])  # Seats available

            # Compute distances
            distance_pickup = haversine((pickup_lat, pickup_lon), ride_pickup)
            distance_drop = haversine((drop_lat, drop_lon), ride_drop)

            # Allow nearby rides (within 500m = 0.5km)
            if distance_pickup <= 0.5 and distance_drop <= 0.5 and required_seats <= ride_seats:
                total_distance = distance_pickup + distance_drop
                if total_distance < min_distance:
                    min_distance = total_distance
                    best_match = ride

        except Exception as e:
            print(f"Skipping invalid ride data: {ride} - Error: {e}")

    if best_match:
        ride_info = (
            f"🚘 Driver: @{best_match[2]}\n"
            f"📍 From: {best_match[3]}, {best_match[4]}\n"
            f"📍 To: {best_match[5]}, {best_match[6]}\n"
            f"⏰ Time: {best_match[7]}\n"
            f"🪑 Seats: {best_match[8]}\n"
            f"💰 Fare: ₹{best_match[9]}\n"
            f"📍 Distance: {round(min_distance, 2)} km"
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📞 Contact Driver", url=f"https://t.me/{best_match[2]}"))
        bot.send_location(chat_id, latitude=pickup_lat, longitude=pickup_lon)
        bot.send_message(chat_id, ride_info, reply_markup=markup,)
    else:
        bot.send_message(chat_id, "❌ No rides found nearby with your criteria. Try again later!")