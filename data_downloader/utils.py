def joinquant_to_yfinance_ticker(code_list: list):
    ticker = []
    for code in code_list:
        s = code.split('.')
        if s[1] == 'XSHE':
            ticker.append(s[0] + '.SZ')
        elif s[1] == 'XSHG':
            ticker.append(s[0] + '.SS')
    return ticker

