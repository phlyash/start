from datetime import datetime
import urllib.request
import sys


def EXIT(message, exit_code):
    print(message)
    sys.exit(exit_code)


def date_check(dateinp):
    min_date = datetime(1992, 7, 1)
    max_date = datetime.today()

    if min_date >= dateinp or max_date <= dateinp:
        return False
    return True


EXIT_SUCCESS = 0
CURRENCY_ERROR = 1
DATE_ERROR = 2
EXIT_REFERENCE = 3
INPUT_ERROR = 4

if len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "-a":
    print(
        "usage: currency.py [valute code] [date: <format{yyyy-mm-dd}>]", "\n",
        "usage example: eur 2020-01-01", "\n",
        "this script has data from 1992-07-01", "\n",
        "other arguments: [-h] [-a] [-ec] [-exit_codes]", sep=""
          )
    EXIT("", EXIT_REFERENCE)
elif sys.argv[1] == "--exit-codes" or sys.argv[1] == "-e":
    print(
        "exit code 0: success", "\n",
        "exit code 1: currency-code format error", "\n",
        "exit code 2: date error(not in data base or date in future)", "\n",
        "exit code 3: references", sep=""
    )
    EXIT("", EXIT_REFERENCE)

if len(sys.argv) != 3:
    EXIT("Input should have format: <currency code> <date>.", INPUT_ERROR)

try:
    dateinp = datetime.strptime(sys.argv[2], "%Y-%m-%d")
except ValueError:
    EXIT("Date format error. Date should have format: yyyy-mm-dd.", DATE_ERROR)

currency = sys.argv[1].upper()

if date_check(dateinp):
    dateinp = datetime.strftime(dateinp, "%d/%m/%Y")
    url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + dateinp
    html = str(urllib.request.urlopen(url).read())

    if currency in html:
        EXIT(f"Курс рубля к {currency} на {dateinp}: "
             f"{html[html.find('Value', html.find(currency)) + 6:html.find('Value',html.find(currency)) + 13]}",
             EXIT_SUCCESS)
    else:
        EXIT(f"error: currency({currency}) not found", CURRENCY_ERROR)
else:
    EXIT("error: date input", DATE_ERROR)
