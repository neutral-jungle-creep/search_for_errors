'''
DOCSTRING: Makes a dictionary for the main program from a file
INPUT: brands.csv
OUTPUT: brands.dic
'''
import pandas as pd
from loguru import logger
import os


def spliter(item: str):
    result = ' '.join(item.split('|'))
    logger.info(result)
    return result


df = pd.read_csv('brand.csv', delimiter=';')
df['Synonyms'] = df['Synonyms'].apply(spliter)
df['Word'] += ' ' + df['Synonyms']
df = df['Word']

df.to_csv('brands_result.txt', header=False, index=False)

with open('brands_result.txt', 'r', encoding='utf-8') as file:
    brands = file.read().split()
    print(len(brands), *brands, sep='\n',
          file=open(r'C:\CodePy\wb\search_errors\venv\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell\brands.dic',
                    'w', encoding='utf-8'))

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'brands_result.txt')
os.remove(path)  # del brands_result.txt