import os
from api import PetFriends
from settings import valid_email, valid_password

TestPetFriend = PetFriends()


# Негативные тесты - Задание 24.7.2
# 1. Получение ключа авторизации без пароля
def test_get_api_key_without_password(email=valid_email, passwd=''):
    """Попытка получения ключа авторизации без пароля. Должны получить статус 403 - Forbidden"""

    # Отправляем запрос
    status, result = TestPetFriend.get_api_key(email, passwd)

    # Сравниваем ответ с ожиданием
    assert status == 403
    assert 'key' not in result


# 2. Получение ключа авторизации без емейла
def test_get_api_key_without_email(email='', passwd=valid_password):
    """Попытка получения ключа авторизации без пароля. Должны получить статус 403 - Forbidden"""

    # Отправляем запрос
    status, result = TestPetFriend.get_api_key(email, passwd)

    # Сравниваем ответ с ожиданием (403 Forbidden)
    assert status == 403
    assert 'key' not in result


# 3. Добавление питомца без авторизации
def test_add_new_pet_without_auth(name='Барсик', animal_type='кот', age='1'):
    """Проверка добавления питомца без авторизации. Должны получить статус 403 - Forbidden"""

    # # Аутентификация
    auth = ''

    # Добавляем питомца
    status, result = TestPetFriend.add_new_pet_simple(auth, name, animal_type, age)

    # Сравниваем ответ с ожиданием
    assert status == 403


# 4. Изменение данных о питомце - пустое имя
def test_update_pet_without_name(name='', animal_type='кошка', age='1', fltr='my_pets'):
    """Проверка изменения питомца - пустое имя. Должны получить статус 400 ошибка в данных, т.к. имя - required"""

    # Аутентификация
    _, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Получаем идентификатор питомца
    _, _, pet_id = TestPetFriend.get_pet_list_and_last_id(auth, fltr)

    if pet_id != 0:
        # Изменяем питомца
        status, result = TestPetFriend.update_pet_by_id(auth, pet_id, name, animal_type, age)

        # Сравниваем ответ с ожиданием
        assert status == 400
    else:
        raise Exception("Нет моих питомцев")


# 5. Добавление питомца без имени
def test_add_new_pet_without_name(name='', animal_type='кот', age='1'):
    """Проверка добавления питомца без имени. Должны получить статус 400 ошибка в данных, т.к. имя - required"""

    # # Аутентификация
    status, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Добавляем питомца
    status, result = TestPetFriend.add_new_pet_simple(auth, name, animal_type, age)

    # Сравниваем ответ с ожиданием
    assert status == 400


# 6. Добавление питомца без типа
def test_add_new_pet_without_type(name='Барсик Неизвестный', animal_type='', age='1'):
    """Проверка добавления питомца без типа. Должны получить статус 400 ошибка в данных, т.к. тип - required"""

    # # Аутентификация
    status, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Добавляем питомца
    status, result = TestPetFriend.add_new_pet_simple(auth, name, animal_type, age)

    # Сравниваем ответ с ожиданием
    assert status == 400


# 7. Добавление питомца с отрицательным возрастом
def test_add_new_pet_without_negative_age(name='Барсик < 0', animal_type='Кот', age='-1'):
    """Проверка добавления питомца с отрицательным возрастом. Должны получить статус 400 ошибка в данных, т.к. возраст не может быть отрицательным"""

    # # Аутентификация
    status, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Добавляем питомца
    status, result = TestPetFriend.add_new_pet_simple(auth, name, animal_type, age)

    # Сравниваем ответ с ожиданием
    assert status == 400


# 8. Добавление питомца с возрастом - текстом
def test_add_new_pet_without_age_not_number(name='Барсик', animal_type='Кот', age='один год'):
    """Проверка добавления питомца с возрастом - текстом. Должны получить статус 400 ошибка в данных"""

    # # Аутентификация
    status, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Добавляем питомца
    status, result = TestPetFriend.add_new_pet_simple(auth, name, animal_type, age)

    # Сравниваем ответ с ожиданием
    assert status == 400


# 9. Добавление питомца с возрастом > int64
def test_add_new_pet_with_too_much_age(name='Барсик Оооочень старый', animal_type='Кот', age=(2**64 + 1)):
    """Проверка добавления питомца с возрастом - огромным числом. Должны получить статус 400 ошибка в данных"""

    # # Аутентификация
    status, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Добавляем питомца
    status, result = TestPetFriend.add_new_pet_simple(auth, name, animal_type, age)

    # Сравниваем ответ с ожиданием
    assert status == 400


# 10. Добавление фото питомца - текстовый файл, а не jpg
def test_add_photo_of_pet_txt_file(pet_photo='cat.txt',  fltr='my_pets'):
    """Проверка добавления фото питомца - указан текстовый файл, а не jpg. Должны получить статус - 500 ошибка"""

    # Аутентификация
    _, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Получаем идентификатор питомца
    _, _, pet_id = TestPetFriend.get_pet_list_and_last_id(auth, fltr)

    # Полный путь к изображению питомца
    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    if pet_id != 0:

        # Добавляем фото
        status, result = TestPetFriend.add_pets_photo(auth, pet_id, pet_photo)

        # Сравниваем ответ с ожиданием
        assert status == 500
    else:
        raise Exception("Нет моих питомцев")
