import requests
import json
import string


def ya_speller(word: str) -> bool:
    '''Принимает строку. Возвращает булево значение в зависимости от корректности написания слова.'''
    endpoint = 'https://speller.yandex.net/services/spellservice.json/checkText?'
    params = {"text": word}

    with requests.session() as session:
        session.headers['User-Agent'] = 'insomnia/2022.2.1'

        response = session.get(endpoint, params=params)
        j_data = json.loads(response.text)
        if len(j_data) == 0 and word not in string.ascii_letters and word not in string.punctuation:
            return True
    return False
