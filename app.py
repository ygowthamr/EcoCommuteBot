from flows.start import*
from flows.FindRide import*
from flows.OfferRide import*
import time

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)  # Wait before retrying
