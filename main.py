import enchant
from loguru import logger
import speller


def rewrite_dict():
    '''Перепишет пользовательские словари с верными словами и с ошибочными, добавит в них новые,
     проверенные с помощью апи слова.'''
    link = 'venv\\Lib\\site-packages\\enchant\\data\\mingw64\\share\\enchant\\hunspell'

    with open(f'{link}\\ru_CUSTOM.dic', 'r', encoding='utf-8') as custom_input, \
         open(f'{link}\\ru_ERRORS.dic', 'r', encoding='utf-8') as errors_input:
        custom_input.readline()
        errors_input.readline()
        custom_words, errors_words = custom_input.readlines(), errors_input.readlines()

    with open(f'{link}\\ru_CUSTOM.dic', 'w', encoding='utf-8') as custom_output, \
         open(f'{link}\\ru_ERRORS.dic', 'r', encoding='utf-8') as errors_output:
        new_true_words, new_false_words = set(custom_words + true_words), set(errors_words + false_words)
        custom_output.write(f'{str(len(new_true_words))}\n')
        errors_output.write(f'{str(len(new_false_words))}\n')
        custom_output.writelines(new_true_words)
        errors_output.writelines(new_false_words)
        logger.debug(f'В ru_CUSTOM.dic добавлено {len(new_true_words)} новых слов.')
        logger.debug(f'В ru_ERRORS.dic добавлено {len(new_false_words)} новых слов.')


def write(file: str, new_data: list) -> None:
    '''Примет название файла. Запишет файл с именем result_{file}.csv в папку со сценарием.'''
    file = file.split('\\')[-1]
    with open(f'result_{file}.csv', 'w', encoding='utf-8') as file_output:
        file_output.write(head)
        file_output.writelines(new_data)
        logger.debug(f'Записано {len(new_data)} строк.')


def check_word(word: str) -> bool:
    '''Примет слово. Если слово прошло проверку на грамматику, вернет правду.'''
    if dictionary_ru.check(word) or dictionary_custom.check(word) or dictionary_brands.check(word):
        return True
    elif dictionary_errors.check(word):
        pass
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
    dictionary_errors = enchant.Dict('ru_ERRORS')  # пользовательский словарь с неверными словами
    dictionary_brands = enchant.Dict('brands')  # словарь с брендами
    main()
