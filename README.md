# alphaFactory
## Introduction
The AlphaFactory project provides an end-to-end solution to apply quantitative finance research. 
It shortens the process of developing a quantitative trading strategy.

The modules could be divided into four part, alpha_research, fin_ml, backtesting and trader.

## Quick Start

### Alpha research

For single asset
```python
import numpy as np
from alpha_research.SingleAssetResearch import SingleAssetResearch

# df is pandas Dataframe, with index in DatetimeIndex
df = ...
factor_study = SingleAssetResearch(df)
# make your own alpha
def cheating_alpha(data, time_lag=5):
    factor = data['close'].shift(-time_lag) - data['close']
    factor += np.random.randn(len(factor))
    factor.fillna(0, inplace=True)
    return factor
# calculate alpha
factor_study.calculate_factor(cheating_alpha, **{'time_lag': 5})
# use the dash app to see the result
factor_study.get_evaluation_dash_app().run_server('127.0.0.1', debug=True)

```
For multi Asset
```python
# df is pandas Dataframe, with MultiIndex (level 0 DatetimeIndex, level 1 Asset Code)
import pandas as pd
import numpy as np
from alpha_research.MultiAssetResearch import MultiAssetResearch
df = ...
multi_study = MultiAssetResearch(df)
# benchmark is pandas Dataframe, with index in DatetimeIndex
benchmark = ...
# group is dictionary, key is code, value is sector
group = ...

# define your alpha
def cheating_alpha(df: pd.DataFrame, time_lag=1):
    factor = - df['close'].groupby(level=1).diff(-time_lag)
    factor += 10 * np.random.randn(len(factor))
    return factor


multi_study.set_asset_group(group)
multi_study.set_benchmark(benchmark)
multi_study.calculate_factor(cheating_alpha, **{'time_lag':5})
multi_study.get_evaluation_dash_app().run_server(host='127.0.0.1', debug=True)


```

For more examples, see example