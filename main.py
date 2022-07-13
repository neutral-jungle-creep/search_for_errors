import enchant
from loguru import logger
import speller


def rewrite_dict():
    with open(r'venv\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell\ru_CUSTOM.dic',
              'r', encoding='utf-8') as dict_input:
        dict_input.readline()
        words = dict_input.readlines()

    with open(r'venv\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell\ru_CUSTOM.dic',
              'w', encoding='utf-8') as dict_output:
        new_words = set(words + true_words)  # чтобы в словаре не было повторений
        logger.debug(f'В ru_CUSTOM.dic добавлено {len(new_words)} новых слов.')
        dict_output.write(f'{str(len(new_words))}\n')
        dict_output.writelines(new_words)


def write(file: str, new_data: list) -> None:
    '''Примет название файла. Запишет файл с именем result_{file}.csv в папку со сценарием.'''
    file = file.split('\\')[-1]
    with open(f'result_{file}.csv', 'w', encoding='utf-8') as file_output:
        file_output.write(head)
        file_output.writelines(new_data)
        logger.debug(f'Записано {len(new_data)} строк.')

    with open(f'result_false.txt', 'w', encoding='utf-8') as report:
        report.writelines(false_words)


def check_word(word: str) -> bool:
    '''Примет слово. Если слово прошло проверку на грамматику, вернет правду.'''
    if dictionary_ru.check(word) or dictionary_custom.check(word) or dictionary_brands.check(word):
        return True
    else:
        if f'{word}\n' not in false_words and f'{word}\n' not in true_words:
            logger.info(f'Слово, проверяемое спеллером: {word}')
            if speller.ya_speller(word):
                true_words.append(f'{word}\n')
                return True
            false_words.append(f'{word}\n')
            return False
        elif f'{word}\n' in true_words:
            return True
    return False


def check_lines(data: list) -> list:
    '''Примет список строк из файла. Вернет отредактированный список строк.'''
    new_data = []
    for line in data:
        for word in line.split('|')[0].replace('(', '').replace(')', '').split():
            if not check_word(word):
                new_data.append(line)
    return new_data


def read(file: str) -> list:
    '''Примет ссылку на файл без расширения. Вернет список строк файла без первой строки.'''
    with open(f'{file}.csv', 'r', encoding='utf-8') as file_input:
        global head
        head = file_input.readline()
        data = file_input.readlines()
        logger.debug(f'Прочитано {len(data)} строк.')
    return data


def main() -> None:
    data = read(file := input('file name: '))  # bucket-25-dress-search
    new_data = check_lines(data)
    write(file, new_data)
    rewrite_dict()


if __name__ == '__main__':
    true_words, false_words = [], []  # список из слов, прошедших проверку и не прошедших

    dictionary_ru = enchant.Dict('ru_RU')  # русский словарь из Либры
    dictionary_custom = enchant.Dict('ru_CUSTOM')  # пользовательский словарь
    dictionary_brands = enchant.Dict('brands')  # словарь с брендами
    # C:\CodePy\wb\search_errors\venv\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell
    main()
