import requests
import time
from datetime import datetime
from tqdm import tqdm
from main import get_file_json


class Vkontakte:

    def __init__(self, vk_token, user_id, quantity, version="5.131"):
        self.VK_token = vk_token
        self.version = version
        self.count = quantity
        self.user_id = user_id

    def get_id(self):
        URL = "https://api.vk.com/method/users.get"
        params = {
            "access_token": self.VK_token,
            "user_ids": self.user_id,
            "v": self.version
        }
        res = requests.get(url=URL, params=params).json()
        for el in res.get("response"):
            return el["id"]

    def get_photos_from_vk(self, offset=0):
        URL = "https://api.vk.com/method/photos.get"
        params = {
            "access_token": self.VK_token,
            "owner_id": self.get_id(),
            "album_id": "profile",
            "extended": 1,
            "offset": offset,
            "count": self.count,
            "photo_sizes": True,
            "v": self.version
        }
        response = requests.get(url=URL, params=params).json()
        photos = []
        info_of_photos = []
        count = 0
        for file in tqdm(response["response"]["items"]):
            photos.append(
                {
                    "likes": str(file["likes"]["count"]),
                    "url_photo": file["sizes"][-1]["url"],
                    "upload_date": datetime.fromtimestamp(int(file["date"])).strftime("%Y.%m.%d")
                }
            )
            info_of_photos.append(
                {
                    "file_name": str(file["likes"]["count"]) + ".jpg",
                    "size": file["sizes"][-1]["type"]
                }
            )
            count += 1
            get_file_json(info_of_photos)
            time.sleep(1)
        return photos