# MyPetsTest_24_7_2

Задание 24.7.2: 

1.Реализация всех API-методов веб приложения Pet Friends https://petfriends.skillfactory.ru/apidocs/

Реализовано в библиотеке api.py в корневой директории. Библиотеку писала сама, поэтому реализация методов местами отличается от приведенной в примере.
В корневой директории лежит файл settings.py - содержит информацию о валидном логине и пароле

2.Тесты API-методов веб приложения Pet Friends

В директории /tests располагается файл с тестами

В директории /tests/images лежат файлы для теста добавления питомца с картинкой и теста добавления картинки

Позитивные тесты (программа test_pet_friends.py, ожидаем статус 200):
- test_get_api_key - Получение ключа авторизации
- test_add_new_pet_simple - Добавление питомца без фото
- test_update_pet - зменение данных о питомце
- test_add_photo_of_pet - Добавление фото питомца
- test_delete_pet - Удаление питомца
- test_add_new_pet - Добавление питомца с фото
- test_get_pets_list - Вывод списка "моих" питомцев

Негативные тесты (программа test_pet_friends_24_7_2.py, ожидаем разные статусы)
- test_get_api_key_without_password - Получение ключа авторизации без пароля (status == 403)
- test_get_api_key_without_email - Получение ключа авторизации без емейла (status == 403)
- test_add_new_pet_without_auth - Добавление питомца без авторизации (status == 403)
- test_update_pet_without_name - Изменение данных о питомце: пустое имя (status == 400) - тест не проходит, система позволяет изменить имя на ''
- test_add_new_pet_without_name - Добавление питомца с пустым именем (status == 400) - тест не проходит, система позволяет ввести питомца с пустым именем
- test_add_new_pet_without_type - Добавление питомца с пустым типом (status == 400) - тест не проходит, система позволяет ввести питомца с пустым типом
- test_add_new_pet_without_negative_age - Добавление питомца с отрицательным возрастом (status == 400) - тест не проходит, система позволяет такой ввод
- test_add_new_pet_without_age_not_number - Добавление питомца с возрастом - не цифрой (status == 400) - тест не проходит, система позволяет такой ввод
- test_add_new_pet_with_too_much_age - Добавление питомца с возрастом > int64 (status == 400) - тест не проходит, система позволяет такой ввод
- test_add_photo_of_pet_txt_file - Добавление фото питомца - текстовый файл, а не jpg (status == 500)

Методы имеют подробное описание.
Тесты проверяют работу методов используя api библиотеку.

Для тестирования выполните команду pytest tests/
