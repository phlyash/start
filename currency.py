from datetime import datetime
import urllib.request
import sys


def EXIT(message, exit_code):
    print(message)
    sys.exit(exit_code)


def date_check(dateinp):
    min_date = datetime(1992, 7, 1)
    max_date = datetime.today()

    if min_date <= dateinp <= max_date:
        return True
    return False


EXIT_SUCCESS = 0
CURRENCY_ERROR = 1
DATE_ERROR = 2
EXIT_REFERENCE = 3
INPUT_ERROR = 4
rFlag = False

if len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "-a":
    print(
        "usage: currency.py [valute code] [date: <format{yyyy-mm-dd}>]", "\n",
        "usage example: eur 2020-01-01", "\n",
        "this script has data from 1992-07-01", "\n",
        "in default program show direct quotations", "-n"
        "other arguments: [-h] [-a] [-e] [--exit-codes] [-r] [--reverse-quotation] [man]", sep=""
          )
    EXIT("help shown successful", EXIT_REFERENCE)
elif sys.argv[1] == "--exit-codes" or sys.argv[1] == "-e":
    print(
        "exit code 0: success", "\n",
        "exit code 1: currency-code format error", "\n",
        "exit code 2: date error(not in data base or date in future)", "\n",
        "exit code 3: references", sep=""
    )
    EXIT("help shown successful", EXIT_REFERENCE)
elif sys.argv[1] == "man":
    print(
        "arguments help:", "\n",
        "-h || -a : show basics for using program", "\n",
        "-e || --exit-codes : show all exit codes with decoding it", "\n",
        "-r || --reverse-quotation : show reverse quotations for currency you asked", sep=""
    )

try:
    dateinp = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    if sys.argv[3] == "-r" or sys.argv[3] == "--reverse-quotations":
        rFlag = True
except ValueError:
    EXIT("Date format error. Date should have format: yyyy-mm-dd.", DATE_ERROR)
except IndexError:
    pass

currency = sys.argv[1].upper()

if date_check(dateinp):
    dateinp = datetime.strftime(dateinp, "%d/%m/%Y")
    url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + dateinp
    html = str(urllib.request.urlopen(url).read())
    if currency in html:
        if not rFlag:
            EXIT(f"Курс рубля к {currency} на {dateinp}: "
            f"{html[html.find('Value', html.find(currency)) + 6:html.find(',', html.find(currency)) + 5].replace(',', '.')}",
            EXIT_SUCCESS)
        else:
            EXIT(f"Курс {currency} к рублю на {dateinp}: "
                 f"{'%.4f' % (1 / float(html[html.find('Value', html.find(currency)) + 6:html.find(',', html.find(currency)) + 5].replace(',', '.')))}",
                 EXIT_SUCCESS)
    else:
        EXIT(f"error: currency({currency}) not found", CURRENCY_ERROR)
else:
    EXIT("error: date input", DATE_ERROR)
