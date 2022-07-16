import enchant
from loguru import logger
import speller
import os


def write_dict(dicts: tuple) -> None:
    '''Примет кортеж с прочитанными словарями, добавит новые слова, полученные из спеллера в них.'''
    with open(f'{link}\\ru_CUSTOM.dic', 'w', encoding='utf-8') as custom_output, \
            open(f'{link}\\ru_ERRORS.dic', 'w', encoding='utf-8') as errors_output:
        new_true_words, new_false_words = dicts[0] + true_words, dicts[1] + false_words
        custom_output.write(f'{str(len(new_true_words))}\n')
        errors_output.write(f'{str(len(new_false_words))}\n')
        custom_output.writelines(new_true_words)
        errors_output.writelines(new_false_words)
        logger.debug(f'В ru_CUSTOM.dic добавлено {len(true_words)} новых слов.')
        logger.debug(f'В ru_ERRORS.dic добавлено {len(false_words)} новых слов.')


def read_dict() -> tuple:
    '''Прочитает словари из библиотеки, вернет кортеж с данными из них.'''
    custom_words, errors_words = [], []
    try:
        with open(f'{link}\\ru_CUSTOM.dic', 'r', encoding='utf-8') as custom_input, \
             open(f'{link}\\ru_ERRORS.dic', 'r', encoding='utf-8') as errors_input:
            custom_input.readline()
            errors_input.readline()
            custom_words, errors_words = custom_input.readlines(), errors_input.readlines()
    except Exception:
        pass
    return custom_words, errors_words


def write(file: str, new_data: list) -> None:
    '''Примет название файла. Запишет файл с именем result_{file}.csv в папку со сценарием.'''
    file = file.split('\\')[-1]
    with open(f'reports\\result_{file}.csv', 'w', encoding='utf-8') as file_output:
        file_output.write(head)
        file_output.writelines(new_data)
        logger.debug(f'В файл отчета записано {len(new_data)} строк с ошибками.')


def check_word(word: str) -> bool:
    '''Примет слово. Если слово прошло проверку на грамматику, вернет правду.'''
    global counter
    if dictionary_ru.check(word) or dictionary_custom.check(word) or dictionary_brands.check(word):
        return True
    elif dictionary_errors.check(word):
        return False
    else:
        if f'{word}\n' not in false_words and f'{word}\n' not in true_words:
            counter += 1
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
    stop = 0
    new_data = []
    for line in data:
        if not stop:
            for word in line.split('|')[0].replace('(', '').replace(')', '').split():
                if 9_000 == counter:  # лимит запросов api в сутки
                    stop = 1
                    logger.debug(f'Лимит запросов в сутки израсходован: {counter}')
                    break
                if not check_word(word):
                    new_data.append(line)
        else:
            return new_data
    return new_data


def read(file: str) -> list:
    '''Примет ссылку на файл без расширения. Вернет список строк файла без первой строки.'''
    with open(f'{file}.csv', 'r', encoding='utf-8') as file_input:
        global head
        head = file_input.readline()
        data = file_input.readlines()
        logger.debug(f'Прочитано {len(data)} строк.')
    return data


def make_dir():
    '''Создаст папку для отчетов, если она еще не существует.'''
    try:
        os.mkdir('reports')
    except Exception:
        pass


def main() -> None:
    make_dir()
    data = read(file := input('Путь к файлу: '))
    new_data = check_lines(data)
    write(file, new_data)
    write_dict(read_dict())


if __name__ == '__main__':
    link = 'venv\\Lib\\site-packages\\enchant\\data\\mingw64\\share\\enchant\\hunspell'  # ссылка на словари
    true_words, false_words = [], []  # список из слов, прошедших проверку и не прошедших
    counter = 0

    dictionary_ru = enchant.Dict('ru_RU')  # русский словарь из Либры
    dictionary_custom = enchant.Dict('ru_CUSTOM')  # пользовательский словарь
    dictionary_errors = enchant.Dict('ru_ERRORS')  # пользовательский словарь с неверными словами
    dictionary_brands = enchant.Dict('brands')  # словарь с брендами
    main()
