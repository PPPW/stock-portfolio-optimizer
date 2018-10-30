from flask import Blueprint, send_from_directory, jsonify, request
from datetime import datetime
import os
import pickle

import numpy as np

from .optimization import optimize_and_normalize, check_ticker


mod = Blueprint('api', __name__)

@mod.route('/', defaults={'path': ''})
@mod.route('/<path:path>')
def any_root_path(path):    
    static_folder = 'static/vue-app/dist'
    if path == '':
        # for '/'        
        return send_from_directory(static_folder, 'index.html')
    if os.path.exists(os.path.join('app', static_folder, path)):
        # for existing static files        
        return send_from_directory(static_folder, path)
    else:
        # for nonexisting urls  
        print(path) 
        return send_from_directory(static_folder, 'index.html')

# mock data for API testing
@mod.route('/api/test')
def get_data():
    start_date = request.args['startDate']
    end_date = request.args['endDate']    
    tickers_raw = request.args.getlist('tickers[]')    
    allocs_raw = request.args.getlist('allocations[]')
    data = {
        'date_range': ['2018-01-02', '2018-01-03', '2018-01-04', '2018-01-05'],
        'performance': list(map(lambda x: '%.2f' % x, np.random.rand(4)*15)),
        'opt_performance': [13.5, 14.5, 15.6, 16.8],
        'opt_allocations': list(map(lambda x: '%.2f' % x, np.random.rand(3)*0.5)),
        'benchmark': [10.1, 12.1, 14.3, 14.9],
        'startDate': start_date,
        'endDate': end_date,
        'tickers': tickers_raw,
        'allocations': allocs_raw
    }
    return jsonify(data)


@mod.route('/api/opt')
def optimize():        
    start_date = request.args['startDate']
    end_date = request.args['endDate']    
    tickers_raw = request.args.getlist('tickers[]')    
    allocs_raw = request.args.getlist('allocations[]')
    
    tickers = []
    allocs = []
    for i, ticker in enumerate(tickers_raw):        
        # TODO: check ticker exist
        if ticker != '':
            tickers.append(ticker)
            allocs.append(float(allocs_raw[i]))  
    allocs = np.array(allocs)
    allocs = allocs / allocs.sum()

    # TODO: handle all empty; wrong date format; etc.
    
    performance, opt_performance, benchmark, opt_allocations, unknown_tickers = optimize_and_normalize(
        start_date, 
        end_date,
        tickers, 
        allocs)
        
    ret = {
        'date_range': performance.index.strftime('%Y-%m-%d').tolist(),
        'performance': performance.tolist(),
        'opt_performance': opt_performance.tolist(),
        'opt_allocations': np.round(opt_allocations, 2).tolist(),
        'benchmark': benchmark.tolist(),
        'unknown_tickers': unknown_tickers
    }
    return jsonify(ret)


@mod.route('/api/ticker')
def ticker_exist():        
    return jsonify({ 'exist': check_ticker(request.args['ticker']) })


@mod.route('/api/autocomplete')
def autocomplete():
    # TODO: global, efficiency
    filter = request.args['filter[filters][0][value]']
    static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'static')    
    sp500 = pickle.load(open(os.path.join(static_file_dir, 'sp500.pkl'), 'rb'))
    matched = sp500.Ticker[sp500.All.str.contains(filter, case=False)]
    return jsonify(matched.tolist())
