from dotenv import load_dotenv
from data_manager import DataManager
import requests
import os

load_dotenv()


class FlightSearch:
    def __init__(self):
        self.data_manager = DataManager()
        self.sheety_endpoint_url = os.getenv("SHEETY_ENDPOINT_URL")
        self.city_search_endpoint = os.getenv("AMADEUS_CITY_SEARCH_ENDPOINT")
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.token_endpoint = os.getenv("AMADEUS_TOKEN_ENDPOINT")
        self.header = {"Content-Type": "application/x-www-form-urlencoded"}
        self.body = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }
        self.token = self.get_new_token()

    def add_city_code(self):
        sheet_data = self.data_manager.get_data()
        for city in sheet_data["prices"]:
            city_name = city["city"]
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {
                "keyword": city_name,
                "max": 1,
            }
            r = requests.get(
                url=self.city_search_endpoint, params=payload, headers=headers
            )
            r.raise_for_status()
            iatacode = r.json()["data"][0]["iataCode"]
            data = {"price": {"iataCode": iatacode}}
            self.data_manager.put_data(
                endpoint_url=f"{self.sheety_endpoint_url}/{city['id']}", parameters=data
            )

    def get_new_token(self):
        response = requests.post(
            url=self.token_endpoint, headers=self.header, data=self.body
        )
        return response.json()["access_token"]
