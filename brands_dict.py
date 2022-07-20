'''
DOCSTRING: Makes a dictionary for the main program from a file
INPUT: brands.csv
OUTPUT: brands.dic
'''
import json
from loguru import logger


def write_dict(brands: list[str]) -> None:
    with open(r'venv\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell\brands.dic',
              'w', encoding='utf-8') as brands_dic_output, \
         open(r'venv\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell\brands.aff',
              'w', encoding='utf-8') as brands_aff_output:
        data = [x for xs in brands for x in xs]
        logger.debug(f'{len(data)}')
        brands_dic_output.write(str(len(data))+'\n')
        brands_dic_output.writelines(data)
        brands_aff_output.writelines(["SET UTF-8\n",
"TRY иаоентрвсйлпкыьямдушзбгчщюжцхфэъАКСВПМГБЛТДНИОРФЭЕХЧУЗШЯЮЦЖЙЩesianrtolcdugmphbyfvkwzESIANRTOLCDUGMPHBYFVKWZ'"])


def read_file() -> list:
    with open('brand_list.json', 'r', encoding='utf-8') as brands_input:
        data = json.load(brands_input)
        logger.debug(f'Прочитано {len(data)} записей.')
    return [[f'{word.lower()}\n' for word in brand["name"].split()] for brand in data]


def main() -> None:
    brands = read_file()
    write_dict(brands)


if __name__ == '__main__':
    main()
