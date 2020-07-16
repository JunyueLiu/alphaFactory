import pickle
import os
import numpy as np
import pandas as pd
import scipy.optimize as sco


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


def calculate_portfolio_ret_std(weights, ret, cov):
    portfolio_ret = np.sum(weights * ret)
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov, weights)))
    return portfolio_ret, portfolio_std


def _neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    p_ret, p_var = calculate_portfolio_ret_std(weights, mean_returns, cov_matrix)
    return -(p_ret - risk_free_rate) / p_var


def _portfolio_volatility(weights, mean_returns, cov_matrix):
    return calculate_portfolio_ret_std(weights, mean_returns, cov_matrix)[1]


def calculate_max_sharp_weights(expected_ret, cov, risk_free_rate=0):
    num_assets = len(expected_ret)
    args = (expected_ret, cov, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    opts = sco.minimize(_neg_sharpe_ratio, num_assets * [1. / num_assets, ], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)
    weights = pd.DataFrame(opts.x, index=expected_ret.index, columns=['allocation'])

    return weights


def calculate_min_variance_weights(expected_ret, cov_matrix):
    num_assets = len(expected_ret)
    args = (expected_ret, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0, 1.0)
    bounds = tuple(bound for asset in range(num_assets))

    result = sco.minimize(_portfolio_volatility, num_assets * [1. / num_assets, ], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
    weights = pd.DataFrame(result.x, index=expected_ret.index, columns=['allocation'])
    return weights


def efficient_return(mean_returns, cov_matrix, target):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)

    def portfolio_return(weights):
        return calculate_portfolio_ret_std(weights, mean_returns, cov_matrix)[0]

    constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    result = sco.minimize(_portfolio_volatility, num_assets * [1. / num_assets, ], args=args, method='SLSQP',
                          bounds=bounds, constraints=constraints)
    return result


def efficient_frontier(mean_returns, cov_matrix, returns_range):
    efficients = []
    for ret in returns_range:
        efficients.append(efficient_return(mean_returns, cov_matrix, ret))
    return efficients


if __name__ == '__main__':
    portfolio = load_result_from_pickles('sample_data')
    portfolio = normalized_net_value(portfolio)
    net_values = to_net_value_df(portfolio)
    # position = to_position_df(portfolio)
    daily_net = net_values.groupby(pd.Grouper(freq='D')).last().fillna(method='ffill')  # type: pd.DataFrame
    daily_ret = daily_net.pct_change()
    annualized_ret_mean = 252 * daily_ret.mean()
    annualized_ret_std = np.sqrt(252) * daily_ret.std()
    annualized_ret_cov = 252 * daily_ret.cov()
    random_weight = np.random.randn(len(annualized_ret_mean))
    result = calculate_max_sharp_weights(annualized_ret_mean, annualized_ret_cov)
    # weights = result['x']
