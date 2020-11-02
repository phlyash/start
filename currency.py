from datetime import datetime
import urllib.request
import sys


EXIT_SUCCESS = 0
CURRENCY_ERROR = 1
DATE_ERROR = 2
EXIT_REFERENCE = 3
INPUT_ERROR = 4
TEXT_HELP_AND_USAGE = (
    "usage: currency.py [valute code] [date: <format{yyyy-mm-dd}>]\n"
    "usage example: eur 2020-01-01\n"
    "this script has data from 1992-07-01\n"
    "in default program show direct quotations\n"
    "other arguments: [-h] [-a] [-e] [--exit-codes] [-r] [--reverse-quotation]\n"
    "with [-r] argument you can see reversed quotations (1 rubble in [valute])"
)
TEXT_EXIT_CODES = (
    "exit code 0: success\n"
    "exit code 1: currency-code format error\n"
    "exit code 2: date error(not in data base or date in future)\n"
    "exit code 3: references"
)


def download(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    date = date.strftime("%d/%m/%Y")
    return str(urllib.request.urlopen("http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date).read())


def date_check(dateinp):
    try:
        dateinp = datetime.strptime(dateinp, "%Y-%m-%d")
        min_date = datetime(1992, 7, 1)
        max_date = datetime.today()

        return min_date <= dateinp <= max_date
    except ValueError:
        return False


def parse(html, currency, reversed_check):
    currency = currency.upper()
    if currency not in html:
        raise ValueError("Currency not found")

    currency_index = html.find(currency)
    value_index = html.find("Value", currency_index)

    if not reversed_check:
        return html[value_index + 6:html.find(',', currency_index) + 5].replace(',', '.')

    return '%.4f' % (1 / float(html[value_index + 6:html.find(',', currency_index) + 5].replace(',', '.')))


def main(args, get_html):
    if len(args) == 1 or args[1] in ("-a", "-h"):
        print(TEXT_HELP_AND_USAGE)
        return EXIT_REFERENCE
    elif args[1] in ("--exit-codes", "-e"):
        print(TEXT_EXIT_CODES)
        return EXIT_REFERENCE

    reversed_check = len(args) > 2 and args[len(args)-1] in ("-r", "--reverse-quotation")
    try:
        currency = args[1]
        dateinp = args[2]
    except IndexError:
        print("Not enough arguments")
        return INPUT_ERROR

    if not date_check(dateinp):
        print("error: date out of scope")
        return DATE_ERROR

    html = get_html(dateinp)

    try:
        currency = parse(html, currency, reversed_check)
    except ValueError as error:
        print(error)
        return CURRENCY_ERROR

    if currency == CURRENCY_ERROR:
        print("cant find currency")
        return CURRENCY_ERROR

    if not reversed_check:
        print(f"Курс рубля к {args[1]} на {dateinp}: {currency}")
        return EXIT_SUCCESS

    print(f"Курс {args[1]} к рублю на {dateinp}: {currency}")
    return EXIT_SUCCESS


if __name__ == '__main__':
    main(sys.argv, download)
