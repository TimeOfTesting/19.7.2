from tests.api import PetFriends
from tests.settings import valid_email, valid_password
import os

pf = PetFriends()

def test_unsuccessful_get_api_key_for_unvalid_user(email='Liza@liza.ru', password='123'):
    """ Проверка что запрос возвращает статус 403, поскольку введены не существующий данные: email, password"""
    status, result = pf.get_api_key(email, password)

    assert status == 403

def test_successful_add_new_pet_without_photo(name="Маша", animal_type='Кошка', age=5):
    """Создание нового питомца без фотографии"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_info_pet_without_photo(auth_key, name, animal_type, age)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    print(pet_id)

    assert status == 200
    assert result['name'] == name

def test_successful_add_photo_pet(pet_id ='be77a778-9597-4594-a159-ebcea7fcf063',pet_photo='cat1.jpg'):
    """Добавление фотографии к созданному питомцу по его ID"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_photo(auth_key, pet_id, pet_photo)

    assert status == 200

def test_unsuccessful_add_new_pet(name="Дy,0,dhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghорывлпрлврпdhskgfhdjghоры",
                                  animal_type='Шоколадка', age=-1):
    """Создание нового питомца с некорректными данными, запрос возвращает статус 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_info_pet_without_photo(auth_key, name, animal_type, age)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    print(pet_id)
    assert status == 400  #тест не прошел, питомец с невалидными данными был создан
    assert result['name'] == name

def test_successful_delete_self_pet_id(pet_id='584879ec-00ca-43f2-ab6e-e003f61e617b'):
    """Удаление питомца по его ID"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_unsuccessful_add_new_pet_photo(name='', animal_type='Кошка',
                                     age='ыфафыаыф', pet_photo='cat1.jpg'):
    """Проверерка добавления питомца с некорректными данными, запрос возвращает статус 400"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400  #тест не прошел, питомец с невалидными данными был создан
    assert result['name'] == name

def test_unsuccessful_get_pets(filter='my_pets'):
    """ Проверка возможность получения списка питомцев по несуществующему API ключу"""
    email = 'Liza@liza.ru'
    password = '123'
    _, auth_key = pf.get_api_key(email, password)
    if auth_key != pf.get_api_key(valid_email, valid_password):
        print('Данный API ключ не существует, невозможно вывести список питомцев! ')
    else:
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.get_list_of_pets(auth_key, filter)
        assert status == 200
        assert len(result['pets']) > 0

def test_unsuccessful_delete_pets(pet_id='3f8aa309-57ec-463b-b739-2a00e484a569'):
    """ Проверка удаления питомца по не существующему API ключу"""
    email = 'Liza@liza.ru'
    password = '123'
    _, auth_key = pf.get_api_key(email, password)
    if auth_key != pf.get_api_key(valid_email, valid_password):
        print('Данный API ключ не существует, питомец не удален!')
    else:
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        assert status == 200
        assert pet_id not in my_pets.values()

def test_unsuccessful_add_new_pet_without_photo(name='Маша', animal_type='Кошка',age= 3, pet_photo=''):
    """Проверка возможности добавления питомца с корректными данными без фотографии"""
    if pet_photo != os.path.join(os.path.dirname(__file__), pet_photo):
        print('Питомец не создан, загрузите пожалуйта его фотографию!')
    else:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name

def test_unsuccessful_update_info_pet(name='Пышка',pet_id='0', animal_type='Белка', age=0):
    """Проверка невозможности отбновления информации о питомце при вводе не существующего ID"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 400











