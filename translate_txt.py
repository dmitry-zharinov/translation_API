"""
Created on Thu Mar 30 08:52:21 2017

@author: dzharinov
"""

import requests
import os
import os.path
import glob

API_KEY = 'trnsl.1.1.20170327T164144Z.43d4a02aa159f9d3.87456492d5e507a9b20d9a8a56545108971a440c'


def read_file(path):
    try:
        with open(path) as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print('Файл не найден')


def write_file(filename, text, lang_to):
    # имя файла
    filename = '{}-{}'.format(lang_to, filename)
    # директория
    result_dir = 'translated-{}'.format(lang_to)
    os.makedirs(result_dir, exist_ok=True)
    path = os.path.join(result_dir, filename)
    with open(path, mode='w', encoding='utf-8') as file:
        file.write(text)
        print('Создан файл {}'.format(path))


# функция получения поддерживаемых языков
def api_get_langs():
    url = 'https://translate.yandex.net/api/v1.5/tr.json/getLangs'
    params = {
        'key': API_KEY,
        'ui': 'ru'
    }
    response = requests.get(url, params=params).json()
    return response['langs']


# функция распознавания языка
def api_detect_lang(text):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
    params = {
        'key': API_KEY,
        'text': text
    }
    response = requests.get(url, params=params).json()
    if response.get('code') == 200:
        return response['lang']


# функция перевода
def api_translate(text, lang_from, lang_to='ru'):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    language = '{}-{}'.format(lang_from, lang_to)
    params = {
        'key': API_KEY,
        'lang': language,
        'text': text
    }
    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))


def main():
    result_language = None
    lang_list = api_get_langs()
    while result_language is None:
        result_lang_input = str(input('На какой язык необходимо перевести файлы? (help - вывести список)'))
        # вывести список языков
        if result_lang_input == 'help':
            languages = list(sorted(lang_list.values()))
            print('\n'.join(languages))
            result_language = None
        # найти код языка
        else:
            result_lang_input = result_lang_input[0].upper() + result_lang_input[1:]
            for k, v in lang_list.items():
                if v == result_lang_input:
                    result_language = k
                    break
            else:
                print('Язык {} не найден. Попробуйте ещё раз!'.format(result_lang_input))

    files = glob.glob(os.path.join('', "*.txt"))
    for file in files:
        ans = input('\nБудет переведён файл {}. Продолжить? y/n '.format(file))
        if ans == 'y':
            # читаем файл
            text = read_file(file)
            # определяем язык
            lang_from = api_detect_lang(text)
            if lang_from is None:
                print('Ошибка: язык в файле {} не распознан!'.format(file))
                continue
            # переводим
            result = api_translate(text, lang_from, result_language)
            # пишем в файл
            write_file(file, result, result_language)
            print('Успешно!')


main()
