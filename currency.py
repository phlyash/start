from datetime import datetime
import urllib.request
import sys


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
    if currency in html:
        if reversed_check:
            return '%.4f' % (1 / float(html[html.find('Value', html.find(currency)) + 6:html.find(',', html.find(currency)) + 5].replace(',', '.')))
        else:
            return html[html.find('Value', html.find(currency)) + 6:html.find(',', html.find(currency)) + 5].replace(',', '.')
    else:
        return "cant find currency"


def main(args):
    EXIT_SUCCESS = 0
    CURRENCY_ERROR = 1
    DATE_ERROR = 2
    EXIT_REFERENCE = 3
    reversed_check = False

    if len(args) == 1 or args[1] in ("-a", "-h"):
        print(
            "usage: currency.py [valute code] [date: <format{yyyy-mm-dd}>]", "\n",
            "usage example: eur 2020-01-01", "\n",
            "this script has data from 1992-07-01", "\n",
            "in default program show direct quotations", "-n"
            "other arguments: [-h] [-a] [-e] [--exit-codes] [-r] [--reverse-quotation] [-u] [--usage]", sep=""
              )
        print("help shown successful")
        return EXIT_REFERENCE
    elif args[1] in ("--exit-codes", "-e"):
        print(
            "exit code 0: success", "\n",
            "exit code 1: currency-code format error", "\n",
            "exit code 2: date error(not in data base or date in future)", "\n",
            "exit code 3: references", sep=""
        )
        print("help shown successful")
        return EXIT_REFERENCE
    elif args[1] in ("--usage", "-u"):
        print(
            "arguments help:", "\n",
            "-h || -a : show basics for using program", "\n",
            "-e || --exit-codes : show all exit codes with decoding it", "\n",
            "-r || --reverse-quotation : show reverse quotations for currency you asked", sep=""
        )
        print("help shown successful")
        return EXIT_REFERENCE

    reversed_check = len(args) > 2 and args[len(args)-1] in ("-r", "--reverse-quotation")
    currency = args[1]
    dateinp = args[2]

    if date_check(dateinp):
        dateinp = dateinp[8:10] + "/" + dateinp[5:7] + "/" + dateinp[0:4]
        url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + dateinp
        html = str(urllib.request.urlopen(url).read())
        currency = parse(html, currency, reversed_check)
        if "cant" in currency:
            print(currency)
            return CURRENCY_ERROR
        elif reversed_check:
            print(f"Курс {args[1]} к рублю на {dateinp}: {currency}")
            return EXIT_SUCCESS
        else:
            print(f"Курс рубля к {args[1]} на {dateinp}: {currency}")
            return EXIT_SUCCESS
    else:
        print("error: date input")
        return DATE_ERROR


if __name__ == '__main__':
    main(sys.argv)
