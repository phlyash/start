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
    for i in range(len(date)):
        date[i] = int(date[i])
        if i == 0:
            if date[i] // 1000 == 0 or date[i] > time.time() // 31536000 + 1970 or date[i] <= 1991:
                return False
        elif i == 1:
            if days_in_month(date[1], date[0]) == False or (date[0] == 1992 and date[1] < 7) or (int(time.strftime("%D", time.localtime())[0:2]) < date[i]):
                return False
        elif i == 2:
            if days_in_month(date[1], date[0]) < date[i] or date[i] < 0 or (int(time.strftime("%D", time.localtime())[3:5]) < date[i]):
                return False
        else:
            return False
    return True


inp = list()
while 1 < len(sys.argv) < 3 and 0 <= len(inp) < 2:
    print("input format: "
          "currency code date{yyyy-mm-dd}", "\n"
          "example: eur 2020-01-01", "\n"
          "program has data from 01-07-1992")
    inp = input().split()
else:
    if 2 < len(sys.argv):
        inp.append(sys.argv[1])
        inp.append(sys.argv[2])
currency = inp[0]
date = inp[1]  # y-m-d
if date_check(date):
    lst = date.split("-")  # d/m/y
    lst[0], lst[2] = lst[2], lst[0]  # swap day and year for cbr format
    date = "/".join(lst)  # date for cbr
    url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date
    html = str(urllib.request.urlopen(url).read())
    if currency.upper() in html:
        print(f"Курс рубля к {currency.upper()} на {date}: "
              f"{html[html.find('Value', html.find(currency.upper())) + 6:html.find('Value',html.find(currency.upper())) + 13]}")
        sys.exit(0)
    else:
        print(f"error: currency({currency}) not found")
        sys.exit(1)
else:
    print("error: date format")
    sys.exit(2)