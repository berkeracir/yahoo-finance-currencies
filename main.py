import numpy as np

from config import OUTPUT_FOLDER_NAME, NUMBER_OF_CURRENCIES
from utils import get_currencies, create_excel_file, download_historical_data


if __name__ == "__main__":
    currencies = get_currencies()   # get currency information
    create_excel_file(currencies)   # create an excel file with currencies

    N = NUMBER_OF_CURRENCIES
    headings = currencies.keys()

    for index in np.argsort(currencies[headings[-1]])[::-1][:N]: # sort '% Change' values and obtain indices of the highest ones
        symbol = currencies[headings[0]][index]
        download_historical_data(symbol, OUTPUT_FOLDER_NAME)    # download historical data of currency with given symbol