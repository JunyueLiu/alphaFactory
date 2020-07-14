import numpy as np
import pandas as pd

from portfolioManager.plotting import net_values_plot, corr_heatmap, ret_heatmap
import plotly.io as pio

pio.renderers.default = "browser"


def add_benchmark(net_values: pd.DataFrame, benchmark: pd.Series):
    benchmark.name = 'benchmark'
    net_values = net_values.join(benchmark)
    net_values['benchmark'] = net_values['benchmark'] / net_values['benchmark'][0]
    return net_values


def unstack_series(net_values: pd.Series) -> pd.DataFrame:
    return net_values.unstack(level=-1)


def pairwise_corr(net_values: pd.DataFrame) -> pd.DataFrame:
    return net_values.corr()


# pairwise correlation


if __name__ == '__main__':
    data = pd.read_csv(r'../hsi_component.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date', 'code'], inplace=True)
    data = data['close']
    data = data.groupby(level=1).apply(lambda x: x / x[0])
    data = data.unstack(level=-1)
    # pairwise correlation
    data.corr()

    benchmark = pd.read_csv(r'../^HSI_1986-12-31 00:00:00_2020-07-07 00:00:00.csv')
    benchmark['Date'] = pd.to_datetime(benchmark['Date'])
    benchmark.set_index('Date', inplace=True)
    benchmark = benchmark['close']
    benchmark.name = 'benchmark'
    net_values = add_benchmark(data, benchmark)
    # fig = net_values_plot(net_values)
    # fig.show()
    # corr_heatmap(pairwise_corr(net_values)).show()
    ret_heatmap(net_values).show()
