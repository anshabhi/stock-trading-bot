from ta import *

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
import warnings

warnings.filterwarnings('error')
os.environ["APCA_API_KEY_ID"] = "PKI37FK2CS8QK7EZRT7L"
os.environ["APCA_API_SECRET_KEY"] = "XcpmtZmZpYgWHPQbAZvPLRA9tK5GNDO9Hea9XKoL"
os.environ["APCA_API_BASE_URL"] = 'https://paper-api.alpaca.markets'

keys = ['WQUPVCZ9LPDRU9YB','W8L7PK09ZI5N4RJ9','UCTMQ2OG73YOLK3V']
api = tradeapi.REST()
api.cancel_all_orders()
initBal = 0
count = 0



def checkOrder():
	other = open('other.txt', 'a') 
	trade = open('trade.txt','a')
	global initBal
	global count
	global tim
	open_orders = api.list_orders(
    		status='open',
    		limit=100
		)
	clock = api.get_clock()
	if clock.is_open == False:
		print('Markets Closed. Go Home')
		api.cancel_all_orders()
		sys.exit(0)
		
	tim.cancel()
	if (len(open_orders) == 0):
		account = api.get_account()
		balance_change = float(account.equity) - float(initBal)
		if (balance_change > 0):
			print ('Made ', balance_change , ' from last transaction',file = trade)
			print ('Made ', balance_change , ' from last transaction',file = other)
			print ('Made ', balance_change , ' from last transaction')
		elif (balance_change < 0):
			print ('Made ', balance_change , ' from last transaction',file=trade)
			print ('Made ', balance_change , ' from last transaction',file = other)
			print ('Made ', balance_change , ' from last transaction')
		tim = Timer(5.0, newTrade)
		tim.start()
		#timer.cancel()
	else:


		portfolio = api.list_positions()
		if len(portfolio) == 0:
			print('open order pending',file=other)
			print('open order pending')
			count = count + 1
		elif len(portfolio) == 1:
			count = 0
			print ('open position pending',file=other)
			print ('open position pending')
		else:
			print('More than 1 position open',file=other)
			print('More than 1 position open')

		if count > 2 and len(portfolio) == 0:
			api.cancel_all_orders()	
			count = 0
			print ('Cancelling Order Not Executed Since 2 minutes',file=trade)
			print ('Cancelling Order Not Executed Since 2 minutes',file=other)
			print ('Cancelling Order Not Executed Since 2 minutes')
			tim = Timer(5.0, newTrade)
			tim.start()
		tim = Timer(60.0, checkOrder)
		tim.start()
	other.close()
	trade.close()
#symb = ['AAPL','CVX','VVV','LMT','MMM','SBUX','WMT','JNJ','JPM','MSFT','GOOG','NEE','SPG']
symb = ['MSFT','AAPL','GOOG','V','JNJ','WMT','MMM','AXP','CAT','CVX','CSCO','KO','DIS','DOW','GS','HD','IBM','INTC','MCD','MRK','PG','NKE','VZ']
#url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+sym +'&interval=1min&datatype=csv&outputsize=compact&apikey=W8L7PK09ZI5N4RJ9'
#url = 'https://intraday.worldtradingdata.com/api/v1/intraday?symbol=' + sym + '&interval=1&range=1&output=csv&sort=desc&api_token=BtNUxpb4hOPJp7AIQsKpgW2x4stWLoNl38iAABbESnmefgQ1mKl4v7rCzgWv'
#print(url)

#response = urllib2.urlopen(url)
#cr = csv.reader(response)

#df = pd.read_csv('worldtradingdata-intraday-SNAP.csv',skiprows=1,nrows = 100) 
#df = pd.read_csv(response,skiprows=1,nrows = 100) 
def barSetToJSON (barSet):
	#print(barSet)

	df = pd.DataFrame (columns=["time","open","high","low","close","volume"])

	for bar in barSet:
		elem = [bar.t,bar.o,bar.h,bar.l,bar.c,bar.v]
		df.loc[len(df)] = elem
	df = df[0:100]	

	return df

def newTrade():
	global tim
	#if tim.is_alive():
	other = open('other.txt', 'a') 
	trade = open('trade.txt','a')
	#other.close()
	#trade.close()
	tim.cancel()

	sym = random.choice(symb)
	print ('Evaluating New Trade')
	print ('Evaluating New Trade',file=other)
	#response = api.get_barset(sym,'1Min')
	print(sym)
	print(sym,file = other)
	print(sym,file = trade)
	#print(response)
	#df = barSetToJSON(response[sym])
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+sym +'&interval=1min&datatype=csv&outputsize=compact&apikey=' + random.choice(keys)
	response = ''
	try:
		response = urllib2.urlopen(url)
		#print(response,')
	except:
		#global tim
		print("Alpha Vantage Connection Error")
		print("Alpha Vantage Connection Error",file = other)
		tim = Timer(15.0,newTrade)
		tim.start()		
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
		df['volatility_dcp'] = (200*(df['volatility_dch'] - df['volatility_dcl'])) /(df['volatility_dcl'] + df['volatility_dch']) 
	except:
		#global tim
		print ('Invalid Data Frame Object')
		print ('Invalid Data Frame Object',file=other)
		tim = Timer(15.0,newTrade)
		tim.start()		
	#df['volume_mfi'] = df['momentum_mfi']
	#df.drop('momentum_mfi')

	#print(df['volatility_dcm'])

		
	#print(len(df.columns))
	dirVol = 0
	voltV = 0
	trendV = 0
	trendD = 0
	momtD = 0
	#print(df.columns)
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
	#print ("Volume Direction:" , dirVol) #max 8
	#print ("Voltality:", voltV) #max 4
	#print ("Trend Value:", trendV) #max 6
	#print ("Trend Direction:", trendD) #max 10
	#print ("Momentum Direction:", momtD) #max 7

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
		price = closeP
		try:
			url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' +sym +'&apikey=' + random.choice(keys)
			response = json.loads(urllib2.urlopen(url).read())
			price = float(response['Global Quote']['05. price'])

		except:
			print("Alpha Vantage - LTP Data Error")
			print("Alpha Vantage - LTP Data Error",file = other)
			print(url,response)
			print(url,response,file=other) 
			tim = Timer(15.0,newTrade)
			tim.start()	
		account = api.get_account()
		global initBal 
		initBal = account.equity
		qnty = (float(account.daytrading_buying_power)*0.1)/(highP)
		qnty = int(qnty)  #0.1 to simulate real life with $40k as buffer for margin.

		orderPlaced = 0
	

		
		if action == 'sell': #originally buy
			buyP = price
			targetP = 0
			if voltV >= 3:
				targetP = round(buyP *(100+0.1*abs(voltV)+0.1*abs(trendV))/100,2)
			else:			
				targetP = round(buyP * 1.0021,2)			
			stopLoss = buyP * 0.998
			print ("Placed buy order ", buyP, targetP, stopLoss,qnty)
			print ("Placed buy order ", buyP, targetP, stopLoss,qnty,file=other)
			print ("Placed buy order ", buyP, targetP, stopLoss,qnty,file=trade)
			try:
				order = api.submit_order(
			    symbol=sym,
			    qty=qnty,
			    side='buy',
			    type='limit',
			    limit_price = buyP,
			    order_class = 'bracket',
			    time_in_force = 'day',
			   		 	
			    take_profit=dict(
	    				limit_price = targetP
	  				),
			    stop_loss= dict(
	    stop_price = stopLoss,
	    limit_price = stopLoss
	  		))
			except:
				print(sys.exc_info())
				print(sys.exc_info(),file=trade)
				print(sys.exc_info(),file=other)
				tim = Timer(15.0,newTrade)
				tim.start()		
			orderPlaced = 1
			

		elif action == 'buy': #originally sell
			#print ("no buying permitted due to market conditions")			
			""" no buying permitted due to market conditions """
			sellP = price
			targetP = 0
			if voltV >= 3:
				targetP = sellP *(100-0.1*abs(voltV)-0.1*abs(trendV))/100
			else:				
				targetP = sellP * 0.9979			
			stopLoss = sellP * 1.002
			print ("Placed sell order ", sellP, targetP, stopLoss,qnty)
			print ("Placed sell order ", sellP, targetP, stopLoss,qnty,file=other)
			print ("Placed sell order ", sellP, targetP, stopLoss,qnty,file=trade)			
			try:			
				order = api.submit_order(
			    symbol=sym,
			    qty=qnty,
			    side='sell',
			    type='limit',
			    limit_price = sellP,			
			    order_class = 'bracket',
			    time_in_force = 'day',
			    	
			    take_profit=dict(
	    				limit_price = targetP
	  				),
			    stop_loss= dict(
	    stop_price = stopLoss,
	    limit_price = stopLoss
	  		))
			except:
				print(sys.exc_info())
				tim = Timer(15.0,newTrade)
				tim.start()		
			orderPlaced = 1
		

		else:
			print ('Lack of Direction', netDir)
			print ('Lack of Direction', netDir,file=other)
			tim = Timer(15.0,newTrade)
			tim.start()

		if (orderPlaced == 1):
		    
			tim = Timer(15.0, checkOrder) 
			tim.start() 		
	else:
		print ('Lack of Trend and Voltality',trendV,voltV,file=other)
		print ('Lack of Trend and Voltality',trendV,voltV)
		tim = Timer(15.0,newTrade)
		tim.start()
	
	other.close()
	trade.close()		

tim = Timer(5.0,newTrade)
tim.start()





	



