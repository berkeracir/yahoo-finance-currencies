import os
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import xlsxwriter
import wget
import numpy as np

from scraper import getHeadingsAndCurrencies


def downloadHistoricalData(currency_symbol, output_folder=""):
    URL = "https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start_timestamp}&period2={end_timestamp}&interval=1d&events=history&includeAdjustedClose=true"

    symbol = currency_symbol + "=X"
    now = datetime.now()
    one_month_ago = now - relativedelta(months=1)
    formatted_url = URL.format(symbol=symbol, start_timestamp=int(one_month_ago.timestamp()), end_timestamp=int(now.timestamp()))

    file_path = os.path.join(output_folder, symbol + ".csv")

    if os.path.exists(file_path):
        os.remove(file_path)    # if the file exists, remove it directly

    wget.download(formatted_url, file_path)

    

if __name__ == "__main__":
    # get currency information
    headings, currencies = getHeadingsAndCurrencies()

    output_folder = "Currencies"
    excel_filename = "Currencies.xlsx"
    sheet_name = date.today().strftime("%m-%d-%Y")

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

    N = 5   # the number of currencies whose historical data will be downloaded
    for index in np.argsort(currencies[headings[-1]])[::-1][:N]: # sort '% Change' values and obtain indices of the highest ones
        symbol = currencies[headings[0]][index]
        downloadHistoricalData(symbol, output_folder)