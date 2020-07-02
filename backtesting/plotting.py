from graph.backtesting_component import net_value_line, returns_distribution, entry_exit_dot, entrust_dot
from plotly import graph_objects as go
from graph.bar_component import ohlc, candlestick
import plotly.figure_factory as ff
import pandas as pd
import plotly.io as pio


pio.renderers.default = "browser"


def net_value_plot(strategy_net_value: pd.Series, benchmark: pd.Series or None = None, strategy_name='strategy'):
    fig = go.Figure()
    fig.add_trace(net_value_line(strategy_net_value / strategy_net_value[0], name=strategy_name), )
    if benchmark is not None:
        # todo benchmark fit with the strategy net value
        benchmark_copy = benchmark[(benchmark.index >= net_value.index[0]) & (benchmark.index <= net_value.index[-1])]
        # benchmark_copy = benchmark_copy[benchmark_copy.index <= net_value.index[-1]]
        fig.add_trace(net_value_line(benchmark_copy / benchmark_copy[0], color='#FFCC00', name='benchmark'))
    return fig


def returns_distribution_plot(returns: pd.Series):
    fig = go.Figure()
    fig.add_trace(returns_distribution(returns))
    fig.update_layout(
        title="Return Distribution",)
    return fig


def entry_and_exit_plot(ohlc_df, traded: pd.DataFrame, symbol: str, ohlc_graph=True, price_key='close', ohlc_key=None,
                        entrust=False):
    # traded columns:
    # code,order_time,order_price,order_qty,order_type,dealt_price,dealt_qty,order_direction,order_status,update_time,
    # exchange_order_id,order_id,cash_inflow
    fig = go.Figure()

    # filter out unrelated trade
    traded = traded[traded['code'] == symbol]
    long = traded[traded['order_direction'] == 'LONG']
    short = traded[traded['order_direction'] == 'SHORT']

    if ohlc_graph:
        candles = candlestick(ohlc_df, ohlc_key=ohlc_key, symbol=symbol)
        fig.add_trace(candles)
    else:
        prices = net_value_line(ohlc_df[price_key], color='#FFA500', name=symbol)
        fig.add_trace(prices)

    long_dot = entry_exit_dot(long, True)
    short_dot = entry_exit_dot(short, False)
    fig.add_trace(long_dot)
    fig.add_trace(short_dot)
    if entrust:
        entrust_long = entrust_dot(long, True)
        entrust_short = entrust_dot(short, False)
        fig.add_trace(entrust_long)
        fig.add_trace(entrust_short)
    fig.update_layout(showlegend=False, yaxis=dict(
        autorange=True,
        fixedrange=False
    ))

    return fig


if __name__ == '__main__':
    traded_pnl = pd.read_csv('traded_pnl_sample.csv')
    net_value = pd.read_csv('net_value_sample.csv', squeeze=True, index_col=0)
    traded = pd.read_csv('traded_sample.csv')
    traded = traded[-100:]

    net_value.index = pd.to_datetime(net_value.index)
    benchmark = pd.read_csv(r'../HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv')
    benchmark['time_key'] = pd.to_datetime(benchmark['time_key'])
    benchmark.set_index('time_key', inplace=True)
    # benchmark = benchmark[benchmark.index >= net_value.index[0]]
    # benchmark = benchmark[benchmark.index <= net_value.index[-1]]
    # benchmark = benchmark[-1000:]
    # returns['time_key'] = pd.to_datetime(returns['time_key'])
    # returns.set_index('time_key', inplace=True)

    # fig = returns_distribution_plot(traded_pnl['cash_inflow'])

    fig = net_value_plot(net_value, benchmark['close'])
    # fig = entry_and_exit_plot(benchmark, traded, 'HK_FUTURE.999010', False, entrust=True)
    fig.show()
