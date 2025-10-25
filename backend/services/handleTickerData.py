import yfinance as yf
import pandas as pd


def getTickerAttributes(ticker):
    data_dict_arr = getRawData(ticker)
    # need to eventually implement the market sentiment analysis into the return dictionary

    ticker_dict = {
        'ticker':ticker,
        'ticker_history':data_dict_arr
    }

    return ticker_dict

def getRawData(ticker):
    tick = yf.Ticker(ticker)
    data_1m_int = tick.history(period='7d',interval='1m') 
    data_1m_int.reset_index(inplace=True)

    data_1m_int['Datetime'] = data_1m_int['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    data_1m_int = data_1m_int[['Datetime','Close']]

    data_dict_arr = data_1m_int.to_dict(orient='records')


    return data_dict_arr


if __name__ == '__main__':
    output = getRawData('AAPL')  
    print(output)


