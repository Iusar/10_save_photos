import requests, json
from tqdm import tqdm
from pprint import pprint
from datetime import datetime

# Исходные данные
vk_id = "552934290"
yd_token =


class Downloader:
    def __init__(self, yd_token: str, vk_user_id: str):

        # Инициализация параметров yandex Disc
        self.yd_token = yd_token
        self.yd_headers = {'Authorization': 'OAuth ' + self.yd_token}

        # Инициализация параметров вконтакте
        self.json_from_vk = {}
        self.vk_user_id = vk_user_id

        # Вспомогательные
        self.list_for_check_equal_names = []
        self.report_list = []

    # Основной метод загрузки на яндекс диск
    def main_function(self):

        for photo in tqdm(self.get_photos_request_to_vk()):
            # pprint(photo)
            photo_name = self.create_filename(photo['likes']['count'], photo['date'])
            post_photo = requests.post(url='https://cloud-api.yandex.net/v1/disk/resources/upload',
                                       params=self.get_yd_params(photo['sizes'][-1]['url'], photo_name),
                                       headers=self.yd_headers)
            if post_photo.status_code == 202:
                self.report_list.append({"file_name": photo_name, "size": photo['sizes'][-1]['type']})
        # Сохранение отчета
        with open('data.json', 'w', encoding='utf-8') as report:
            json.dump(self.report_list, report, ensure_ascii=False, indent=4)
        pass

    # Получаем словарь из вконтакте для метода main_function
    def get_photos_request_to_vk(self):

        vk_params = {"owner_id": self.vk_user_id, 'album_id': 'profile', 'count': 5,
                     'access_token': self.get_vk_token_from_txt(), 'photo_sizes': '1', 'extended': 1, 'v': 5.131}
        photos_from_vk = requests.get('https://api.vk.com/method/photos.get', params=vk_params)
        if photos_from_vk.status_code == 200:
            self.json_from_vk = photos_from_vk.json()['response']['items']
            return self.json_from_vk
        else:
            print(f'error :( {photos_from_vk.status_code}')
            pass

    # Забираем токен ВК из текстового файла для get_photos_request_to_vk
    def get_vk_token_from_txt(self):
        with open('vk_token.txt', 'r', encoding='utf-8') as file:
            token_from_txt = file.read().strip()
        return token_from_txt

    # Создаем уникальное название файла для main_function
    def create_filename(self, likes, date):

        if str(likes) + '.jpg' in self.list_for_check_equal_names:
            file_name = str(likes) + str(date) + '.jpg'
            self.list_for_check_equal_names.append(file_name)
        else:
            file_name = str(likes) + '.jpg'
            self.list_for_check_equal_names.append(file_name)
        return file_name

    # функция динамичных параметров записи для main_function
    def get_yd_params(self, photo_url, photo_name):
        yd_params = {'path': '/VK_photos/' + photo_name, 'url': photo_url}
        return yd_params

    # Загружаем фото на Ядиск


if __name__ == '__main__':
    uploader = Downloader(yd_token, vk_id)
    result = uploader.main_function()
