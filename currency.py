import urllib.request
inp = input().split() # пусть ввод правильный
currency = inp[0]
date = inp[1] #y-m-d
lst = date.split("-") #d/m/y
lst[0], lst[2] = lst[2], lst[0] #swap day and year for cbr format
date = "/".join(lst) #date for cbr
url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req=" + date
html = str(urllib.request.urlopen (url).read())
if currency.upper() in html:
    print(f"Курс рубля к {currency} на {date}: {html[html.find(currency.upper())+70:html.find(currency.upper())+77]}")
else:
    print("error:currency not found")