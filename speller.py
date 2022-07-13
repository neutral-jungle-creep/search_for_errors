import requests
import json
import string


def ya_speller(query: str) -> bool:
    '''Проверяет слова, которые не прошли проверку словарями, с помощью api.'''
    endpoint = 'https://speller.yandex.net/services/spellservice.json/checkText?'
    params = {"text": query}

    with requests.session() as session:
        session.headers['User-Agent'] = 'insomnia/2022.2.1'

        response = session.get(endpoint, params=params)
        j_data = json.loads(response.text)
        if len(j_data) == 0 and query not in string.ascii_letters and query not in string.punctuation:
            return True
    return False
