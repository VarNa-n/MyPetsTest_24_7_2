import requests
import json
import os


class PetFriends:
    """API-библиотека к приложению PetFriends"""

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'

    # get_api_key: GET /api/key - get API key
    def get_api_key(self, email: str, passwd: str) -> json:
        """Метод get_api_key аутентифицирует пользователя и возвращает статус выполнения запроса
        и результат в формате json с уникальным ключом пользователя"""

        headers = {
            'email': email,
            'password': passwd
        }

        res = requests.get(f'{self.base_url}/api/key', headers=headers)
        status = res.status_code

        # Ответ должен быть в формате json. Если нет, то возвращаем текст
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text

        return status, result

    # get_pet_list_and_last_id: Задание 24.7.2 - GET /api/pets - /api/pets плюс возвращает последний pet_id
    def get_pet_list_and_last_id(self, auth_key: str, fltr=''):
        """Метод возвращает статус выполнения запроса, список питомцев в формате json
        и идентификатор последнего введенного питомца для последующего теста PUT и DELETE"""

        headers = {'auth_key': auth_key}

        res = requests.get(f'{self.base_url}/api/pets?filter={fltr}', headers=headers)
        status = res.status_code
        # Ответ должен быть в формате json. Если нет, то возвращаем текст
        res_id = 0
        try:
            result = res.json()
            # Возвращаем id только для своего питомца
            if len(result['pets']) > 0:
                res_id = result['pets'][0]['id'] if fltr == 'my_pets' else 0
        except json.JSONDecodeError:
            result = res.text

        return status, result, res_id

    # add_new_pet: POST /api/pets - add information about new pet
    def add_new_pet(self, auth_key: str, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод add_new_pet реализует api-метод POST для добавления питомца в базу.
        Возвращает статус выполнения запроса и результат в формате json"""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(f'{self.base_url}/api/pets', headers=headers, data=data, files=file)
        status = res.status_code
        # Ответ должен быть в формате json. Если нет, то возвращаем текст
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text

        return status, result

    # update_pet_by_id: Задание 24.4.1 - PUT /api/pets/{pet_id} - update information about pet
    def update_pet_by_id(self, auth_key: str, pet_id: str,  name: str, animal_type: str, age: str) -> json:
        """Метод update_pet_by_id реализует api-метод PUT для изменения информации о питомце в базе.
        Возвращает статус выполнения запроса и результат в формате json"""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key}

        res = requests.put(f'{self.base_url}/api/pets/{pet_id}', headers=headers, data=data)
        status = res.status_code
        # Ответ должен быть в формате json. Если нет, то возвращаем текст
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text

        return status, result

    # delete_pet_by_id: Задание 24.4.1 - DELETE /api/pets/{pet_id} - delete pet from database
    def delete_pet_by_id(self, auth_key: str, pet_id: str) -> json:
        """Метод delete_pet_by_id реализует api-метод PUT для изменения информации о питомце в базе.
        Возвращает статус выполнения запроса и результат в формате json"""

        headers = {'auth_key': auth_key}

        res = requests.delete(f'{self.base_url}/api/pets/{pet_id}', headers=headers)
        status = res.status_code
        # Ответ должен быть в формате json. Если нет, то возвращаем текст
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text

        return status, result

    # add_new_pet_simple: Задание 24.7.2 - POST /api/create_pet_simple - add information about new pet without photo
    def add_new_pet_simple(self, auth_key: str, name: str, animal_type: str, age: str) -> json:
        """Метод add_new_pet_simple реализует api-метод POST для добавления питомца в базу без фото.
        Возвращает статус выполнения запроса и результат в формате json"""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        headers = {'auth_key': auth_key}

        res = requests.post(f'{self.base_url}/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code

        # Ответ должен быть в формате json. Если нет, то возвращаем текст
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text

        return status, result

    # add_pets_photo: Задание 24.7.2 - POST /api/pets/set_photo/{pet_id} - add photo of a pet
    def add_pets_photo(self, auth_key: str, pet_id: str, pet_photo: str) -> json:
        """Метод add_pets_photo реализует api-метод POST для добавления фото указанного питомца в базу.
        Возвращает статус выполнения запроса и результат в формате json"""

        headers = {'auth_key': auth_key}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(f'{self.base_url}/api/pets/set_photo/{pet_id}', headers=headers, files=file)
        status = res.status_code
        # Ответ должен быть в формате json. Если нет, то возвращаем текст
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text

        return status, result


## Аутентификация
#pp = PetFriends()
#status, result = pp.get_api_key('nata@varsh.ru', '1q2w3')
#print("*******", result['key'])
#auth = result['key']
## Получаем идентификатор питомца
#_, _, pet_id = pp.get_pet_list_and_last_id(auth, 'my_pets')
#print(pet_id)
