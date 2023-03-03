import os
import pytest
from api_26 import PetFriends
from settings import valid_email, valid_password
from datetime import datetime


TestPetFriend = PetFriends()


# Получение ключа авторизации (фикстура)
@pytest.fixture()
def get_key(email=valid_email, passwd=valid_password):
    """Фикстура для получения авторизации в проекте. Должны получить статус 200 и api-key в результате"""

    # Отправляем запрос
    status, result = TestPetFriend.get_api_key(email, passwd)

    # Сравниваем ответ с ожиданием
    assert status == 200
    assert 'key' in result
    return result['key']


@pytest.mark.add
# Добавление питомца без фото
def test_add_new_pet_simple(get_key, name='Барсик', animal_type='кот', age='1'):
    """Проверка добавления питомца без фото в базу (метод POST).
    Должны получить статус 200 и результат в формате json"""

    # Добавляем питомца
    status, result = TestPetFriend.add_new_pet_simple(get_key, name, animal_type, age)

    # Сравниваем ответ с ожиданием
    assert status == 200
    assert result['name'] == name


@pytest.mark.xfail(raises=Exception)
# Изменение данных о питомце
def test_update_pet(get_key, name='Симка', animal_type='кошка', age='1', fltr='my_pets'):
    """Проверка изменения данных о питомце без фото (метод PUT).
    Должны получить статус 200 и результат в формате json"""

    # Получаем идентификатор питомца
    _, _, pet_id = TestPetFriend.get_pet_list_and_last_id(get_key, fltr)

    if pet_id != 0:
        # Изменяем питомца
        status, result = TestPetFriend.update_pet_by_id(get_key, pet_id, name, animal_type, age)

        # Сравниваем ответ с ожиданием
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Нет моих питомцев")


@pytest.mark.photo
# Добавление фото питомца
def test_add_photo_of_pet(get_key, pet_photo='cat1.jpg',  fltr='my_pets'):
    """Проверка добавления фото питомца в базу (метод POST).
    Должны получить статус 200 и результат в формате json"""

    # Получаем идентификатор питомца
    _, _, pet_id = TestPetFriend.get_pet_list_and_last_id(get_key, fltr)

    # Полный путь к изображению питомца
    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    if pet_id != 0:
        # Изменяем питомца
        status, result = TestPetFriend.add_pets_photo(get_key, pet_id, pet_photo)

        # Сравниваем ответ с ожиданием
        assert status == 200
        assert result['pet_photo'].startswith('data:image/jpeg')
    else:
        raise Exception("Нет моих питомцев")


@pytest.mark.skip(reason="Удаление пропускаем")
# Удаление питомца
def test_delete_pet(get_key, fltr='my_pets'):
    """Проверка удаления последнего питомца (метод DELETE).
    Должны получить статус 200 и результат в формате json"""

    # Получаем идентификатор питомца
    _, _, pet_id = TestPetFriend.get_pet_list_and_last_id(get_key, fltr)

    if pet_id != 0:
        # Удаляем питомца
        status, result = TestPetFriend.delete_pet_by_id(get_key, pet_id)

        # Сравниваем ответ с ожиданием
        assert status == 200

        # Получаем идентификатор питомца
        _, _, pet_new_id = TestPetFriend.get_pet_list_and_last_id(get_key, fltr)
        # Ожидаем, что id питомца 0 или другой
        assert pet_new_id == 0 or pet_id != pet_new_id
    else:
        raise Exception('Нет моих питомцев')


@pytest.mark.add
@pytest.mark.photo
# Добавление питомца с фото
def test_add_new_pet(get_key, name='Барсик', animal_type='кот', age='1', pet_photo='cat1.jpg'):
    """Проверка добавления питомца с фото в базу (метод POST).
    Должны получить статус 200 и результат в формате json"""

    # Полный путь к изображению питомца
    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    # Добавляем питомца
    status, result = TestPetFriend.add_new_pet(get_key, name, animal_type, age, pet_photo)

    # Сравниваем ответ с ожиданием
    assert status == 200
    assert result['name'] == name


# Вывод списка "моих" питомцев
def test_get_pets_list(get_key, name='Барсик', animal_type='кот', age='1', fltr='my_pets'):
    """Проверка получения списка питомцев (метод GET).
    Должны получить статус 200 и результат в формате json"""

    # Получаем список питомцев
    _, pets_list, _ = TestPetFriend.get_pet_list_and_last_id(get_key, fltr)
    len_pets_list = len(pets_list['pets'])

    # Добавляем питомца
    _, result = TestPetFriend.add_new_pet_simple(get_key, f'{name} New', animal_type, age)

    # Получаем новый список питомцев
    status, pets_list_new, _ = TestPetFriend.get_pet_list_and_last_id(get_key, fltr)

    # Сравниваем ответ с ожиданием
    assert status == 200
    assert len(pets_list_new['pets']) == len_pets_list + 1


@pytest.fixture(autouse=True)
def time_delta():
    start_time = datetime.now()
    print(f"\nStart test at {start_time}")
    yield
    end_time = datetime.now()
    print(f"\nТест шел: {end_time - start_time}")
