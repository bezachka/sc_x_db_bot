from requests import get, post
from dotenv import load_dotenv, find_dotenv
import os
from pathlib import Path
from datetime import datetime
import json
import webbrowser

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / "keys.env") 

AUTH_URL = os.getenv("AUTH_URL")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")

data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        "scope" : ""
    }

response = post(url=AUTH_URL, data=data)

TOKEN = "Bearer " + response.json()["access_token"]

def get_auction_history(region, item_id):
    dict = {}
    url = f"https://eapi.stalcraft.net/{region}/auction/{item_id}/history"
    headers = {"Authorization" : TOKEN}
    response = get(url=url, headers=headers)
    for i in response.json()["prices"]:
        data_str = i["time"]
        dt_object = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
        if dict.get(dt_object.strftime("%d.%m.%Y")) == None:
            dict[dt_object.strftime("%d.%m.%Y")] = [i["price"]]
        else:
            dict[dt_object.strftime("%d.%m.%Y")].append(i["price"])

    return dict

dict = get_auction_history(region="ru", item_id="dmjwn")
for i in dict:
    print(dict.get(i))
    