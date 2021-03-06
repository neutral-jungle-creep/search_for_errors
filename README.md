### ПОИСК ОРФОГРАФИЧЕСКИХ ОШИБОК

Скрип создан для поиска ошибок в части человеческого запроса в датасторе. 

---

#### Описание 

Для проверки используется библиотека pyenchant, 
которая не поддерживает проверку русского языка, поэтому в нее был добавлен русскоязычный словарь, взятый
из файлов LibreOffice.

Словарь из офиса включает в себя очень мало слов. Пользуясь только методом проверки
через словари из 90 тыс строк скриптом было определено 28 тыс строк как неверные.

Чтобы улучшить ситуацию, был создан сценарий speller.py. Этот скрипт отправляет слово в api для проверки орфографии, который
знает намного больше слов и брендов, но имеет большой недостаток - лимит 10 тыс запросов в сутки. Именно поэтому api был использован как 
дополнительный инструмент после проверки словарями. 

В конце каждой проверки пользовательские словари правильных и ошибочных слов пополняются для того, чтобы как можно реже
обращаться к сценарию speller.py в дальнейшем.

---

#### Алгоритм работы скрипта:
1. На вход скрипт получает из консоли путь к файлу, который требуется проверить, с названием файла без расширения.
2. Прочитанный файл проверяется построчно.
3. Каждое слово из части человеческого запроса отправляется в функцию для проверки.
   - Если слово есть в одном из словарей с верными словами, вернет правду
   - Иначе если слово есть в словаре с ошибочными словами, вернет ложь
   - Иначе обратится к api
     - Если слово правильное по результатам из api, запишет слово в список верных, вернет правду
     - Иначе запишет слово в список ошибочных, вернет ложь
4. Если функция для проверки вернула ложь хотя бы один раз для строки, добавит строку в список с ошибочными
5. Запишет файл со строками, в которых есть ошибки.
6. Перепишет пользовательские словари, добавив туда новые слова из списков с верными и ошибочными словами.

---

#### Планируется добавить

1. Возможность проверки части query записи
2. Научить скрипт распознавать больше брендов
3. Сделать пути к файлам универсальными для всех ОС