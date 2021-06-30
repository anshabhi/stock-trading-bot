def volumeFn (Iname,val):
	#print(Iname,val[0])
	if (Iname == 'adi'):
		if (val[0] < -0.5):
			return -1 #fall
		elif (val[0] > 0.5):
			return 1 #rise
		else:					#Acting as leading indicator of price movements.
			return 0 #neutral
	elif (Iname == 'cmf'):
		if (val[0] < -0.5):
			return -1 #fall
		elif (val[0] > 0.5):
			return 1 #rise		#It measures the amount of Money Flow Volume over a specific period.
		else:			
			return 0 #neutral
	elif (Iname == 'em'):
		if (val[0] < -0.5):
			return -1 #fall
		elif (val[0] > 0.5):
			return 1 #rise		It relate an asset’s price change to its volume and is particularly useful for assessing the strength of a trend.
		else:			
			return 0 #neutral
	elif (Iname == 'fi'):
		if (val[0] < 0):
			return -1 #fall
		elif (val[0] > 0):	#High positive values mean there is a strong rising trend, and low values signify a strong downward trend.
			return 1 #rise
		else:
			return 0 #neutral
	elif (Iname == 'mfi'):
		if (val[0] < 45):
			return -1 #fall
		elif (val[0] > 55):
			return 1 #rise #mfi of <40 indicates fall and >60 indicates rise. 
		else:
			return 0 #neutral
	elif (Iname == 'nvi'):
		if (val[0] < val[45]):
			return -1 #fall
		elif (val[0] > val[45]): #compare nvi 0 with nvi of 45 periods back for breakout trend
			return 1 #rise
		else:
			return 0 #neutral
	elif (Iname == 'obv'):
		if (val[0] < -45):
			return -1 #fall
		elif (val[0] > 55):
			return 1 #rise #mfi of <40 indicates fall and >60 indicates rise. 
		else:
			return 0 #neutral
	elif (Iname == 'vpt'):
		if (val[0] < -5):
			return -1 #fall
		elif (val[0] > 5):
			return 1 #rise #mfi of <40 indicates fall and >60 indicates rise. 
		else:
			return 0 #neutral
	elif (Iname == 'sma-em'):
		if (val[0] < 0):
			return -1 #fall
		elif (val[0] > 0):	#High positive values mean there is a strong rising trend, and low values signify a strong downward trend.
			return 1 #rise
		else:
			return 0 #neutral
	else:
		return 0
	
def voltalityFn (Iname,val):
	#print(Iname,val[0])
	if (Iname == 'atr'):
		if (val[0] < 1):
			return -1 #not volatile
		elif (val[0] > 1):
			return 1 #volatile
		else:
			return 0 #neutral	#The indicator provide an indication of the degree of price volatility. Strong moves, in either direction, are often accompanied by large ranges, or large True Ranges.
	elif (Iname == 'bbw'):
		if (val[0] < 1):
			return -1 #not volatile
		elif (val[0] > 1):			#Bollinger Channel Band Width
			return 1 #volatile
		else:
			return 0 #neutral
	elif (Iname == 'dcp'):
		if (val[0] < 1):
			return -1 #not volatile
		elif (val[0] > 1):			#The upper band marks the highest price of an issue for n periods.
			return 1 #volatile
		else:
			return 0 #neutral
	elif (Iname == 'kcw'):
		if (val[0] < 0.65):
			return -1 #not volatile
		elif (val[0] > 0.65):			#Showing a simple moving average line (high) of typical price
			return 1 #volatile
		else:
			return 0 #neutral
	else:
		return 0
	
def trendFn (Iname,val):
	#print(Iname,val[0])
	if (Iname == 'atx'):
		if (val[0] < 20):
			return -1 #no trend
#The Plus Directional Indicator (+DI) and Minus Directional Indicator (-DI) are derived from smoothed averages of these differences, and measure trend direction over time. 
		elif (val[0] > 25):
			return 1 #good trend
		else:
			return 0 #neutral

	elif (Iname == 'aroon-ind'):
		if (abs(val[0]) < 20):
			return -1 # no trend
#CCI measures the difference between a security’s price change and its average price change.
		elif (abs(val[0]) < 65):
			return 1 # good trend
		else:
			return 2 # strong trend

	elif (Iname == 'cci'):
		if (abs(val[0]) < 20):
			return -1 # no trend
#The Plus Directional Indicator (+DI) and Minus Directional Indicator (-DI) are derived from smoothed averages of these differences, and measure trend direction over time. 
		elif (abs(val[0]) < 150):
			return 1 # good trend
		else:
			return 2 # strong trend

	elif (Iname == 'dpo'):
		if (abs(val[0]) < 1):
			return -1 # no trend
#The Plus Directional Indicator (+DI) and Minus Directional Indicator (-DI) are derived from smoothed averages of these differences, and measure trend direction over time. 
		elif (abs(val[0]) < 1.8):
			return 1 # good trend
		else:
			return 2 # strong trend

	else:
		return 0

def momentumFn (Iname,val, close):
	#print(Iname,val[0])
	if (Iname == 'ao'):
		lastVal = val[0]
		prevSum = val.sum() - lastVal
		if (lastVal < 0 and prevSum > 0):
			return -1
		elif (lastVal > 0 and prevSum > 0):
			return 0		#The Awesome Oscillator is an indicator used to measure market momentum.
		elif (lastVal < 0 and prevSum < 0): 	
			return 0
		elif (lastVal > 0 and prevSum < 0):
			return 1
		else:
			return 0
	elif (Iname == 'kama'):
		if (close[0] < val[0]):
			return -1
		elif (close[0] > val[0]):		#Moving average designed to account for market noise or volatility.
			return 1
		else:
			return 0

	elif (Iname == 'roc'):
		if (val[0] < -0.8):
			return -2
		elif (val[0] < -0.1):		#Moving average designed to account for market noise or volatility.
			return -1
		elif (val[0] > 0.8):
			return 2
		elif (val[0] > 0.1):
			return 1
		else:
			return 0

	elif (Iname == 'rsi'):
#Compares the magnitude of recent gains and losses over a specified time period to measure speed and change of price movements of a security. I
		if (val[0] > 60):
			return -1
		elif (val[0] < 40):
			return 1
		else:
			return 0

	elif (Iname == 'stoch'):
#The stochastic oscillator presents the location of the closing price of a stock in relation to the high and low range of the price of a stock over a period of time, typically a 14-day period.
		if (val[0] > 80):
			return -1
		elif (val[0] < 20):
			return 1
		else:
			return 0
	
	elif (Iname == 'stoch-signal'):
		if (val[0] > 80):
			return -1
		elif (val[0] < 20):
			return 1
		else:
			return 0

	elif (Iname == 'tsi'):
#Shows both trend direction and overbought/oversold conditions.

		avg = val.sum()/len(val)
		if (val[0] < avg):
			return -1
		elif (val[0] > avg):
			return 1
		else:
			return 0

	elif (Iname == 'to'):
#Compares the magnitude of recent gains and losses over a specified time period to measure speed and change of price movements of a security. I
		if (val[0] > 55):
			return 1
		elif (val[0] < 45):
			return -1
		else:
			return 0

	elif (Iname == 'wr'):
#Williams %R is a momentum indicator that is the inverse of the Fast Stochastic Oscillator.
		if (val[0] > -25):
			return -1
		elif (val[0] < -75):
			return 1
		else:
			return 0



	else:
		return 0
	

	 

			 
