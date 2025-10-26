import json
import yfinance as yf
import numpy as np
from arch import arch_model
import multiprocessing
import pandas as pd
from functools import partial


from services.sentimentAnalysis import getSentimentAnalysis

def getHistoricalTickerData(ticker):
    ticker_obj = yf.Ticker(ticker)
    ticker_data = ticker_obj.history(period='2y',interval='1d')
    log_returns = np.log(ticker_data['Close']/ticker_data['Close'].shift(1)).dropna()
    return ticker_data,log_returns


def fitGarchModel(log_returns):
    garch_returns = log_returns*100
    model = arch_model(garch_returns,vol='GARCH',q=1,p=1,dist='t')
    results = model.fit(disp='off')

    params = results.params
    garch_params = {
        'omega':params['omega'],
        'alpha[1]':params['alpha[1]'],
        'beta[1]':params['beta[1]'],
    }

    last_sigma_sq = results.conditional_volatility.iloc[-1]**2
    last_return_scaled = garch_returns.iloc[-1]

    return garch_params, last_sigma_sq, last_return_scaled

def initialiseParams(ticker):
    try:
        sentiment_data = getSentimentAnalysis(ticker)
        ticker_data,log_returns = getHistoricalTickerData(ticker)
        garch_params, last_sigma_sq, last_return_scaled = fitGarchModel(log_returns)

        start_price = ticker_data['Close'].iloc[-1]
        mu_hist = log_returns.mean()

        target_price = sentiment_data.get('analyst_targetMeanPrice')
        mu_analyst = (np.log(target_price/start_price)/252)*100

        social_score = sentiment_data.get('social_score')
        multiplier_social = 1.0 + ((social_score-50)/100)
        mu_social = (mu_hist*multiplier_social)*100

        combined_score = sentiment_data.get('combined_score')
        multiplier_combined = 1.0+((combined_score-50)/100)    
        mu_combined = (mu_hist*multiplier_combined)*100

        last_date = ticker_data.index[-1]
        all_params = {
            "start_price": start_price,
            "garch_params": garch_params,
            "last_sigma_sq": last_sigma_sq,
            "last_return_scaled": last_return_scaled,
            "mu_analyst": mu_analyst,
            "mu_social": mu_social,
            "mu_combined": mu_combined,
            "last_date": last_date
        }

        return all_params

    except Exception as e:
        print(f'ERROR > Could not set up parameters for GARCH > {e}')
        return None


def runSingleSimPath(forecast_horizon, mu, garch_params, last_price, last_sigma_sq,last_return_scaled):
    omega = garch_params['omega']
    alpha = garch_params['alpha[1]']
    beta = garch_params['beta[1]']

    price_path = []
    for t in range(forecast_horizon):
        sigma_t_sq = omega + (alpha*(last_return_scaled**2))+(beta*last_sigma_sq)
        if sigma_t_sq<0:
            sigma_t_sq = last_sigma_sq

        sigma_t = np.sqrt(sigma_t_sq)

        Z = np.random.normal(0,1) #random shock value

        return_scaled = mu+(sigma_t*Z)
        final_return = return_scaled/100
        new_price = last_price*np.exp(final_return)
        price_path.append(new_price)

        last_price=new_price
        last_return_scaled = return_scaled
        last_sigma_sq = sigma_t_sq

    return price_path

def _run_single_simulation_for_worker(task, forecast_horizon, init_params):
    """
    Helper function for multiprocessing pool. Runs a single simulation path.
    """
    mu_name, mu_value = task
    path = runSingleSimPath(
        forecast_horizon=forecast_horizon,
        mu=mu_value,
        garch_params=init_params["garch_params"],
        last_price=init_params["start_price"],
        last_sigma_sq=init_params["last_sigma_sq"],
        last_return_scaled=init_params["last_return_scaled"]
    )
    return (mu_name, path)

def forecastPrices(ticker, forecast_horizon):
    n_sims = 1000

    init_params = initialiseParams(ticker)
    if not init_params:
        return {"error": "Failed to initialize parameters for simulation."}

    last_date = init_params["last_date"]
    future_dates = pd.to_datetime(pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_horizon))

    mus = {
        "analyst": init_params["mu_analyst"],
        "social": init_params["mu_social"],
        "combined": init_params["mu_combined"]
    }

    tasks = []
    for mu_name, mu_value in mus.items():
        for _ in range(n_sims):
            tasks.append((mu_name, mu_value))

    p_worker = partial(_run_single_simulation_for_worker, 
                       forecast_horizon=forecast_horizon, 
                       init_params=init_params)

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(p_worker, tasks)

    grouped_results = {}
    for mu_name, path in results:
        if mu_name not in grouped_results:
            grouped_results[mu_name] = []
        grouped_results[mu_name].append(path)

    final_results = {}
    for mu_name, paths in grouped_results.items():
        paths_df = pd.DataFrame(paths).T
        mean_path = paths_df.mean(axis=1)
        
        forecast_data = []
        for i in range(len(mean_path)):
            forecast_data.append({
                "Datetime": future_dates[i].strftime('%Y-%m-%d %H:%M:%S'),
                "Close": mean_path.iloc[i]
            })
        
        final_results[mu_name] = forecast_data
        
    return final_results