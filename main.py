import enchant
import pandas as pd
import csv
from loguru import logger
import speller

file_name = input('file name: ')  # bucket-25-dress-search
df = pd.read_csv(f'{file_name}.csv', delimiter='|')
df['error'] = 0
false_words_set = []  # список слов до проверки спеллера
dictionary_ru = enchant.Dict('ru_RU')
dictionary_custom = enchant.Dict('ru_CUSTOM')
# C:\CodePy\wb\spellcheck\venv\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell
dictionary_brands = enchant.Dict('brands')  # словарь с брендами


def word_check(item):
    # проверяет наличие слова в одном из словарей
    if dictionary_ru.check(item) or dictionary_custom.check(item) or dictionary_brands.check(item):
        return True
    if item not in false_words_set:
        false_words_set.append(item)
        logger.info(f'слово добавлено в false_words_set: {item}')
        speller.ya_speller(item)
    return False


def query_check(serie: pd.Series):
    debracket = serie.replace('(', '').replace(')', '')
    debracket: str
    list_from_str = debracket.split()
    result = all(map(word_check, list_from_str))
    if not result:
        logger.info(f'запрос, не прошедший проверку: {list_from_str}')
    return result


df['error'] = df['Search Query'].apply(query_check)

trunc_df = df.loc[df['error'] == False]
trunc_df.to_csv(f'result_{file_name}.csv', sep='|', quoting=csv.QUOTE_NONE)
print(*false_words_set, sep='\n',
      file=open('reports\\result_words_for_speller.txt', 'w', encoding='utf-8'))

print(*speller.true_words, sep='\n',
      file=open('reports\\result_true.txt', 'w', encoding='utf-8'))  # слова, прошедшие проверку спеллера
print(*speller.false_words, sep='\n',
      file=open('reports\\result_false.txt', 'w', encoding='utf-8'))  # слова, не прошедшие проверку спеллера

