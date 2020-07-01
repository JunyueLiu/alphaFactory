import numpy as np
from plotly import figure_factory as ff
import dash_table
from scipy import stats
from graph.factor_component import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from alpha_research.utils import *


def price_factor_plot(data: pd.DataFrame, factor: pd.Series, price_key='close', price_name='close',
                      factor_name='factor', ):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    strftime_format = generate_strftime_format(factor.index)
    fig.add_trace(line(factor, name=factor_name, color='#FFBF00', strftime_format=strftime_format), secondary_y=True)
    fig.add_trace(line(data[price_key], name=price_name, color='#008000', strftime_format=strftime_format),
                  secondary_y=False)
    fig.update_layout(
        title_text=""
    )
    # Set x-axis title
    fig.update_xaxes(title_text="time")

    # Set y-axes titles
    fig.update_yaxes(title_text=price_name,
                     range=[data[price_key].min() * 0.99, data[price_key].max() * 1.01],
                     secondary_y=False)
    fig.update_yaxes(title_text=factor_name, secondary_y=True)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, yaxis_tickformat='g')
    return fig


def returns_plot(factor_returns, factor_name='factor'):
    fig = go.Figure()
    strftime_format = generate_strftime_format(factor_returns.index)
    for col in factor_returns.columns:
        fig.add_trace(line(factor_returns[col], name=factor_name + '_' + col, strftime_format=strftime_format))
    # fig.update_layout(yaxis_tickformat='g')
    return fig


def cumulative_return_plot(cumulative_factor_returns, benchmark=None, factor_name='factor', benchmark_name='benchmark'):
    fig = go.Figure()
    strftime_format = generate_strftime_format(cumulative_factor_returns.index)
    for col in cumulative_factor_returns.columns:
        fig.add_trace(
            line(cumulative_factor_returns[col], name=factor_name + '_' + col, strftime_format=strftime_format))
    if benchmark is not None:



        fig.add_trace(line(benchmark, name=benchmark_name, color='#008000', strftime_format=strftime_format))
    return fig


def factor_forward_return_plot(factor: pd.Series, forward_returns: pd.DataFrame):
    fig = go.Figure()
    # todo
    # fig.add_trace(go.Scatter())
    pass


def factor_distribution_plot(factor):
    fig = go.Figure()
    fig.add_trace(histogram(factor))
    return fig


def entry_and_exit_plot(data: pd.DataFrame, factor, price_key='close'):
    strftime_format = generate_strftime_format(data.index)
    fig = go.Figure()
    fig.add_trace(line(data[price_key], name=price_key, color='grey', strftime_format=strftime_format))
    long = pd.Series(np.where(factor == 1, data[price_key], np.nan), index=data.index)
    short = pd.Series(np.where(factor == -1, data[price_key], np.nan), index=data.index)

    fig.add_trace(line(long, name='long', color='green', strftime_format=strftime_format))
    fig.add_trace(line(short, name='short', color='red', strftime_format=strftime_format))

    fig.update_layout(yaxis_tickformat='g')
    return fig


def qq_plot(factor: pd.DataFrame):
    factor = factor.dropna()
    qq = stats.probplot(factor, dist='norm', sparams=(1,))
    x = np.array([qq[0][0][0], qq[0][0][-1]])
    fig = go.Figure()
    pts = go.Scatter(x=qq[0][0],
                     y=qq[0][1],
                     mode='markers',
                     showlegend=False
                     )
    line = go.Scatter(x=x,
                      y=qq[1][1] + qq[1][0] * x,
                      showlegend=False,
                      mode='lines'
                      )
    fig.add_trace(pts)
    fig.add_trace(line)
    fig.update_xaxes(title_text="Normal Distribution Quantile")
    fig.update_yaxes(title_text="Factor Observed Quantile")
    return fig


def overlaid_factor_distribution_plot(in_sample_factor: pd.Series, out_sample_factor: pd.Series):
    fig = go.Figure()
    fig.add_trace(histogram(in_sample_factor))
    fig.add_trace(histogram(out_sample_factor))
    fig.update_layout(barmode='overlay')
    return fig


def observed_qq_plot(in_sample_factor: pd.Series, out_sample_factor: pd.Series):
    x = in_sample_factor.values
    y = out_sample_factor.values
    x.sort()
    y.sort()

    fig = go.Figure()
    pts = go.Scatter(x=x,
                     y=y,
                     mode='markers',
                     showlegend=False
                     )
    line = go.Scatter(x=x,
                      y=x,
                      showlegend=False,
                      mode='lines'
                      )
    fig.add_trace(pts)
    fig.add_trace(line)
    fig.update_xaxes(title_text="In the sample Observed Quantile")
    fig.update_yaxes(title_text="Out of the sample Observed Quantile")
    return fig


def position_plot(position: pd.Series) -> go.Figure:
    """

    :param position:
    :return:
    """
    # todo so many lines here, need to support selection functionality.
    fig = go.Figure()
    strftime_format = generate_strftime_format(position.index.get_level_values(0))
    for asset_ts in position.groupby(level=1):
        fig.add_trace(
            line(asset_ts[1], timestamp=asset_ts[1].index.get_level_values(0), name=asset_ts[0],
                 strftime_format=strftime_format))
    return fig


def turnover_plot(turnover: pd.Series) -> go.Figure:
    """

    :param turnover:
    :return:
    """
    fig = go.Figure()
    strftime_format = generate_strftime_format(turnover.index)
    fig.add_trace(line(turnover, strftime_format=strftime_format))
    return fig


def returns_by_quantile_bar_plot(mean_ret: pd.DataFrame, ) -> go.Figure:
    # sample
    #                       1_period_return  5_period_return  10_period_return
    # factor_quantile
    # 1                       0.014033         0.032236          0.044672
    # 2                       0.012368         0.025965          0.035857
    # 3                       0.010046         0.022567          0.032039
    # 4                       0.013727         0.029933          0.041088
    # 5                       0.012879         0.029367          0.039913
    fig = go.Figure()
    for ret_col in mean_ret.columns:
        fig.add_trace(bar(mean_ret.index, mean_ret[ret_col], ret_col))
    return fig


def returns_by_quantile_heatmap_plot(mean_ret: pd.DataFrame, ) -> go.Figure:
    # sample
    #                       1_period_return  5_period_return  10_period_return
    # factor_quantile
    # 1                       0.014033         0.032236          0.044672
    # 2                       0.012368         0.025965          0.035857
    # 3                       0.010046         0.022567          0.032039
    # 4                       0.013727         0.029933          0.041088
    # 5                       0.012879         0.029367          0.039913
    fig = go.Figure()
    fig.add_trace(heatmap(mean_ret.columns, mean_ret.index, mean_ret.values))
    fig.update_layout(
        {'xaxis': {'type': 'category'},
         'yaxis': {'type': 'category'}

         }
    )
    return fig


def returns_by_quantile_distplot(quantile_ret_ts: pd.DataFrame):
    """

    :param quantile_ret_ts:
    :return:
    """
    #                             1_period_return  5_period_return  10_period_return
    # factor_quantile Date
    # 1               2010-06-17         0.002230         0.021172         -0.014775
    #                 2010-06-18         0.036203         0.017436         -0.016843
    #                 2010-06-21        -0.004873        -0.017346         -0.035416
    #                 2010-06-22        -0.000315        -0.036443         -0.046313
    #                 2010-06-23        -0.010813        -0.039430         -0.039475
    # ...                                     ...              ...               ...
    fig = make_subplots(rows=len(quantile_ret_ts.columns), cols=1)
    count = 1
    for ret_col in quantile_ret_ts.columns:
        hist_data = []
        group_labels = []
        grouped = quantile_ret_ts[ret_col].groupby(level=0)
        for group in grouped:
            group_labels.append(ret_col + ' ' + str(group[0]) + ' quantile')
            hist_data.append(group[1].dropna().values)
        fig1 = ff.create_distplot(hist_data, group_labels, bin_size=.1)
        # fig1 has multi graph object
        for i in range(len(fig1.data)):
            fig.add_trace(fig1.data[i], row=count, col=1)
        count += 1
    return fig


def cumulative_returns_by_quantile_plot(cum_ret_by_qt_ts: pd.Series):
    strftime_format = generate_strftime_format(cum_ret_by_qt_ts.index.get_level_values(1))
    fig = go.Figure()
    for g in cum_ret_by_qt_ts.groupby(level=0):
        fig.add_trace(line(g[1], timestamp=g[1].index.get_level_values(1), name=g[0], strftime_format=strftime_format))
    return fig


def monthly_ic_heatmap_plot(mean_monthly_ic):
    mean_monthly_ic = mean_monthly_ic.copy()

    # 给原来df的添加一个index,便于后面搜索
    mean_monthly_ic = mean_monthly_ic \
        .set_index([mean_monthly_ic['year'], mean_monthly_ic['month']])
    # print(mean_monthly_ic)

    # 设定集合
    x = [str(i) for i in range(1, 13)]  # month
    y = list(set([int(i) for i in mean_monthly_ic['year']]))  # year 去重
    y.sort(reverse=True)

    mean_monthly_ic = mean_monthly_ic.drop(columns=['month', 'year'])
    # print(mean_monthly_ic)
    # heatmap的z
    z = list()
    # heatmap titles
    titles = list()

    for i in mean_monthly_ic.iteritems():
        titles.append(i[0])

        z_year = list()
        for year in y:
            z_month = list()
            for month in x:
                try:
                    ic = i[1].loc[str(year), str(month)]
                except:
                    z_month.append(np.nan)
                else:
                    z_month.append(ic)
            # z_year存的是一个period的heatmap
            z_year.append(z_month)
        # z存的是所有period的heatmap
        z.append(z_year)
    # 开始画图

    fig = make_subplots(rows=int(len(mean_monthly_ic.columns) / 3) + 1,
                        cols=3, subplot_titles=titles)
    count = 0
    for z1 in z:
        # z1 是其中一个subplot的z
        fig1 = ff.create_annotated_heatmap(x=x, y=y, z=np.array(z1),
                                           hoverinfo='z')
        # fig1.show()
        fig.add_trace(fig1.data[0], int(count / 3) + 1, count % 3 + 1)

        count += 1

    layout = dict()
    for i in range(1, count + 1):
        layout['xaxis' + str(i)] = {'type': 'category'}
        layout['yaxis' + str(i)] = {'type': 'category'}

    fig.update_layout(
        layout
    )

    return fig


def pd_to_dash_table(data: pd.DataFrame or pd.Series, id: str or None = None):
    if isinstance(data, pd.Series):
        df = pd.DataFrame(data, index=data.index, columns=data.name)
    else:
        df = data.copy()
    df = df.reset_index()
    # print(df)
    df = df.round(decimals=3)
    # df.rename(index={'index': ' '}, inplace=True)
    return dash_table.DataTable(
        id=id,
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
