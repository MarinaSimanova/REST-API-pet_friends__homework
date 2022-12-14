
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Charlie', animal_type='собака',
                                     age='2', pet_photo='images/spaniel.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Charlie", "собака", "2", "images/spaniel.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Toby', animal_type='dog', age=3):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Test 1
def test_get_api_key_for_valid_user_with_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа, с некорректным password пользователя, возвращает статус 403 и
     в результате не содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert status == 403
    assert 'key' not in result


# Test 2
def test_get_api_key_for_non_existent_user(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа, с некорректным email пользователя, возвращает статус 403 и
     в результате не содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert status == 403
    assert 'key' not in result


# Test 3
def test_add_new_pet_with_not_valid_age(name='Malt', animal_type='мальтийская болонка', age='1001',
                                        pet_photo='images/maltese lapdog.jpg'):
    """Проверяем что можно добавить питомца со значением  возраста больше 500"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# Test 4
def test_add_new_pet_without_a_name(name='', animal_type='собака', age='4',
                                    pet_photo='images/spaniel.jpg'):
    """Проверяем что можно добавить питомца без имени"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# Test 5
def test_add_new_pet_without_photo(name='Malt', animal_type='мальтийская болонка', age='4'):
    """Проверяем что можно добавить питомца без фото"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# Test 6
def test_add_pet_photo(pet_photo='images/spitz.jpg'):
    """Проверяем что можно добавить фото питомца """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'],  pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200
        assert result['pet_photo'] != ''
        assert 'pet_photo' in result

    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Test 7
def test_get_api_key_for_empty_password(email=valid_email, password=''):
    """ Проверяем что запрос api ключа, с пустым полем password, возвращает статус 403 и
     в результате не содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


# Test 8
def test_add_new_pet_with_long_name(name='jefryyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy',
                                    animal_type='мальтийская болонка', age='4', pet_photo='images/maltese lapdog.jpg'):
    """Проверяем что можно добавить питомца с длинным именем"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# Test 9
def test_add_new_pet_without_photo_with_wrong_data(name='1111@', animal_type='222!!!!!', age='4'):
    """Проверяем что можно добавить питомца без фото и с некорректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# Test 10
def test_add_new_pet_with_negative_age(name='Malt', animal_type='мальтийская болонка',
                                       age='-4', pet_photo='images/maltese lapdog.jpg'):
    """Проверяем что можно добавить питомца с отрицательным возрастом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
