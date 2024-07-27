import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class DataManager:
    def __init__(self):
        self.sheety_endpoint_url = os.getenv("SHEETY_ENDPOINT_URL")
        self.headers = {"Authorization": os.getenv("AUTH_ID")}

    def get_data(self):
        response = requests.get(url=self.sheety_endpoint_url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def put_data(self, endpoint_url, parameters):
        response = requests.put(url=endpoint_url, json=parameters, headers=self.headers)
        response.raise_for_status()
