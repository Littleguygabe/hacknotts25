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

    except Exception as e:
        print(f'Exception Message > {e}')
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


    data_df = tick.history(period=f'{time_period}d',interval=time_interval) 
    
    data_df.reset_index(inplace=True)
    date_col_name = 'Datetime' if 'Datetime' in data_df.columns else 'Date'
    data_df[date_col_name] = data_df[date_col_name].dt.strftime('%Y-%m-%d %H:%M:%S')

    data_df.rename(columns={date_col_name: 'Datetime'}, inplace=True)

    data_df = data_df[['Datetime','Close']]

    data_dict_arr = data_df.to_dict(orient='records')

    return data_dict_arr
    
if __name__ == '__main__':
    output = getRawData('AAPL', 100)
    print(output)


