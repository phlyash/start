import currency
import unittest
from datetime import datetime


class CurrencyTest(unittest.TestCase):

    def test_date_check(self):
        result = currency.date_check(str(datetime.today().date()))
        self.assertEqual(result, True)

    def test_less_date_check(self):
        result = currency.date_check("1992-06-20")
        self.assertEqual(result, False)

    def test_higher_date_check(self):
        date = str(datetime.today().year) + '-' + str(datetime.today().month) + '-' + str(datetime.today().day + 1)
        result = currency.date_check(date)
        self.assertEqual(result, False)

    def test_13month(self):
        result = currency.date_check("2019-13-10")
        self.assertEqual(result, False)

    def test_parse(self):
        html = open("F:/project/start/xml.txt")
        result = currency.parse(html.read(), "usd", False)
        html.close()
        self.assertEqual(result, "30.9436")

    def test_parse_parse_reversed(self):
        html = open("F:/project/start/xml.txt")
        result = currency.parse(html.read(), "usd", True)
        html.close()
        self.assertEqual(result, "0.0323")

    def test_parse_false_valute_code(self):
        html = open("F:/project/start/xml.txt")
        result = currency.parse(html.read(), "zxc", False)
        html.close()
        self.assertEqual(result, "cant find currency")

    def test_main_true(self):
        args = ["path", "eur", "2020-01-01"]
        result = currency.main(args)
        self.assertEqual(result, 0)

    def test_main_reversed_true(self):
        args = ["path", "eur", "2020-01-01"]
        result = currency.main(args)
        self.assertEqual(result, 0)

    def test_noargs(self):
        args = ["path"]
        result = currency.main(args)
        self.assertEqual(result, 3)

    def test_help(self):
        args = ["path", "-h"]
        result = currency.main(args)
        self.assertEqual(result, 3)

    def test_usage_help(self):
        args = ["path", "-u"]
        result = currency.main(args)
        self.assertEqual(result, 3)

    def test_exit_codes_help(self):
        args = ["path", "-e"]
        result = currency.main(args)
        self.assertEqual(result, 3)

    def test_main_date_error(self):
        args = ["path", "eur", "2019-13-10"]
        result = currency.main(args)
        self.assertEqual(result, 2)

    def test_main_currency_error(self):
        args = ["path", "zxc", "2020-01-01"]
        result = currency.main(args)
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
