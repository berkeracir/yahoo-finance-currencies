from bs4 import BeautifulSoup
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import os
import requests
import wget
import xlsxwriter

from config import OUTPUT_FOLDER_NAME, EXCEL_FILE_NAME, SHEET_NAME_DATE_FORMAT


YAHOO_FINANCE_CURRENCIES_URL = "https://finance.yahoo.com/currencies"
YAHOO_FINANCE_QUERY_URL = "https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start_timestamp}&period2={end_timestamp}&interval=1d&events=history&includeAdjustedClose=true"


def get_currencies() -> dict():
    '''
    Scrapes currency information from Yahoo Finance Currencies and returns currency information in 
    dictionary ('Symbol': str, 'Name': str, 'Last Price': float, 'Change': float, '% Change': float)
    '''

    page = requests.get(YAHOO_FINANCE_CURRENCIES_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('div', id="Lead-4-YFinListTable-Proxy")
    table_rows = table.find_all('tr', class_="simpTblRow")
    
    currencies = {'Symbol': [], 'Name': [], 'Last Price': [], 'Change': [], '% Change': []}

    for table_row in table_rows:
        currencies['Symbol'].append(table_row.find('td', {'aria-label': "Symbol"}).getText().replace("=X", ""))
        currencies['Name'].append(table_row.find('td', {'aria-label': "Name"}).getText())
        currencies['Last Price'].append(float(table_row.find('td', {'aria-label': "Last Price"}).getText().replace(",", "")))
        currencies['Change'].append(float(table_row.find('td', {'aria-label': "Change"}).getText().replace("+", "").replace(",", "")))
        currencies['% Change'].append(float(table_row.find('td', {'aria-label': "% Change"}).getText().replace("%", "").replace("+", "")))

    return currencies


def create_excel_file(currencies: dict) -> None:
    '''Creates an Excel file with scraped currency information from Yahoo Finance Currencies'''

    headings = list(currencies.keys())

    output_folder = OUTPUT_FOLDER_NAME
    excel_filename = EXCEL_FILE_NAME
    sheet_name = date.today().strftime(SHEET_NAME_DATE_FORMAT)

    # create a new directory if not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    wb = xlsxwriter.Workbook(os.path.join(output_folder, excel_filename))   # Excel Workbook
    ws = wb.add_worksheet(sheet_name)   # Excel Worksheet
    ws.set_column(0, len(headings), 10) # adjust column widths

    f1 = wb.add_format({'bold': True, 'border': 0}) # bold header without any border

    ws.write_row(0, 0, headings, f1)    # write the header
    for col in range(len(headings)):
        ws.write_column(1, col, currencies[headings[col]])    # write the column values of each heading

    ws.conditional_format(1, len(headings)-1, len(currencies[headings[-1]]), len(headings)-1, {'type': '3_color_scale'})    # apply color scaling for '% Change' column

    wb.close()


def download_historical_data(currency_symbol: str, output_folder: str="") -> None:
    '''Downloads given currency's histroical data from Yahoo Finance's API into given output folder'''

    symbol = currency_symbol + "=X"
    now = datetime.now()
    one_month_ago = now - relativedelta(months=1)
    formatted_url = YAHOO_FINANCE_QUERY_URL.format(symbol=symbol, start_timestamp=int(one_month_ago.timestamp()), end_timestamp=int(now.timestamp()))

    file_path = os.path.join(output_folder, symbol + ".csv")

    if os.path.exists(file_path):
        os.remove(file_path)    # if the file exists, remove it directly

    wget.download(formatted_url, file_path)