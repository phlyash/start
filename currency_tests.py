import currency
import unittest
from datetime import datetime
import os


XML_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "xml.txt"
)


def download(date):
    with open(XML_PATH) as f:
        file = f.read()
    return file


class CurrencyTest(unittest.TestCase):

    def test_date_check(self):
        result = currency.date_check(str(datetime.today().date()))
        self.assertEqual(result, True)

    def test_less_date_check(self):
        result = currency.date_check("1992-06-30")
        self.assertEqual(result, False)

    def test_higher_date_check(self):
        date = datetime.today()
        date = date.replace(day=date.day+1)
        date = date.strftime("%Y-%m-%d")
        result = currency.date_check(date)
        self.assertEqual(result, False)

    def test_13month(self):
        result = currency.date_check("2019-13-10")
        self.assertEqual(result, False)

    def test_parse(self):
        with open(XML_PATH) as f:
            html = f.read()
        result = currency.parse(html, "usd", False)
        self.assertEqual(result, "30.9436")

    def test_parse_parse_reversed(self):
        with open(XML_PATH) as f:
            html = f.read()
        result = currency.parse(html, "usd", True)
        self.assertEqual(result, "0.0323")

    def test_parse_false_valute_code(self):
        with open(XML_PATH) as f:
            html = f.read()
        with self.assertRaises(ValueError) as e:
            currency.parse(html, "zxc", False)
        exception = str(e.exception)
        self.assertEqual(exception, "Currency not found")

    def test_main_true(self):
        args = ["path", "usd", "2002-03-02"]
        result = currency.main(args, download)
        self.assertEqual(result, currency.EXIT_SUCCESS)

    def test_main_reversed_true(self):
        args = ["path", "usd", "2002-03-02"]
        result = currency.main(args, download)
        self.assertEqual(result, currency.EXIT_SUCCESS)

    def test_noargs(self):
        args = ["path"]
        result = currency.main(args, download)
        self.assertEqual(result, currency.EXIT_REFERENCE)

    def test_help(self):
        args = ["path", "-h"]
        result = currency.main(args, download)
        self.assertEqual(result, currency.EXIT_REFERENCE)

    def test_exit_codes_help(self):
        args = ["path", "-e"]
        result = currency.main(args, download)
        self.assertEqual(result, currency.EXIT_REFERENCE)

    def test_main_date_error(self):
        args = ["path", "eur", "2019-13-10"]
        result = currency.main(args, download)
        self.assertEqual(result, currency.DATE_ERROR)

    def test_main_currency_error(self):
        args = ["path", "zxc", "2020-01-01"]
        result = currency.main(args, download)
        self.assertEqual(result, currency.CURRENCY_ERROR)

    def test_main_1_argument(self):
        args = ["path", "eur"]
        result = currency.main(args, download)
        self.assertEqual(result, currency.INPUT_ERROR)


if __name__ == "__main__":
    unittest.main()
