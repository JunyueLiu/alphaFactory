from plotly import graph_objects as go
import pandas as pd

def net_value_line(net_value:pd.Series):
    pass

def returns_distribution(returns: pd.DataFrame or pd.Series):
    return go.Histogram(x=returns)

