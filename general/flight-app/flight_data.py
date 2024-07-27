import datetime as dt
from data_manager import DataManager
from dotenv import load_dotenv
import requests
import os

# six_month = dt.datetime.now() + dt.timedelta(days = 180)
# print(six_month)

class FlightData:
    def __init__(self):
        self.data_manager = DataManager()
        self.flight_offer_endpoint = os.getenv("AMADEUS_FLIGHT_OFFER_ENDPOINT")
        self.travelver_type = "ADULT"
        self.body = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }
        self.token = self.get_new_token()

    def find_cheapest_flight(self):
        sheet_data = self.data_manager.get_data()
        for city in sheet_data["prices"]:
            destination_code = city["iataCode"]
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {
                "currencyCode": "GBP",
                "originDestinations": [
                    {
                        "id": "1",
                        "originLocationCode": "LON",
                        "destinationLocationCode": destination_code,
                        "departureDateTimeRange": {
                            "date": "2024-11-01",
                            "time": "10:00:00",
                        },
                    }
                ],
            }
            response = requests.post(
                url=self.flight_offer_endpoint, params=payload, headers=headers
            )
            # Code to be finished here
