from datetime import datetime
import urllib.request
import sys


def download():
    return str(urllib.request.urlopen(url).read())


def date_check(dateinp):
    try:
        dateinp: datetime = datetime.strptime(dateinp, "%Y-%m-%d")
        min_date = datetime(1992, 7, 1)
        max_date = datetime.today()

        return min_date <= dateinp <= max_date
    except ValueError:
        return False


def parse(html, currency, reversed_check):
    currency = currency.upper()
    if currency not in html:
        return CURRENCY_ERROR

    if not reversed_check:
        return html[html.find('Value', html.find(currency)) + 6:html.find(',', html.find(currency)) + 5].replace(',', '.')

    return '%.4f' % (1 / float(html[html.find('Value', html.find(currency)) + 6:html.find(',', html.find(currency)) + 5].replace(',', '.')))


def main(args, get_html):

    TEXT_HELP_AND_USAGE = (
        "usage: currency.py [valute code] [date: <format{yyyy-mm-dd}>]\n",
        "usage example: eur 2020-01-01\n",
        "this script has data from 1992-07-01\n",
        "in default program show direct quotations\n"
        "other arguments: [-h] [-a] [-e] [--exit-codes] [-r] [--reverse-quotation]\n",
        "with [-r] argument you can see reversed quotations (1 rubble in [valute])"
    )
    TEXT_EXIT_CODES = (
        "exit code 0: success\n",
        "exit code 1: currency-code format error\n",
        "exit code 2: date error(not in data base or date in future)\n",
        "exit code 3: references"
    )

    if len(args) == 1 or args[1] in ("-a", "-h"):
        print(*TEXT_HELP_AND_USAGE, sep="")
        return EXIT_REFERENCE
    elif args[1] in ("--exit-codes", "-e"):
        print(*TEXT_EXIT_CODES, sep="")
        return EXIT_REFERENCE

    reversed_check = len(args) > 2 and args[len(args)-1] in ("-r", "--reverse-quotation")
    try:
        currency = args[1]
        dateinp = args[2]
    except IndexError:
        print("Not enough arguments")
        return INPUT_ERROR

    if not date_check(dateinp):
        print("error: date input")
        return DATE_ERROR

    dateinp = dateinp[8:10] + "/" + dateinp[5:7] + "/" + dateinp[0:4]
    global url
    url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + dateinp
    html = get_html()
    currency = parse(html, currency, reversed_check)

    if currency == CURRENCY_ERROR:
        print("cant find currency")
        return CURRENCY_ERROR

    if not reversed_check:
        print(f"Курс рубля к {args[1]} на {dateinp}: {currency}")
        return EXIT_SUCCESS

    print(f"Курс {args[1]} к рублю на {dateinp}: {currency}")
    return EXIT_SUCCESS


EXIT_SUCCESS = 0
CURRENCY_ERROR = 1
DATE_ERROR = 2
EXIT_REFERENCE = 3
INPUT_ERROR = 4

if __name__ == '__main__':
    main(sys.argv, download)
