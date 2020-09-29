Курс валют к рублю
------------------

## Задача

### Описание

Написать консольную программу, получающую на входе код валюты и дату. На выходе должен возвращаться курс рубля к указанной валюте на указанную дату.

Пример использования:

```
./currency.py EUR 2020-01-01

Курс рубля к EUR на 2020-01-01:
69,3777
```

Данные по котировкам взять из (XML API Центрального Банка России)[https://www.cbr.ru/development/SXML/] (ЦБР)

### Дополнительно

1. Добавить обработку ошибок и отображение справки при неправильном использовании программы
2. Написать модульные тесты, проверяющие работу основных функций программы

## Справка

### 1. Получение параметров из командной строки

Все переданные пользователем в программу параметры могут быть найдены в отдельной переменной, хранящейся в стандартном модуле sys: `sys.argv`. Переменная яляется списком (list). (Подробнее)[https://docs.python.org/3/library/sys.html#sys.argv]

Пример:

```python
import sys

print(
    "Number of arguments: {0}\nArg 1: {1}\nArg2: {2}".format(
        len(sys.argv),
        sys.argv[0],
        sys.argv[1]
    )
)
```

### 2. Получение данных с сервера

Для получения данных из API ЦБР, можно использовать модуль стандартной библиотеки Python (urllib.request)[https://docs.python.org/3/library/urllib.request.html].

Примеры использования:

1. https://webformyself.com/python-urllib-request-i-urlopen/
2. https://codecamp.ru/blog/python-urllib/

### 3. Поиск данных в файле

Получение конкретных данных из файла с курсами валют на данном этапе можно выполнить с использованием поиска подстроки в строке (функция find() подойдет).
