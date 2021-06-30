# Stock Trading Bot 

This is a small side project that I built for automated trading using Alpaca API.

This bot can perform high frequency trading (HFT) by simultanesouly analyzing patterns in multiple stocks and taking an action when a pattern of interest is detected in any of the stocks.

The bot can uses the following APIs:

1. AlphaVantage and WorldTradingData for obtaining real time 5 min data for identifying patterns.
2. Alpaca API for placing actual orders.


The bot uses the following strategy for placing a trade:

1. Place a buy order if Voltality signals return a sum of 1 or more and trend indicators return a sum of 1 or more. 
Indicates a strong trend with good voltality. Such trades carry the potential for most profit.

2. Place a sell order if above conditions are true and direction signals return a value <0.

The script makes a calculation based on the results from indicators (using [TAind.py](https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html)).

## Sample Execution

The following is the result of a sample execution of the bot:

```
PG
AXP
DIS
JNJ
WMT
V
GS
DIS
DOW
JNJ
MCD
Placed buy order  459.63 461.93 458.71074 269
Placed sell order  208.9 207.8555 209.3178 534
Placed sell order  166.1 165.2695 166.4322 604
Made  21.679999999993015  from last transaction
Placed sell order  102.41 102.19493899999999 102.61482 1215
Cancelling Order Not Executed Since 2 minutes
Placed sell order  166.1 165.75119 166.4322 746
Cancelling Order Not Executed Since 2 minutes
Placed sell order  102.41 102.19493899999999 102.61482 1215
Cancelling Order Not Executed Since 2 minutes
Placed buy order  280.5 281.09 279.939 442
Placed sell order  148.24 147.64704 148.53648 836
Made  -16.720000000030268  from last transaction
Placed sell order  208.9 208.46131 209.3178 533
Made  -91.3399999999674  from last transaction
Placed buy order  102.0 102.21 101.796 982
Made  -35.73999999999069  from last transaction
Placed sell order  1507.73 1500.19135 1510.74546 59
Placed sell order  102.41 102.19493899999999 102.61482 798
Made  -15.880000000004657  from last transaction
Made  -77.42999999999302  from last transaction
Placed buy order  102.41 102.63 102.20518 798
Made  -53.13000000000466  from last transaction
Placed buy order  208.9 209.34 208.4822 351
(<class 'alpaca_trade_api.rest.APIError'>, APIError('bracket orders must be entry orders'), <traceback object at 0x7f1954527550>)
Made  82.19000000000233  from last transaction
Placed buy order  148.24 148.55 147.94352 495
(<class 'alpaca_trade_api.rest.APIError'>, APIError('bracket orders must be entry orders'), <traceback object at 0x7f1954524230>)
Placed sell order  280.01 279.421979 280.57002 262
Made  12.64000000001397  from last transaction
Placed sell order  208.75 207.70625 209.1675 315
Placed buy order  43.2 43.29 43.113600000000005 1478
Made  -25.79999999998836  from last transaction
Made  -60.929999999993015  from last transaction
Placed buy order  132.6 132.88 132.3348 432
Made  -202.86999999999534  from last transaction
Placed buy order  208.9 209.34 208.4822 275
(<class 'alpaca_trade_api.rest.APIError'>, APIError('bracket orders must be entry orders'), <traceback object at 0x7f19544b5960>)
Made  59.64000000001397  from last transaction
Placed sell order  1507.73 1504.563767 1510.74546 38
Made  -185.0900000000256  from last transaction
Placed buy order  21.71 21.76 21.66658 2385
Made  66.44000000000233  from last transaction
```

## Future Development Ideas

The script can be developed further with more signals and sanity checks for better use.
