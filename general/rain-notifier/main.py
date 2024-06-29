import requests
import smtplib
import os

endpoint_url = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("API_KEY")
my_email = os.environ.get("MY_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
email_password = os.environ.get("EMAIL_PASSWORD")


parameters = {
    # Set your city location
    # Visit https://www.latlong.net/
    "lat": 36.778259,
    "lon": -119.417931,
    "cnt": 4,
    "appid": api_key,
}


response = requests.get(url=endpoint_url, params=parameters)
response.raise_for_status()
weather_data = response.json()

will_train = False

for item in weather_data["list"]:
    if item["weather"][0]["id"] < 700:
        will_train = True

if will_train:
    # Set another SMTP if not gmail
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls() # Make the connection secure
        connection.login(user=my_email, password=email_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=receiver_email,
            msg="Subject:It's going to rain!\n\nBring an umbrella!!!"
        )
