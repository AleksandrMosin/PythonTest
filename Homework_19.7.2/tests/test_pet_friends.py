from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем что запрос всех питомцев возвращает не пустой список"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Freddy', animal_type='ram',
                                     age='4', pet_photo='images/ram.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список питомцев пустой, то добавляем нового и опять запрашиваем список питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Melman', 'giraffe', '35', 'images/giraffe.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Sharik', animal_type='pug', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии питомцев
        raise Exception('There are no pets')


def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """Проверяем что запрос api ключа с неверным email и верным password возвращает код 403"""

    status, result = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert 'This user is not found in the database' in result


def test_get_api_key_for_valid_email_and_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем что запрос api ключа с верным email и неверным password возвращает код 403"""

    status, result = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert 'This user is not found in the database' in result

def test_get_api_key_for_invalid_email_and_invalid_password(email=invalid_email, password=invalid_password):
    """Проверяем что запрос api ключа с неверным email и верным password возвращает код 403"""

    status, result = pf.get_api_key(email, password)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert 'This user is not found in the database' in result


def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяем что запрос всех питомцев с неверным api ключом возвращает код 403"""

    # Задаем неверный ключ api и сохраняем в переменную auth_key
    auth_key = {'key': 'asd123'}

    # Запрашиваем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


def test_create_pet_simple_with_valid_data(name='Morgan', animal_type='bull', age='3'):
    """Проверяем что можно упрощенно добавить питомца с корректными данными"""

    # Создаем питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_create_pet_simple_with_invalid_data(name='Willy', animal_type=int(2), age='4'):
    """Проверяем что запрос на упрощенное добавление питомца с неверным api ключом возвращает код 403"""

    # Создаем питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # Тут баг! - в качестве типа животного принимает числа


def test_create_pet_simple_with_invalid_data1(name=int(56), animal_type='cat', age='6'):
    """Проверяем что запрос на упрощенное добавление питомца с неверным api ключом возвращает код 403"""

    # Создаем питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # Тут баг! - в качестве имени животного принимает числа


def test_create_pet_simple_with_invalid_data2(name='Willy', animal_type='cat', age=int(-10)):
    """Проверяем что запрос на упрощенное добавление питомца с неверным api ключом возвращает код 403"""

    # Создаем питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # Тут баг! - в качестве возраста питомца принимает отрицательные числа


def test_add_new_pet_with_invalid_data(name='Chilly', animal_type='mouse',
                                       age='4', pet_photo='images/mouse.txt'):
    """Проверяем что можно добавить питомца с некорректными данными"""

    # Создаем питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # Тут баг! - в качестве фото принимает txt файл


def test_set_photo():
    """Проверяем возможность установки фото питомца"""

    # Запрашиваем список своих питомцев, получаем и записываем путьзображения
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/ram.jpg')
    if len(my_pets['pets']) > 0:

        status, result = pf.set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
    else:
        raise Exception("There are no pets")


