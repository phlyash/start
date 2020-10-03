import urllib.request
import sys
import time


def leap_year_check(year):
    if year % 4 == 0 and (year % 400 == 0 or year % 100 != 0):
        return True
    else:
        return False


def days_in_month(month, year):
    if month == 2:
        if leap_year_check(year):
            return 29
        else:
            return 28
    if 1 <= month <= 7:
        if month % 2 == 0:
            return 30
        else:
            return 31
    elif 7 < month <= 12:
        if month % 2 == 0:
            return 31
        else:
            return 30
    else:
        return False


def date_check(date):
    date = date.split("-")
    if len(date) == 3:
        date[0] = int(date[0])
        date[1] = int(date[1])
        date[2] = int(date[2])
        if date[0] // 1000 == 0 or date[0] > time.time() // 31536000 + 1970 or date[0] <= 1991:
            return False
        if days_in_month(date[1], date[0]) == False or (date[0] == 1992 and date[1] < 7) or (int(time.strftime("%D", time.localtime())[0:2]) < date[1]):
            return False
        if days_in_month(date[1], date[0]) < date[2] or date[2] < 0 or (int(time.strftime("%D", time.localtime())[3:5]) < date[2]):
            return False
    else:
        return False
    return True


if len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "-a":
    print(
        "usage: currency.py [valute code] [date: <format{yyyy-mm-dd}>]", "\n",
        "usage example: eur 2020-01-01", "\n",
        "this script has data from 1992-07-01", "\n",
        "other arguments: [-h] [-a] [-ec] [-exit_codes]", sep=""
          )
    sys.exit("exit code: 3")
elif sys.argv[1] == "-exit_codes" or sys.argv[1] == "-ec":
    print(
        "exit code 0: success", "\n",
        "exit code 1: currency-code format error", "\n",
        "exit code 2: date error(not in data base or date in future)", "\n",
        "exit code 3: references", sep=""
    )
    sys.exit("exit code: 3")
currency = sys.argv[1]
date = sys.argv[2] # y-m-d
if date_check(date):
    lst = date.split("-")  # d/m/y
    lst[0], lst[2] = lst[2], lst[0]  # swap day and year for cbr format
    date = "/".join(lst)  # date for cbr
    url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date
    html = str(urllib.request.urlopen(url).read())
    if currency.upper() in html:
        print(f"Курс рубля к {currency.upper()} на {date}: "
              f"{html[html.find('Value', html.find(currency.upper())) + 6:html.find('Value',html.find(currency.upper())) + 13]}")
        sys.exit("exit code: 0")
    else:
        print(f"error: currency({currency}) not found")
        sys.exit("exit code: 1")
else:
    print("error: date input")
    sys.exit("exit code: 2")