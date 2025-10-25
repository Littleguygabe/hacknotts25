import yfinance as yf
import pandas as pd


def getTickerAttributes(ticker,time_period):
    try:
        data_dict_arr = getRawData(ticker,time_period)
        # need to eventually implement the market sentiment analysis into the return dictionary

        ticker_dict = {
            'ticker':ticker,
            'ticker_history':data_dict_arr
        }

        return ticker_dict

    except:
        return {'err_msg':f"'{ticker}' ticker Does not exist OR has no retrievable data"}

def getRawData(ticker,time_period):
    tick = yf.Ticker(ticker)

    #establish the interval based on the time_period

    match time_period:
        case time_period if time_period<=7:
            time_interval = '1m'

        case time_period if time_period<=60:
            time_interval = '15m'

        case _:
            time_interval = '1d'

    print(time_interval)

    data_1m_int = tick.history(period='7d',interval=time_interval) 
    data_1m_int.reset_index(inplace=True)

    data_1m_int['Datetime'] = data_1m_int['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    data_1m_int = data_1m_int[['Datetime','Close']]

    data_dict_arr = data_1m_int.to_dict(orient='records')


    return data_dict_arr


if __name__ == '__main__':
    output = getRawData('AAPL')  
    print(output)


