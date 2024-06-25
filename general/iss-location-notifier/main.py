import time
import requests
from datetime import datetime
import smtplib

MY_LAT = 36.778259  # Your latitude
MY_LONG = -119.417931  # Your longitude
TIMEZONE = "America/Los_Angeles"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


def above_my_location():
    if MY_LONG - 5 <= iss_longitude <= MY_LONG + 5 and MY_LAT - 5 <= iss_latitude <= MY_LAT + 5:
        return True


def is_dark_now():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "tzid": TIMEZONE,
        "formatted": 0
    }

    new_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    new_response.raise_for_status()
    new_data = new_response.json()

    sunrise = int(new_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(new_data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


my_email = "test@gmail.com"
password = "**********"
email_sent = False

while True:
    if is_dark_now() and above_my_location():
        if not email_sent:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()  # Make the connection secure
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs="test123@gmail.com",
                    msg="Subject:Check out the ISS\n\nThe ISS is above you in the sky!"
                )
            email_sent = True
    else:
        email_sent = False
    time.sleep(60)
