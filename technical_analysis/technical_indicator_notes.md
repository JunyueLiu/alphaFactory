# Trend

## Average Directional Index (ADX)

- The ADX makes use of a positive (+DI) and negative (-DI) directional indicator in addition to the trendline.
- The trend has strength when ADX is above 25; the trend is weak or the price is trendless when ADX is below 20, according to Wilder.

# Price Action

## one day

| 类型             | 中文释义         | 代码                                          | 简介说明                                                     |      |
| :--------------- | :--------------- | :-------------------------------------------- | :----------------------------------------------------------- | ---- |
| Closing Marubozu | 收盘缺影线       | ta.CDLCLOSINGMARUBOZU(open, high, low, close) | 一日K线模式，以阳线为例，最低价低于开盘价，收盘价等于最高价，预示着趋势持续 |      |
| Doji             | 十字             | ta.CDLDOJI(open, high, low, close)            | 一日K线模式，开盘价与收盘价基本相同                          |      |
| Doji Star        | 十字星           | ta.CDLDOJISTAR(open, high, low, close)        | 一日K线模式，开盘价与收盘价基本相同，上下影线不会很长，预示着当前趋势反转 |      |
| Dragonfly Doji   | 蜻蜓十字/T形十字 | ta.CDLDRAGONFLYDOJI(open, high, low, close)   | 一日K线模式，开盘后价格一路走低，之后收复，收盘价与开盘价相同，预示趋势反转 |      |
| Gravestone Doji  | 墓碑十字/倒T十字 | ta.CDLGRAVESTONEDOJI(open, high, low, close)  | 一日K线模式，开盘价与收盘价相同，上影线长，无下影线，预示底部反转 |      |
| Hammer           | 锤头             | ta.CDLHAMMER(open, high, low, close)          | 一日K线模式，实体较短，无上影线，下影线大于实体长度两倍，处于下跌趋势底部，预示反转 |      |
| Hanging Man      | 上吊线           | ta.CDLHANGINGMAN(open, high, low, close)      | 一日K线模式，形状与锤子类似，处于上升趋势的顶部，预示着趋势反转 |      |
| Inverted Hammer  | 倒锤头           | ta.CDLINVERTEDHAMMER(open, high, low, close)  | 一日K线模式，上影线较长，长度为实体2倍以上，无下影线，在下跌趋势底部，预示着趋势反转 |      |
| Long Legged Doji | 长脚十字         | ta.CDLLONGLEGGEDDOJI(open, high, low, close)  | 一日K线模式，开盘价与收盘价相同居当日价格中部，上下影线长，表达市场不确定性 |      |

## two day

| 型                                   | 中文释义            | 代码                                                        | 简介说明                                                     |                                                              |
| :----------------------------------- | :------------------ | :---------------------------------------------------------- | :----------------------------------------------------------- | ------------------------------------------------------------ |
| Belt-hold                            | 捉腰带线            | ta.CDLBELTHOLD(open, high, low, close)                      | 二日K线模式，下跌趋势中，第一日阴线，第二日开盘价为最低价，阳线，收盘价接近最高价，预示价格上涨 | ![图1 看涨捉腰带线](https://bkimg.cdn.bcebos.com/pic/a8014c086e061d957945aae07ef40ad163d9cae3?x-bce-process=image/resize,m_lfit,w_631,limit_1/format,f_auto) |
| Counterattack                        | 反击线              | ta.CDLCOUNTERATTACK(open, high, low, close)                 | 二日K线模式，与分离线类似                                    | ![img](https://bkimg.cdn.bcebos.com/pic/e7cd7b899e510fb309aca28ad933c895d1430c71?x-bce-process=image/resize,m_lfit,w_268,limit_1/format,f_auto) |
| Dark Cloud Cover                     | 乌云压顶            | ta.CDLDARKCLOUDCOVER(open, high, low, close, penetration=0) | 二日K线模式，第一日长阳，第二日开盘价高于前一日最高价，收盘价处于前一日实体中部以下，预示着股价下跌 | ![K线形态——乌云压顶](https://pic1.zhimg.com/v2-814dccae444e4bb888ef2cd71c09daae_1440w.jpg?source=172ae18b) |
| Engulfing Pattern                    | 吞噬模式            | ta.CDLENGULFING(open, high, low, close)                     | 二日K线模式，分多头吞噬和空头吞噬，以多头吞噬为例，第一日为阴线，第二日阳线，第一日的开盘价和收盘价在第二日开盘价收盘价之内，但不能完全相同 | ![图 2. 模式的结构](https://c.mql5.com/2/19/Constr__1.png)   |
| Up/Down-gap side-by-side white lines | 向上/下跳空并列阳线 | ta.CDLGAPSIDESIDEWHITE(open, high, low, close)              | 二日K线模式，上升趋势向上跳空，下跌趋势向下跳空，第一日与第二日有相同开盘价，实体长度差不多，则趋势持续 | ![Image:向上跳空并列阳线的示意图.jpg](https://wiki.mbalib.com/w/images/c/c2/%E5%90%91%E4%B8%8A%E8%B7%B3%E7%A9%BA%E5%B9%B6%E5%88%97%E9%98%B3%E7%BA%BF%E7%9A%84%E7%A4%BA%E6%84%8F%E5%9B%BE.jpg) |
| Harami Pattern                       | 母子线              | ta.CDLHARAMI(open, high, low, close)                        | 二日K线模式，分多头母子与空头母子，两者相反，以多头母子为例，在下跌趋势中，第一日K线长阴，第二日开盘价收盘价在第一日价格振幅之内，为阳线，预示趋势反转，股价上升 | ![k母子.gif](https://lh4.googleusercontent.com/ymf7DoFUcM4WvpBpXCDAp-wAY8v6bB8iwNvqHsIr9c7_hlRLsN0rPeh9wNIxXCL6jl8hBPNEP6L-lQXnzh13brf_RE1kfr31T12hqBcuVCDbtBUINnrsOqHgqd2dTAIS2KYIpbOm) |
| Harami Cross Pattern                 | 十字孕线            | ta.CDLHARAMICROSS(open, high, low, close)                   | 二日K线模式，与母子县类似，若第二日K线是十字线，便称为十字孕线，预示着趋势反转转 | ![img](https://bkimg.cdn.bcebos.com/pic/71cf3bc79f3df8dcf6112eafca11728b471028db?x-bce-process=image/resize,m_lfit,w_268,limit_1/format,f_jpg) |
| Homing Pigeon                        | 家鸽                | ta.CDLHOMINGPIGEON(open, high, low, close)                  | 二日K线模式，与母子线类似，不同的的是二日K线颜色相同，第二日最高价、最低价都在第一日实体之内，预示着趋势反转 | ![img](http://www.gpedt.com/uploadfile/20151230/20151230145935745035.gif) |
| In-Neck Pattern                      | 颈内线              | ta.CDLINNECK(open, high, low, close)                        | 二日K线模式，下跌趋势中，第一日长阴线，第二日开盘价较低，收盘价略高于第一日收盘价，阳线，实体较短，预示着下跌继续 | ![蜡烛图方法3.3：颈内线（irikubi) - 远方财经](http://www.yuanfangcaijing.com/zb_users/upload/2016/09/201609261474868209363004.png) |

## three



| 类型                           | 中文释义         | 代码                                                         | 简介说明                                                     |      |
| :----------------------------- | :--------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | ---- |
| Two Crows                      | 两只乌鸦         | ta.CDL2CROWS(open, high, low, close)                         | 三日K线模式，第一天长阳，第二天高开收阴，第三天再次高开继续收阴，收盘比前一日收盘价低，预示股价下跌 |      |
| Three Black Crows              | 三只乌鸦         | ta.CDL3BLACKCROWS(open, high, low, close)                    | 三日K线模式，连续三根阴线，每日收盘价都下跌且接近最低价，每日开盘价都在上根K线实体内，预示股价下跌 |      |
| Three Inside Up/Down           | 三内部上涨和下跌 | ta.CDL3INSIDE(open, high, low, close)                        | 三日K线模式，母子信号+长K线，以三内部上涨为例，K线为阴阳阳，第三天收盘价高于第一天开盘价，第二天K线在第一天K线内部，预示着股价上涨 |      |
| Three Outside Up/Down          | 三外部上涨和下跌 | ta.CDL3OUTSIDE(open, high, low, close)                       | 三日K线模式，与三内部上涨和下跌类似，K线为阴阳阳，但第一日与第二日的K线形态相反，以三外部上涨为例，第一日K线在第二日K线内部，预示着股价上涨 |      |
| Three Stars In The South       | 南方三星         | ta.CDL3STARSINSOUTH(open, high, low, close)                  | 三日K线模式，与大敌当前相反，三日K线皆阴，第一日有长下影线，第二日与第一日类似，K线整体小于第一日，第三日无下影线实体信号，成交价格都在第一日振幅之内，预示下跌趋势反转，股价上升 |      |
| Three Advancing White Soldiers | 三个白兵         | ta.CDL3WHITESOLDIERS(open, high, low, close)                 | 三日K线模式，三日K线皆阳，每日收盘价变高且接近最高价，开盘价在前一日实体上半部，预示股价上升 |      |
| Abandoned Baby                 | 弃婴             | ta.CDLABANDONEDBABY(open, high, low, close, penetration=0)   | 三日K线模式，第二日价格跳空且收十字星（开盘价与收盘价接近，最高价最低价相差不大），预示趋势反转，发生在顶部下跌，底部上涨 |      |
| Advance Block                  | 大敌当前         | ta.CDLADVANCEBLOCK(open, high, low, close)                   | 三日K线模式，三日都收阳，每日收盘价都比前一日高，开盘价都在前一日实体以内，实体变短，上影线变长 |      |
| Evening Doji Star              | 十字暮星         | ta.CDLEVENINGDOJISTAR(open, high, low, close, penetration=0) | 三日K线模式，基本模式为暮星，第二日收盘价和开盘价相同，预示顶部反转 |      |

## four

| 类型                    | 中文释义 | 代码                                           | 简介说明                                                     |
| :---------------------- | :------- | :--------------------------------------------- | :----------------------------------------------------------- |
| Three-Line Strike       | 三线打击 | ta.CDL3LINESTRIKE(open, high, low, close)      | 四日K线模式，前三根阳线，每日收盘价都比前一日高，开盘价在前一日实体内，第四日市场高开，收盘价低于第一日开盘价，预示股价下跌 |
| Concealing Baby Swallow | 藏婴吞没 | ta.CDLCONCEALBABYSWALL(open, high, low, close) | 四日K线模式，下跌趋势中，前两日阴线无影线，第二日开盘、收盘价皆低于第二日，第三日倒锤头，第四日开盘价高于前一日最高价，收盘价低于前一日最低价，预示着底部反转 |

| 类型                              | 中文释义          | 代码                                                 | 简介说明                                                     |
| :-------------------------------- | :---------------- | :--------------------------------------------------- | :----------------------------------------------------------- |
| Breakaway                         | 脱离              | ta.CDLBREAKAWAY(open, high, low, close)              | 五日K线模式，以看涨脱离为例，下跌趋势中，第一日长阴线，第二日跳空阴线，延续趋势开始震荡，第五日长阳线，收盘价在第一天收盘价与第二天开盘价之间，预示价格上涨 |
| Ladder Bottom                     | 梯底              | ta.CDLLADDERBOTTOM(open, high, low, close)           | 五日K线模式，下跌趋势中，前三日阴线，开盘价与收盘价皆低于前一日开盘、收盘价，第四日倒锤头，第五日开盘价高于前一日开盘价，阳线，收盘价高于前几日价格振幅，预示着底部反转 |
| Mat Hold                          | 铺垫              | ta.CDLMATHOLD(open, high, low, close, penetration=0) | 五日K线模式，上涨趋势中，第一日阳线，第二日跳空高开影线，第三、四日短实体影线，第五日阳线，收盘价高于前四日，预示趋势持续 |
| Rising/Falling Three Methods      | 上升/下降三法     | ta.CDLRISEFALL3METHODS(open, high, low, close)       | 五日K线模式，以上升三法为例，上涨趋势中，第一日长阳线，中间三日价格在第一日范围内小幅震荡，第五日长阳线，收盘价高于第一日收盘价，预示股价上升 |
| Upside/Downside Gap Three Methods | 上升/下降跳空三法 | ta.CDLXSIDEGAP3METHODS(open, high, low, close)       | 五日K线模式，以上升跳空三法为例，上涨趋势中，第一日长阳线，第二日短阳线，第三日跳空阳线，第四日阴线，开盘价与收盘价于前两日实体内，第五日长阳线，收盘价高于第一日收盘价，预示股价上升 |

# Prop

channel

