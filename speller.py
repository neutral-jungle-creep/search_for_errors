import requests
import json
import string


true_words = []  # список из слов, прошедших проверку
false_words = []  # список слов, не прошедших проверку


def ya_speller(query: str):
    # проверяет слова, которые не прошли проверку словарями, с помощью api
    endpoint = 'https://speller.yandex.net/services/spellservice.json/checkText?'
    params = {"text": query}

    with requests.session() as session:
        session.headers['User-Agent'] = 'insomnia/2022.2.1'

        response = session.get(endpoint, params=params)
        j_data = json.loads(response.text)
        if len(j_data) == 0 and query not in string.ascii_letters and query not in string.punctuation:
            true_words.append(query)
        else:
            false_words.append(query)