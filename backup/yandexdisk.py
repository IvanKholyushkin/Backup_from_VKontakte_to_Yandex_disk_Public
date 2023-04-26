import requests
import time
from tqdm import tqdm


class YandexDisk:

    def __init__(self, token, photos):
        self.Yandex_token = token
        self.photo_dict = photos

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.Yandex_token}"
        }

    def folder_creation(self, folder):
        URL = r"https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": folder}
        requests.put(url=URL, headers=self.get_headers(), params=params)
        return folder

    def upload_to_yandex_disk(self, folder):
        URL = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        final_dict = []
        count = 0
        for element in tqdm(self.photo_dict):
            if element["likes"] not in final_dict:
                final_dict.append(element["likes"])
                path = f'{folder}/{element["likes"]}.jpg'
            else:
                final_dict.append(element["likes"])
                path = f'{folder}/{element["likes"]}.{element["upload_date"]}.jpg'
            params = {"path": path, "url": element["url_photo"]}
            time.sleep(1)
            response = requests.post(url=URL, headers=self.get_headers(), params=params)
            if response.status_code == 202:
                count += 1
            else:
                print(response.status_code)
        return f'Загруженно {count} фото в папку "{folder}"'