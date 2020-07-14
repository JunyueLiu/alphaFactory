import pickle
import os
import pandas as pd


def load_result_from_pickles(source_path):
    pickle_files = [f for f in os.listdir(source_path) if f.endswith('.pickle')]
    portfolio = {}
    # portfolio
    # {
    #   'strategy_1':{
    #   'net_value': pd.Series,
    #   'position': pd.DataFrame
    #
    # }
    for file in pickle_files:
        with open(os.path.join(source_path, file), 'rb') as f:
            backtesting_result = pickle.load(f)
            portfolio[file.replace('.pickle', '')] = {
                'net_value': backtesting_result['net_value'],
                'position': backtesting_result['holding'],

            }
    return portfolio


def normalized_net_value(portfolio: dict):
    for k in portfolio.keys():
        net_value = portfolio[k]['net_value']
        portfolio[k]['net_value'] = net_value / net_value[0]
    return portfolio


def to_net_value_df(portfolio: dict):
    net_values = {}
    for k in portfolio.keys():
        net_values[k] = portfolio[k]['net_value']
    return pd.DataFrame(net_values)


def to_position_df(portfolio: dict):
    position = {}
    for k in portfolio.keys():
        position[k] = portfolio[k]['position']
    return pd.DataFrame(position)

if __name__ == '__main__':
    portfolio = load_result_from_pickles('sample_data')
    portfolio = normalized_net_value(portfolio)
    net_values = to_net_value_df(portfolio)
    position = to_position_df(portfolio)
