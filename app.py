from flows.start import*
from flows.FindRide import*
from flows.OfferRide import*
import time

while True:
    try:
        bot.polling(none_stop=True)  # Keeps running unless an error occurs
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        time.sleep(5)  # Wait 5 seconds before restarting
