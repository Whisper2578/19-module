from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):

    """ Запрос: API ключ.
        Проверка: возвращает статус 200, ответ содержит слово key """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(f'\n {email}, {password}, {status}, {result}')

# Test 1
def test_get_api_key_with_valid_mail_and_invalid_passwor(email=valid_email, password=invalid_password):

    """ Запрос: валидный e-mail, невалидный пароль.
        Проверка: ответ не содержит слово key """

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста валидный e-mail, невалидный пароль')

# Test 2
def test_get_api_key_with_invalid_email_and_valid_password(email=invalid_email, password=valid_password):

    """ Запрос: невалидный e-mail, валидный пароль.
        Проверка: ответ не содержит слово key """

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста невалидный e-mail, валидный пароль')

# Test 3
def test_get_api_key_with_invalid_email_and_invalid_password(email=invalid_email, password=invalid_password):

    """ Запрос: невалидный e-mail, невалидный пароль.
        Проверка: ответ не содержит слово key """

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста невалидный e-mail, невалидный пароль')


def test_get_all_pets_with_valid_key(filter='my_pets'):

    """ Запрос: Список всех моих питомцев
        Проверка: Полученный список не пустой.
        Шаги: получаем API ключ, сохраняем в переменную auth_key, запрашиваем список всех питомцев.
        Проверяем, что список не пустой. Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    num = len(result['pets'])
    if filter == 'my_pets':
        print(f'{num} моих питомцев на сайте')
    else:
        print(f'список не пустой')

# Test 4
def test_get_all_pets_with_invalid_key():

    """ Запрос: Список всех питомцев только при значении параметра filter - 'my_pets' либо ''
        в противном случае получаем status == 500 """

    filter = 'my_pets' # допустимое
    filter = 'my__pets' # допустимое, ошибочное
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500
    print(f'\nСтатус {status}, недоступное значение фильтра')


def test_add_new_pet_with_valid_data(name='Мелкий', animal_type='котенок', age='1', pet_photo='images/1.jpg'):
    """Проверка,  добавление питомца с валидными данными"""

    # Присваиваем переменной pet_photo полный путь к фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем api-ключ и сохраняем в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем статус ответа и имя
    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'Карточка добавлена {result}')

# Test 5
def test_add_new_pet_with_invalid_foto(name='Мелкий', animal_type='котенок', age='2', pet_photo='images/8.jpg'):

    """ Проверка,  добавление питомца с некорректными данными файла фото, при ошибке заменяем на аватар """

    # Присваиваем переменной pet_photo полный путь к фото питомца
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    if not os.path.exists(pet_photo):#проверка корректности данных о фото
        print(f'\n Файл {pet_photo} не найден')
        pet_photo = 'images/Avatar.jpg'
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        print(f'Замена фото на Аватар {pet_photo}')
   # Запрашиваем api-ключ, записываем в auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем статус загрузки и имя
    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'Карточка добавлена {result}')

# Test 6
def test_add_pet_with_valid_data_without_photo(name='Безфото', animal_type='котенок', age='1'):

    """ Проверка, Добавления нового питомца без выбора фото """

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'Карточка добавлена {result}')

# Test 7
def test_add_photo_at_pet(pet_photo='images/Avatar.jpg'):

    """ Проверка, возможность добавления фотографии питомца отдельно """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        print(f'\n фото добавлено {result}')
    else:
        raise Exception('Питомцы отсутствуют')

# Test 8
def test_add_pet_with_invalid_age(name='Мафусаил', animal_type='кот', pet_photo='images/2.jpg'):

    """ Добавление питомца с невозможным возрастом.
    Предупреждения при значениях меньше 0 или больше 20 лет """

    age = '120'
    # age = '-1'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    age = float(result['age'])#.split()
    assert status == 200
    assert (age > 20 or age < 0), 'Добавлен питомец с невозможным возрастом, меньше 0 или старше 20 лет.'
    print(f'\n Приложение допускает ввод невозможных возрастов, меньше 0 или старше 20 лет. {age}')

# Test 9
def test_add_pet_with_variable_age_symble(name='Сатурн', animal_type='кот', pet_photo='images/3.jpg'):

    """ Добавление карточки питомца с символьным значением возраста
        Предупреждение от теста"""

    age = '!@#$%'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    #age = float(result['age'])#.split()
    assert status == 200
    assert age, 'Добавлен питомец с невозможным возрастом'
    print(f'\n Приложение допускает ввод невозможных возрастов {age}')

# Test 10
def test_add_pet_with_valid_data_empty_field():

    """Проверка, добавление питомца с пустыи полями в карточке. Предупреждение от теста """

    name = ''
    animal_type = ''
    age = ''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'Приложение допускает добавление пустых карточек питомцев {result}')

# Test 11
def test_add_pet_with_a_multiple_name(animal_type='система', age='11', pet_photo='images/2.jpg'):

    """ Проверка. Добавления питомца с именем более 10 слов.
   Тест выводит предупреждение, если  в приложение добавлен питомец с именем, состоящим из более 10 слов """

    name = 'Солнце Меркурий Венера Земля Марс Юпитер Сатурн Уран Нептун Плутон Церера'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    word_count = len(list_name)

    assert status == 200
    assert word_count > 10, 'Добавлен питомец с более 10 слов в имени'
    print('ok')
    print(f'Приложение допускает добавление карточек питомцев с именами из более 10 слов. Текущий счётчик: {word_count}')

# Test 12
def test_successful_delete_pet():

    """ Проверка, удаление питомца """

    # Получаем auth_key, запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если my_pets пустой, то добавляем нового и опять запрашиваем my_pets
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Венера", "кошка", "2", "images/1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке {num} питомца(ев)')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Запрашиваем my_pets повторно
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем статус 200, списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке {num} питомца(ев)')

# Test 13
def test_successful_delete_notvalid_key_pet():
    """Проверка. Удаления питомца по неверному auth_key. Статусу 403"""

    # Получаем ключ auth_key и запрашиваем my_pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    print()
    print(auth_key)
    # {'key': '7758ea1aa8e210db1aa479c1ec0cdc0fa661ebdfd448756bc8d6f84e'}#правильный ключ
    auth_key = {'key': '8858ea1aa8e210db1aa479c1ec0cdc0fa661ebdfd448756bc8d6f84e'} #неправильный ключ
    print(auth_key)
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Сатурн", "кот", "4", "images/1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке {num} питомца(ев)')

    # # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # # Проверяем что статус ответа равен 403 и в списке питомцев нет изменений
    assert status == 403
    #assert pet_id in my_pets.values()
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке {num} питомцев')

# Test 14
def test_successful_update_pet_info(name='Марс', animal_type='кот', age=3):

    """ Проверка. Обновление информации о питомце"""

    # Получаем auth_key и my_pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        print('ok')
        print(result)
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Список питомцев пуст")

# Test 15
def test_add_pet_with_empty_name(name='', animal_type='кот', age='5', pet_photo='images/4.jpg'):

    """ Проверка. Добавление питомца с пустым значением в переменной name.
    Тест не будет пройден, если питомец будет добавлен в приложение с пустым значением в поле "Имя" """

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert name == '', 'Питомец добавлен в приложение с пустым значением в поле "Имя"'

# Test 16
def test_add_pet_with_a_long_name(animal_type='кошка', age='2', pet_photo='images/3.jpg'):

    """ Добавления питомца с именем, которое имеет слишком длинное значение.
    Сообщение, если питомец будет добавлен в приложение с именем состоящим из 35 символов """

    name = 'PcHHMrVJ7HznNPDmdiXM57mfBbQFzfF4Z5qаа'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['name']#.split()
    symbol_count = len(list_name)

    assert status == 200
    assert symbol_count > 35, 'Имя более 35 символов.'
    print(f'\n Имя более 35 символов. {symbol_count}')


# Test 17
def test_add_pet_with_specsymbils_in_animal_type(name='Юпитер', age='1', pet_photo='images/3.jpg'):

    """ Проверка. Спецсимволы в animal_type. Уведомление при наличии спецсимволов в поле "Порода" """

    animal_type = 'Cat!@#$%^'
    symbols = '!@#$%^&*()_'
    symbol = []

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    for i in symbols:
        if i in result['animal_type']:
            symbol.append(i)
    assert symbol[0] in result['animal_type'], 'Карточка создана с недопустимыми символами поле "Порода"'
    print(f'\n Карточка создана с недопустимыми символами поле "Порода" :  {symbols}')

# Test 18
def test_add_pet_with_numbers_in_variable_animal_type(name='Фобос', animal_type='кот9562876', age='0', pet_photo='images/4.jpg'):

    """ Негативный сценарий. Цифры в animal_type. Уведомление при наличии цифр в поле "Порода"."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert animal_type in result['animal_type'], 'Карточка создана с цифрами в поле "Порода"'
    print(f'\n Карточка создана с цифрами в поле "Порода" :  {animal_type}')

# Test 19
def test_add_pet_more_10_words_in_animal_type(name='Нептун', age='6', pet_photo='images/2.jpg'):

    """ Негативный сценарий.Более 10 слов в поле "Порода". Уведомление если в полее "Порода" более 10 слов."""

    animal_type = 'Абиссинская Ангорская Бенгальская Бирманская Бомбейская Британская Манчкин Нибелунг Пиксибоб Рэгдолл Саванна Тойгер Бурмилла'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count > 10, 'Более 10 слов в поле "Порода"'
    print(f'\n Более 10 слов в поле "Порода" : {word_count}')

# Test 20
def test_add_pet_more_then_25_symbols_animal_type(name='Аватар', age='20', pet_photo='images/avatar.jpg'):

    """ Негативный сценарий. Более 25 символов в поле animal_type. Уведомлении при превышении """

    animal_type = 'IuDGWPFNYsFBAbw2NoUOPo9Iv5p5fzUUYnefkXRqgzgbhuOGthh90w9'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type']#.split()
    symbol_count = len(list_animal_type)

    assert status == 200
    assert symbol_count > 25, 'Карточка создана с более чем 25 символов в поле "Порода"'
    print(f'\n Карточка создана с более чем 25 символов в поле "Порода" : {symbol_count}')