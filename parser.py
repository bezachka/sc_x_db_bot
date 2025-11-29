from requests import get, post
from dotenv import load_dotenv, find_dotenv
import os
from pathlib import Path
from datetime import datetime
import requests
from server import get_code


BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / "keys.env") 

AUTH_URL = os.getenv("AUTH_URL")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = os.getenv("CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        "scope" : ""
    }



def get_auth_token(code):
    url = "https://exbo.net/oauth/token"

    params = {
    "client_id" : CLIENT_ID,
    "client_secret" : CLIENT_SECRET,
    "code" : code,
    "grant_type" : "authorization_code",
    "redirect_uri" : "https://sc-x-db-bot.onrender.com/callback"
}

    response = requests.post(url = url, params=params)
    return "Bearer " + response.json()["access_token"]


response = post(url="https://exbo.net/oauth/token", data=data)


# TOKEN = "Bearer " + response.json()["access_token"]

# url = f"https://eapi.stalcraft.net/ru/friends/beza"
# headers = {"Authorization" : TOKEN}
# response1 = get(url=url, headers=headers)
# print(response1.json())


# url = "https://api.github.com/repos/EXBO-Studio/stalcraft-database/contents/ru/items/weapon/assault_rifle/p63d2.json"

# response_new = get(url)
# files = response_new.json()
# content = base64.b64decode(files['content']).decode('utf-8')
# json_data = json.loads(content)
# print(json.dumps(json_data, indent=2, ensure_ascii=False))

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

def get_auction_active_lots(item_id, region):
    headers = {"Authorization" : TOKEN}
    url = f"https://eapi.stalcraft.net/{region}/auction/{item_id}/lots"
    response1 = get(url, headers=headers)
    return response1.json()


    