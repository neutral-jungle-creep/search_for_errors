import enchant
from loguru import logger
import speller


def write(file: str, new_data: list) -> None:
    '''Примет название файла. Запишет файл с именем result_{file}.csv в папку со сценарием.'''
    file = file.split('\\')[-1]
    with open(f'result_{file}.csv', 'w', encoding='utf-8') as file_output:
        file_output.write(head)
        file_output.writelines(new_data)
        logger.info(f'Записано {len(new_data)} строк.')


def check_word(word: str) -> bool:
    '''Примет слово. Если слово прошло проверку на грамматику, вернет правду.'''
    if dictionary_ru.check(word) or dictionary_custom.check(word) or dictionary_brands.check(word):
        return True
    else:
        if word not in false_words_set:
            false_words_set.append(word)
            logger.info(f'слово добавлено в false_words_set: {word}')
            speller.ya_speller(word)

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
        logger.info(f'Прочитано {len(data)} строк.')
    return data


def main() -> None:
    data = read(file := input('file name: '))  # bucket-25-dress-search
    new_data = check_lines(data)
    write(file, new_data)


if __name__ == '__main__':
    false_words_set = []  # список слов до проверки спеллера
    dictionary_ru = enchant.Dict('ru_RU')  # русский словарь из Либры
    dictionary_custom = enchant.Dict('ru_CUSTOM')  # пользовательский словарь
    dictionary_brands = enchant.Dict('brands')  # словарь с брендами
    # C:\CodePy\wb\spellcheck\venv\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell
    main()
