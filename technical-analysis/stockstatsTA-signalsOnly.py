import ta

import csv
import urllib.request as urllib2
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import os
import sys
import json
from threading import Timer
import random
from TAind import volumeFn, voltalityFn, trendFn, momentumFn

from colorama import Fore, Style
from colorama import init
init()


keys = []

initBal = 0
count = 0

symb = ['AAPL','CVX','VVV','LMT','MMM','SBUX','WMT','JNJ','JPM','MSFT','GOOG','NEE','SPG']
#url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+sym +'&interval=1min&datatype=csv&outputsize=compact&apikey=W8L7PK09ZI5N4RJ9'
#url = 'https://intraday.worldtradingdata.com/api/v1/intraday?symbol=' + sym + '&interval=1&range=1&output=csv&sort=desc&api_token=BtNUxpb4hOPJp7AIQsKpgW2x4stWLoNl38iAABbESnmefgQ1mKl4v7rCzgWv'
#print(url)

#response = urllib2.urlopen(url)
#cr = csv.reader(response)

#df = pd.read_csv('worldtradingdata-intraday-SNAP.csv',skiprows=1,nrows = 100) 
#df = pd.read_csv(response,skiprows=1,nrows = 100) 



#api.cancel_all_orders()
#sym = random.choice(symb)
sym = 'NSE:RELIANCE'	
print ('Evaluating New Trade')
#response = api.get_barset(sym,'1Min')
print(sym)
	#print(response)
	#df = barSetToJSON(response[sym])
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+sym +'&interval=1min&datatype=csv&outputsize=compact&apikey=' + random.choice(keys)
response = ''
try:
	response = urllib2.urlopen(url)
		#print(response,')
except:
	print("Alpha Vantage Connection Error")
	sys.exit(0)		
df = pd.read_csv(response) 

if (len(df) != 100):
	tim = Timer(20.0,newTrade)
	tim.start()		
	
df = df[::-1]
	#df.drop(df.index[1])

	#print(df.head())

	#df['close'] = df['Close']
	#df['open'] = df['Open']
	#df['high'] = df['High']
	#df['low'] = df['Low']
	#df['volume'] = df['Volume']
	#df.drop(['Close','Open','High','Low'])
try:
	df = ta.add_all_ta_features(df, "open", "high", "low", "close", "volume", fillna=True)
except:
	print ('Invalid Data Frame Object')
	tim = Timer(15.0,newTrade)
	tim.start()		
	#df['volume_mfi'] = df['momentum_mfi']
	#df.drop('momentum_mfi')
df['volatility_dcp'] = (200*(df['volatility_dch'] - df['volatility_dcl'])) /(df['volatility_dcl'] + df['volatility_dch']) 
	#print(df['volatility_dcm'])

		
	#print(len(df.columns))
dirVol = 0
voltV = 0
trendV = 0
trendD = 0
momtD = 0
if (df['trend_adx_pos'][0] > df['trend_adx_neg'][0]):
	trendD += 1
elif (df['trend_adx_pos'][0] < df['trend_adx_neg'][0]):
	trendD -= 1
else:
	trendD += 0

if (df['trend_aroon_ind'][0] > 0 and abs(df['trend_aroon_ind'][0])>40):
	trendD += 1
elif (df['trend_aroon_ind'][0] < 0 and abs(df['trend_aroon_ind'][0])>40):
	trendD -= 1
else:
	trendD += 0

if (df['trend_cci'][0] > 0):
	trendD += 1
elif (df['trend_cci'][0] < 0):
	trendD -= 1
else:
	trendD += 0

	#The real power of the Detrended Price Oscillator is in identifying turning points in longer cycles:

if (df['trend_dpo'][0] < 0.05 and df['trend_dpo'][0] > 0):
	trendD -= 1
elif (df['trend_dpo'][0] > -0.05 and df['trend_dpo'][0] < 0):
	trendD += 1
else:
	trendD += 0

	#not using trend_EMA for anything.
trendT = ''
if (df['trend_visual_ichimoku_a'][0]<df['trend_visual_ichimoku_b'][0]):
	trendD -= 1
	trentT = 'fall'
elif (df['trend_visual_ichimoku_a'][0]>df['trend_visual_ichimoku_b'][0]):
	trendD += 1
	trendT = 'rise'
else:
	trendD += 0		
	trentT = ''

if (trendT == 'fall' and df['close'][0] < df['trend_visual_ichimoku_a'][0]):
	trendD -= 2 #strong sell 
	trendV += 2 #strong trend
elif (trendT == 'rise' and df['close'][0] > df['trend_visual_ichimoku_a'][0]):
	trendD += 2 #strong buy
	trendV += 2 #strong trend


if (df['trend_ichimoku_a'][0] < df['trend_ichimoku_b'][0]):
	trendD -= 1
elif (df['trend_ichimoku_a'][0] > df['trend_ichimoku_b'][0]):
	trendD += 1
else:
	trendD += 0

if (df['trend_kst'][0] < 0.5):
	trendD -= 1
elif (df['trend_kst'][0] > 0.5):
	trendD += 1
else:
	trendD += 0

if (df['trend_macd'][0] < 0):
	trendD -= 1
elif (df['trend_macd'][0] > 0):
	trendD += 1
else:
	trendD += 0

miIn = df['trend_mass_index'][0]
if miIn > 25:
	for i in df['trend_mass_index']:
		if (i > 35 and i != miIn):
			#trendD = -trendD #Reversal
			print('Reversal Spotted')

	 
trendD += df['trend_psar_up_indicator'][0]
trendD -= df['trend_psar_down_indicator'][0]

		
for i in df:
	Itype = i.split('_')[0]	
	name = '-'		
	Iname = name.join(i.split('_')[1:])
	if (Itype == 'volume' and Iname != ''):
		dirVol += int(volumeFn (Iname,df[i]))
	elif (Itype == 'volatility'):
		voltV += int(voltalityFn (Iname,df[i]))
	elif (Itype == 'trend'):
		trendV += int(trendFn (Iname,df[i]))
	elif (Itype == 'momentum'):
		momtD += int(momentumFn (Iname,df[i],df['close'])) 
			#print(volumeFn (Iname,df[i]))
		#print(i,df[i][0])		
print ("Volume Direction:" , dirVol) #max 8
print ("Voltality:", voltV) #max 4
print ("Trend Value:", trendV) #max 6
print ("Trend Direction:", trendD) #max 10
print ("Momentum Direction:", momtD) #max 7

openP = df['open'][0]
lowP = df['low'][0]
highP = df['high'][0]
closeP = df['close'][0]

netDir = dirVol + trendD

action = ''

if (netDir) < 0:
	action = 'sell'
elif (netDir) == 0:
	action = 'none'
else:
	action = 'buy'
if ((voltV >= -4 and trendV >= 2) or (voltV >= -1 and trendV >= 1) ):

	

	qnty = 0  #0.1 to simulate real life with $40k as buffer for margin.
	orderPlaced = 0
	
		
	if action == 'buy': #originally buy
		buyP = lowP
		targetP = 0
		if voltV >= 3:
			targetP = lowP *(100+0.1*abs(voltV)+0.1*abs(trendV))/100
		else:			
			targetP = lowP * 1.0011			
		stopLoss = lowP * 0.998
		print ("Placed buy order ", buyP, targetP, stopLoss,qnty)				
			
			
		
	elif action == 'sell': #originally sell
		sellP = highP
		targetP = 0
		if voltV >= 3:
			targetP = highP *(100-0.1*abs(voltV)-0.1*abs(trendV))/100
		else:				
			targetP = highP * 0.9989
		stopLoss = highP * 1.002
		print ("Placed sell order ", sellP, targetP, stopLoss,qnty)			
				

		

	else:
		print ('Lack of Direction', netDir)
			
else:
	print ('Lack of Trend and Voltality',trendV,voltV)
	





	



