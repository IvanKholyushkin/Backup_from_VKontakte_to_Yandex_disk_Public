import json
import backup as b
import configparser


def get_file_json(info_photos):
    with open("file with info of photo.json", "w") as write_file:
        json.dump(info_photos, write_file, indent=4)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("secret.ini")
    VK_TOKEN = config["VK"]["VK_TOKEN"]
    TOKEN = config["Yandex"]["TOKEN"]
    user_id = input("Введите идентификатор пользователя или id вашей страницы: ")
    quantity = input(
        "Введите количество фото для загрузки на Яндекс диск (по умолчанию будет загруженно 5 фотографий) ")
    if quantity.isdigit():
        count_photos_to_download = quantity
    else:
        count_photos_to_download = 5
    vk = b.Vkontakte(VK_TOKEN, user_id, count_photos_to_download)
    ya = b.YandexDisk(TOKEN, photos=vk.get_photos_from_vk())
    folder_name = ya.folder_creation(input("Введите название папки "))
    print(ya.upload_to_yandex_disk(folder_name))