import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import numpy as np
import datetime as dt
from scipy.optimize import minimize
#import time


DATA_PROVIDER = 'quandl' # 'morningstar'
BENCHMARK = 'GOOG' # TODO: 'SPY' is not working in the quandl API
unknown_tickers = []


def optimize_and_normalize(start_date, end_date, tickers, alloc):   
    unknown_tickers = []
    normalized, normalized_bench, opt_alloc = optimize_portfolio(start_date, end_date, tickers)
    return normalized.dot(alloc), \
        normalized.dot(opt_alloc), \
        normalized_bench, \
        opt_alloc, \
        unknown_tickers


def optimize_portfolio(start_date, end_date, tickers):
    normalized, normalized_bench = normalize(start_date, end_date, tickers)
    
    x0 = [1./len(tickers) for i in range(len(tickers))]
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = [(0, 1) for i in range(len(tickers))]
    opt_alloc = minimize(neg_sharpe_ratio, x0, args = (normalized), 
                        method='SLSQP', 
                        bounds=bounds, constraints=constraints, 
                        options={'disp': False}).x
    return normalized, normalized_bench, opt_alloc


def normalize(start_date, end_date, tickers):    
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(tickers, dates)  
    #prices_all.fillna(method='ffill', inplace=True)
    #prices_all.fillna(method='bfill', inplace=True)
      
    prices = prices_all[tickers]  

    normalized = prices / prices.iloc[0]    
    if BENCHMARK in prices_all:
        normalized_bench = prices_all[BENCHMARK] / prices_all[BENCHMARK].iloc[0]
    else:
        normalized_bench = pd.Series()
    
    return normalized, normalized_bench
    

def get_data(tickers, dates, colname = 'AdjClose'):    
    all_data = pd.DataFrame(index=dates)
    tickers_copy = [s for s in tickers]
    if BENCHMARK not in tickers:
        tickers_copy.insert(0, BENCHMARK)

    for ticker in tickers_copy:      
        try:  
            current_data = web.DataReader(ticker, DATA_PROVIDER, dates[0], dates[-1])[[colname]]
        except:
            print('Ticker not found:', ticker)
            unknown_tickers.append(ticker)
            continue
        current_data = current_data.rename(columns={colname: ticker})

        all_data = all_data.join(current_data)        
        if ticker == BENCHMARK:  
            all_data = all_data.dropna(subset=[BENCHMARK])

        #time.sleep(1)
    return all_data


def check_ticker(ticker):
    try:  
        _ = web.DataReader(ticker, DATA_PROVIDER, '2018-01-15', '2018-01-16')
    except:
        return False
    return True


def neg_sharpe_ratio(allocs, normalized, interest_rate=0.0, n_days=252.0):    
    normalized_pot = normalized.dot(allocs)
    daily_ret = (normalized_pot/normalized_pot.shift() - 1).drop(normalized_pot.index[0])
        
    return_mean = daily_ret.mean()
    return_std = daily_ret.std() 
    return -1 * (return_mean - interest_rate)/return_std * np.sqrt(n_days)


def main():
    start = '2017-01-01'
    end = '2017-12-31'   
    tickers = ['GOOG', 'AAPL', 'AMZN']         
    normalized, normalized_bench, opt_alloc = optimize_portfolio(start, end, tickers)    
    print(normalized)
    print(normalized_bench)
    print(opt_alloc)

    
if __name__ == "__main__":
    main()
