import requests
from datetime import datetime
import smtplib
import time

# Constants
MY_LAT = 40.287811 # Your latitude
MY_LONG = -4.013770 # Your longitude
FROM_EMAIL = "veregorn88@gmail.com"
FROM_PASSWORD = "adcf mbkq gced babz"
TO_EMAIL = "rjbarco@gmail.com"



# This is a function that returns True if my position is within +5 or -5 degrees of the ISS position.
def is_iss_close():
    # Get the ISS position
    # API call to get the current ISS position
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # Extract coordinates
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Check if the ISS is close to my current position
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    return False



# This is a function that returns True if it is currently dark
def is_dark():
    # Parameters for the API call
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    # API call to get the sunrise and sunset times
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # Extract sunrise and sunset hours
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Get the current time
    time_now = datetime.now()
    # Get the current hour
    hour_now = time_now.hour

    # Check if it is currently dark
    if hour_now >= sunset or hour_now <= sunrise:
        return True
    return False



# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# run the code every 60 seconds.
while True:
    if is_iss_close() and is_dark():
        # Send an email
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=FROM_EMAIL, password=FROM_PASSWORD)
            connection.sendmail(
                from_addr=FROM_EMAIL,
                to_addrs=TO_EMAIL,
                msg="Subject:Look Up\n\nThe ISS is above you in the sky."
            )
    time.sleep(60)
    