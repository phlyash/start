from datetime import datetime
import urllib.request
import sys


def shutdown(message, exit_code):
    print(message)
    sys.exit(exit_code)


def date_check(dateinp):
    min_date = datetime(1992, 7, 1)
    max_date = datetime.today()

    return min_date <= dateinp <= max_date


EXIT_SUCCESS = 0
CURRENCY_ERROR = 1
DATE_ERROR = 2
EXIT_REFERENCE = 3
INPUT_ERROR = 4
reversed_check = False

if len(sys.argv) == 1 or sys.argv[1] in ("-a", "-h"):
    print(
        "usage: currency.py [valute code] [date: <format{yyyy-mm-dd}>]", "\n",
        "usage example: eur 2020-01-01", "\n",
        "this script has data from 1992-07-01", "\n",
        "in default program show direct quotations", "-n"
        "other arguments: [-h] [-a] [-e] [--exit-codes] [-r] [--reverse-quotation] [-u] [--usage]", sep=""
          )
    shutdown("help shown successful", EXIT_REFERENCE)
elif sys.argv[1] in ("--exit-codes", "-e"):
    print(
        "exit code 0: success", "\n",
        "exit code 1: currency-code format error", "\n",
        "exit code 2: date error(not in data base or date in future)", "\n",
        "exit code 3: references", sep=""
    )
    shutdown("help shown successful", EXIT_REFERENCE)
elif sys.argv[1] in ("--usage", "-u"):
    print(
        "arguments help:", "\n",
        "-h || -a : show basics for using program", "\n",
        "-e || --exit-codes : show all exit codes with decoding it", "\n",
        "-r || --reverse-quotation : show reverse quotations for currency you asked", sep=""
    )
    shutdown("help shown successful", EXIT_REFERENCE)

try:
    dateinp: datetime = datetime.strptime(sys.argv[2], "%Y-%m-%d")
    reversed_check = len(sys.argv) > 2 and sys.argv[len(sys.argv)-1] in ("-r", "--reverse-quotation")
except ValueError:
    shutdown("Date format error. Date should have format: yyyy-mm-dd.", DATE_ERROR)

currency = sys.argv[1].upper()

if date_check(dateinp):
    dateinp = datetime.strftime(dateinp, "%d/%m/%Y")
    url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + dateinp
    html = str(urllib.request.urlopen(url).read())
    if currency in html:
        if not reversed_check:
            shutdown(f"Курс рубля к {currency} на {dateinp}: "
            f"{html[html.find('Value', html.find(currency)) + 6:html.find(',', html.find(currency)) + 5].replace(',', '.')}",
            EXIT_SUCCESS)
        else:
            shutdown(f"Курс {currency} к рублю на {dateinp}: "
                 f"{'%.4f' % (1 / float(html[html.find('Value', html.find(currency)) + 6:html.find(',', html.find(currency)) + 5].replace(',', '.')))}",
                 EXIT_SUCCESS)
    else:
        shutdown(f"error: currency({currency}) not found", CURRENCY_ERROR)
else:
    shutdown("error: date input", DATE_ERROR)
