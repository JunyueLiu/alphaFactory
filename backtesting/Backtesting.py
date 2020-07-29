import json
import pickle
import datetime
import inspect
import pandas as pd
import numpy as np

from backtesting.dash_app.index_app import get_backtesting_report_dash_app
from db_wrapper.mongodb_utils import MongoConnection

from gateway.quote_base import QuoteBase
from gateway.brokerage_base import BrokerageBase
from backtesting.BacktestingQuote import BacktestingQuote
from backtesting.BacktestingBrokerage import BacktestingBrokerage
from backtesting.backtesting_metric import *
from strategy.StrategyBase import Strategy
from bar_manager.BarManager import BarManager


class BacktestingBase:
    def __init__(self, quote: BacktestingQuote, brokerage: BacktestingBrokerage, strategy: Strategy, strategy_parameter
                 , start=None, end=None, initial_capital=100, backtesting_setting=None):

        self.quote_ctx = quote
        self.brokerage_ctx = brokerage
        self.strategy = strategy
        self.strategy_parameter = strategy_parameter
        self.start = start
        self.end = end
        self.initial_capital = initial_capital
        self.risk_free_rate = 0
        self.backtesting_setting = backtesting_setting
        self.backtesting_result = {}

        self.data = None
        self.benchmark = None

        self.dealt_list = []

        if self.start is None:
            self.start = self.backtesting_setting.get('start', None)
        if self.end is None:
            self.end = self.backtesting_setting.get('end', None)

        brokerage.cash = backtesting_setting['initial_capital']

    def _check_data_valid(self):
        """
        Check whether the data provided for backtesting is enough for strategy subscription
        :return:
        """
        for symbol, subtype_data in self.data.items():
            if symbol not in self.strategy_parameter['subscribe'].keys():
                raise ValueError('The data for backtesting doesn\'t include {}', symbol)
            else:
                for s in self.strategy_parameter['subscribe'][symbol]:
                    if s not in subtype_data.keys():
                        raise ValueError('The data for backtesting doesn\'t include {}:{}', symbol, s)

    def _initial_strategy(self):
        """
        To initial strategy, call before run the backtesting
        :return:
        """
        self.strategy.load_setting(self.strategy_parameter)
        self.strategy.set_quote_context(self.quote_ctx)
        self.strategy.set_brokerage_context(self.brokerage_ctx)

    def _load_setting(self, setting: dict or str):
        """
        Load the setting from dictionary or JSON file.
        :param setting:
        :return:
        """
        if isinstance(setting, dict):
            self.backtesting_setting = setting
        elif isinstance(setting, str):
            with open(setting, 'rb') as f:
                df = f.read()
                f.close()
                self.backtesting_setting = json.loads(df)
        d = self.__dict__
        for key in d.keys():
            if key in self.backtesting_setting.keys():
                d[key] = self.backtesting_setting[key]

    def _load_data(self):
        """
        helper function to load the data
        :return:
        """
        self.data = dict()
        if self.backtesting_setting['data_source'] == 'csv':
            time_key = self.backtesting_setting['time_key']
            for symbol, bar_data in self.backtesting_setting['data'].items():
                self.data[symbol] = dict()
                for bar_type, path in bar_data.items():
                    self.data[symbol][bar_type] = self._load_data_from_csv(path, time_key)
            if 'benchmark' in self.backtesting_setting.keys():
                self.benchmark = self._load_data_from_csv(self.backtesting_setting['benchmark'], time_key)
                self.benchmark = self.benchmark['close']
        elif self.backtesting_setting['data_source'] == 'mongo':
            time_key = self.backtesting_setting['time_key']
            host = self.backtesting_setting['host']
            port = self.backtesting_setting['port']
            user = self.backtesting_setting['user']
            password = self.backtesting_setting['password']
            conn = MongoConnection(host, port, user, password)
            for symbol, bar_data in self.backtesting_setting['data'].items():
                self.data[symbol] = dict()
                for bar_type, dbs in bar_data.items():
                    self.data[symbol][bar_type] = self._load_data_from_db(conn, dbs['db'], dbs['collections'], time_key)
            if 'benchmark' in self.backtesting_setting.keys():
                self.benchmark = self._load_data_from_db(self.backtesting_setting['benchmark']['db'],
                                                         self.backtesting_setting['benchmark']['collections'], time_key)
                self.benchmark = self.benchmark['close']
        self.quote_ctx.set_history_data(self.data)

    def _reset_data(self):
        self.data = None

    def get_trading_history(self):
        return self.brokerage_ctx.history_order_list_query()

    def get_dealt_history(self):
        return self.brokerage_ctx.deal_order_list

    def _load_data_from_db(self, conn: MongoConnection, db: str, collection: str, time_key: str):
        """
        helper function to load data from database
        :param conn:
        :param db:
        :param collection:
        :param time_key:
        :return:
        """
        if self.start is not None and self.end is not None:
            bar = conn.read_mongo_df(db, collection, {time_key: {'$gt': self.start, '$lt': self.end}})
        elif self.start is not None and self.end is None:
            bar = conn.read_mongo_df(db, collection, {time_key: {'$gt': self.start}}, )
        elif self.start is not None and self.end is None:
            bar = conn.read_mongo_df(db, collection, {time_key: {'$lt': self.end}})
        bar[time_key] = pd.to_datetime(bar[time_key])
        bar.set_index(time_key, inplace=True)
        return bar

    def _load_data_from_csv(self, path, time_key):
        """
        helper function to load data from csv
        :param path:
        :param time_key:
        :return:
        """
        bar = pd.read_csv(path)
        bar[time_key] = pd.to_datetime(bar[time_key])
        bar.set_index(time_key, inplace=True)
        if self.start is not None:
            bar = bar[bar.index >= pd.to_datetime(self.start)]
        if self.end is not None:
            bar = bar[bar.index <= pd.to_datetime(self.end)]
        return bar

    def _set_benchmark(self, series: pd.Series):
        self.benchmark = series

    def calculate_result(self):
        """
        calculate the backtesting result
        :return:
        """
        # first make the all asset prices dataframe
        dfs = []
        for code, ktype_data in self.data.items():
            for ktype, data in ktype_data.items():
                d = data.reset_index()
                dfs.append(d)
        asset_price = pd.concat(dfs)
        asset_price.set_index([self.backtesting_setting['time_key'], 'code'], inplace=True)

        self.dealt_list = self.get_dealt_history()
        traded = pd.DataFrame([order.order_dict() for order in self.dealt_list])
        # make the dealt_qty with +- sign
        traded['dealt_qty'] = np.where(traded['order_direction'] == 'LONG', traded['dealt_qty'], -traded['dealt_qty'])
        # calculate cash inflow from dealt qty and dealt price
        # long will have cash outflow (negative inflow) and short will have cash inflow
        traded['cash_inflow'] = - traded['dealt_price'] * traded['dealt_qty']
        # todo commission deduction
        # aggregate the cash inflow and dealt among with same code and same datetime
        traded_grouped = traded.groupby(['code', 'update_time']).agg(
            {'cash_inflow': 'sum', 'dealt_qty': 'sum'})
        traded_grouped.index = traded_grouped.index.set_names(['code', self.backtesting_setting['time_key']])
        # transform into time series of cumulative cash inflow and cumulative asset holding
        traded_grouped = traded_grouped.groupby(level=[0]).cumsum()
        traded_grouped.rename(columns={'cash_inflow': 'cumulative_cash_inflow',
                                       'dealt_qty': 'holding'}, inplace=True)
        first_traded, last_traded = first_last_trade_time(traded, 'update_time')
        traded_pnl = get_traded_pnl(traded)

        joint = asset_price.join(traded_grouped)
        # need to use groupby fillna
        joint = joint.groupby(level=1).ffill()
        joint.fillna(value=0, inplace=True)
        joint['equity'] = joint['close'] * joint['holding'] + joint['cumulative_cash_inflow']
        # aggregate different assets class returns with same timestamp.
        net_value = joint['equity'].groupby(level=0).sum() + self.initial_capital  # type:pd.Series
        # todo calculate every the metric from the net value index
        returns = net_value.pct_change()
        drawdown_metric, drawdown_percent = drawdown(net_value)

        self.backtesting_result['strategy_profile'] = {
            'name': self.strategy.strategy_name,
            'author': self.strategy.author,
            'version': self.strategy.strategy_version,
            'description': self.strategy.strategy_description,
            'parameter': self.strategy.strategy_parameters

        }
        self.backtesting_result['backtesting_setting'] = self.backtesting_setting
        self.backtesting_result['risk free rate'] = self.risk_free_rate
        self.backtesting_result['first_traded'] = first_traded
        self.backtesting_result['last_traded'] = last_traded
        self.backtesting_result['trade_list'] = traded
        self.backtesting_result['holding'] = joint['holding']
        self.backtesting_result['num_trade'] = num_trade(traded)
        self.backtesting_result['time_in_market'] = exposure(returns)
        self.backtesting_result['win_rate'] = win_rate(traded_pnl)
        self.backtesting_result['avg_win'] = avg_win(traded_pnl)
        self.backtesting_result['avg_loss'] = avg_loss(traded_pnl)
        self.backtesting_result['payoff_ratio'] = payoff_ratio(traded_pnl)
        self.backtesting_result['cagr'] = cagr(net_value / self.initial_capital)
        self.backtesting_result['cumulative_return'] = (net_value[-1] - net_value[0]) / net_value[0]
        self.backtesting_result['sharpe'] = sharpe_ratio(returns,
                                                         self.risk_free_rate)
        self.backtesting_result['sortino'] = sortino(returns)
        self.backtesting_result['volatility'] = returns_volatility(returns)
        self.backtesting_result['skew'] = returns_skew(returns)
        self.backtesting_result['Kurtosis'] = returns_kurt(returns)

        # data here is pandas Series, save for future use
        self.backtesting_result['data'] = self.data
        self.backtesting_result['benchmark'] = self.benchmark
        self.backtesting_result['net_value'] = net_value
        self.backtesting_result['rate of return'] = returns
        self.backtesting_result['drawdown_value'] = drawdown_metric
        self.backtesting_result['drawdown_percent'] = drawdown_percent
        self.backtesting_result['drawdown_detail'] = drawdown_details(drawdown_percent)

        self.backtesting_result['kelly'] = kelly(traded_pnl)
        self.backtesting_result['value_at_risk'] = value_at_risk(returns)


    def get_dash_report(self, dash_app=None):
        """
        from self.backtesting_result data generate report
        :param dash_app:
        :return:
        """
        return get_backtesting_report_dash_app(self.backtesting_result, dash_app)

    @staticmethod
    def get_dash_report_from_backtesting_result(backtesting_result: dict, dash_app=None):
        """

        :param backtesting_result:
        :param dash_app:
        :return:
        """
        return get_backtesting_report_dash_app(backtesting_result, dash_app)

    def backtesting_result_save_pickle(self, file: str):
        """

        :param file:
        :return:
        """
        with open(file, 'wb') as f:
            pickle.dump(self.backtesting_result, f, protocol=pickle.HIGHEST_PROTOCOL)
            print('Save to {} success.'.format(file))

    def bakctesting_result_to_json(self):
        """

        :return:
        """
        return json.dumps(self.backtesting_result)

    def save_backtesting_result_to_db(self, conn: MongoConnection, db: str, collections: str, ):
        d = {
            'strategy_name': self.strategy.strategy_name,
            'strategy_version': self.strategy.strategy_version,
            'strategy_para': json.dumps(self.strategy.strategy_parameters).replace(),
            # because key has '.' mongodb doesn't allow this.
            'strategy_logic': inspect.getsource(self.strategy.strategy_logic),

            'backtesting_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'backtesting_setting': json.dumps(self.backtesting_setting),
            # because key has '.' mongodb doesn't allow this.
            'backtesting_result': {
                'first_traded': self.backtesting_result['first_traded'],
                'last_traded': self.backtesting_result['last_traded'],

                'num_trade': self.backtesting_result['num_trade'],
                'time_in_market': self.backtesting_result['time_in_market'],
                'win_rate': self.backtesting_result['win_rate'],
                'avg_win': self.backtesting_result['avg_win'],
                'avg_loss': self.backtesting_result['avg_loss'],
                'payoff_ratio': self.backtesting_result['payoff_ratio'],
                'cagr': self.backtesting_result['cagr'],
                'cumulative_return': self.backtesting_result['cumulative_return'],
                'sharpe': self.backtesting_result['sharpe'],
                'sortino': self.backtesting_result['sortino'],
                'volatility': self.backtesting_result['volatility'],
                'skew': self.backtesting_result['skew'],
                'Kurtosis': self.backtesting_result['Kurtosis'],

                'kelly': self.backtesting_result['kelly'],
                'value_at_risk': self.backtesting_result['value_at_risk'],
                'max_drawdown_value': self.backtesting_result['drawdown_value'].min(),
                'max_drawdown_percent': self.backtesting_result['drawdown_percent'].min(),
                'Avg Drawdown Days': "{:.2f}".format(self.backtesting_result['drawdown_detail']['days'].mean()),
                'Max Drawdown Days': "{:.2f}".format(self.backtesting_result['drawdown_detail']['days'].max()),

            }

        }
        r = conn.insert_from_dict(db, collections, d)
        print('finish insert. Object id {}'.format(r.inserted_id))

    def run(self):
        """
        To run the backtesting, one should implement this function.
        :return:
        """
        pass

