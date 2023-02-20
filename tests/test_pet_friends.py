import os
from api import PetFriends
from settings import valid_email, valid_password

TestPetFriend = PetFriends()


# Получение ключа авторизации
def test_get_api_key(email=valid_email, passwd=valid_password):
    """Получение ключа авторизации в проекте. Должны получить статус 200 и api-key в результате"""

    # Отправляем запрос
    status, result = TestPetFriend.get_api_key(email, passwd)

    # Сравниваем ответ с ожиданием
    assert status == 200
    assert 'key' in result


# Добавление питомца без фото
def test_add_new_pet_simple(name='Барсик', animal_type='кот', age='1'):
    """Проверка добавления питомца без фото в базу (метод POST).
    Должны получить статус 200 и результат в формате json"""

    # Аутентификация
    status, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Добавляем питомца
    status, result = TestPetFriend.add_new_pet_simple(auth, name, animal_type, age)

    # Сравниваем ответ с ожиданием
    assert status == 200
    assert result['name'] == name


# Изменение данных о питомце
def test_update_pet(name='Симка', animal_type='кошка', age='1', fltr='my_pets'):
    """Проверка изменения данных о питомце без фото (метод PUT).
    Должны получить статус 200 и результат в формате json"""

    # Аутентификация
    _, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Получаем идентификатор питомца
    _, _, pet_id = TestPetFriend.get_pet_list_and_last_id(auth, fltr)

    if pet_id != 0:
        # Изменяем питомца
        status, result = TestPetFriend.update_pet_by_id(auth, pet_id, name, animal_type, age)

        # Сравниваем ответ с ожиданием
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Нет моих питомцев")


# Добавление фото питомца
def test_add_photo_of_pet(pet_photo='cat1.jpg',  fltr='my_pets'):
    """Проверка добавления фото питомца в базу (метод POST).
    Должны получить статус 200 и результат в формате json"""

    # Аутентификация
    status, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Получаем идентификатор питомца
    _, _, pet_id = TestPetFriend.get_pet_list_and_last_id(auth, fltr)

    # Полный путь к изображению питомца
    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    if pet_id != 0:
        # Изменяем питомца
        status, result = TestPetFriend.add_pets_photo(auth, pet_id, pet_photo)

        # Сравниваем ответ с ожиданием
        assert status == 200
        assert result['pet_photo'].startswith('data:image/jpeg')
    else:
        raise Exception("Нет моих питомцев")


# Удаление питомца
def test_delete_pet(fltr='my_pets'):
    """Проверка удаления последнего питомца (метод DELETE).
    Должны получить статус 200 и результат в формате json"""

    # Аутентификация
    _, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Получаем идентификатор питомца
    _, _, pet_id = TestPetFriend.get_pet_list_and_last_id(auth, fltr)

    if pet_id != 0:
        # Удаляем питомца
        status, result = TestPetFriend.delete_pet_by_id(auth, pet_id)

        # Сравниваем ответ с ожиданием
        assert status == 200

        # Получаем идентификатор питомца
        _, _, pet_new_id = TestPetFriend.get_pet_list_and_last_id(auth, fltr)
        # Ожидаем, что id питомца 0 или другой
        assert pet_new_id == 0 or pet_id != pet_new_id
    else:
        raise Exception('Нет моих питомцев')


# Добавление питомца с фото
def test_add_new_pet(name='Барсик', animal_type='кот', age='1', pet_photo='cat1.jpg'):
    """Проверка добавления питомца с фото в базу (метод POST).
    Должны получить статус 200 и результат в формате json"""

    # Аутентификация
    status, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Полный путь к изображению питомца
    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    # Добавляем питомца
    status, result = TestPetFriend.add_new_pet(auth, name, animal_type, age, pet_photo)

    # Сравниваем ответ с ожиданием
    assert status == 200
    assert result['name'] == name


# Вывод списка "моих" питомцев
def test_get_pets_list(name='Барсик', animal_type='кот', age='1', fltr='my_pets'):
    """Проверка получения списка питомцев (метод GET).
    Должны получить статус 200 и результат в формате json"""

    # Аутентификация
    status, res_auth = TestPetFriend.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    # Получаем список питомцев
    _, pets_list, _ = TestPetFriend.get_pet_list_and_last_id(auth, fltr)
    len_pets_list = len(pets_list['pets'])

    # Добавляем питомца
    _, result = TestPetFriend.add_new_pet_simple(auth, f'{name} New', animal_type, age)

    # Получаем новый список питомцев
    status, pets_list_new, _ = TestPetFriend.get_pet_list_and_last_id(auth, fltr)

    # Сравниваем ответ с ожиданием
    assert status == 200
    assert len(pets_list_new['pets']) == len_pets_list + 1

