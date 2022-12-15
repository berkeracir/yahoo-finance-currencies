import requests
from bs4 import BeautifulSoup


def getHeadingsAndCurrencies():
    URL = "https://finance.yahoo.com/currencies"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('div', id="Lead-4-YFinListTable-Proxy")
    table_rows = table.find_all('tr', class_="simpTblRow")
    
    headings = ["Symbol", "Name", "Last Price", "Change", "% Change"]
    currencies = {'Symbol': [], 'Name': [], 'Last Price': [], 'Change': [], '% Change': []}

    for table_row in table_rows:
        currencies['Symbol'].append(table_row.find('td', {'aria-label': "Symbol"}).getText().replace("=X", ""))
        currencies['Name'].append(table_row.find('td', {'aria-label': "Name"}).getText())
        currencies['Last Price'].append(float(table_row.find('td', {'aria-label': "Last Price"}).getText().replace(",", "")))
        currencies['Change'].append(float(table_row.find('td', {'aria-label': "Change"}).getText().replace("+", "").replace(",", "")))
        currencies['% Change'].append(float(table_row.find('td', {'aria-label': "% Change"}).getText().replace("%", "").replace("+", "")))

    return headings, currencies