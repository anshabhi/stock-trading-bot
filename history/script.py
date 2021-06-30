import pandas as pd
import numpy as np
import math
from datetime import datetime
from dateutil import parser
import csv
import urllib2
import sys

import pytz 

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=NSE:RELIANCE&interval=1min&datatype=csv&outputsize=full&apikey=W8L7PK09ZI5N4RJ9'
response = urllib2.urlopen(url)
#cr = csv.reader(response)
dfP = pd.read_csv(response)

old_timezone = pytz.timezone("US/Eastern")
new_timezone = pytz.timezone("Asia/Kolkata")
dfP = dfP[0:400]
dfP = dfP.iloc[::-1]

for i in range(0,len(dfP)):
	dfP['timestamp'][i] = str(old_timezone.localize(pd.to_datetime(dfP['timestamp'][i])).astimezone(new_timezone))

	#print(old_timezone.localize(dfP[i].timestamp).astimezone(new_timezone))

#print(dfP[dfP.timestamp >= '2020-03-20'])	
#sys.exit("Done Executing")
#df = pd.read_csv('nifty-12-19.csv')
#df.loc[df['date'] == '20190101']
#print(dfP.tail())
#dfP = pd.read_csv('2020-JAN-NIFTY.csv')

df = pd.read_hdf('StockMarketData_2020-02-14.h5', key='/RELIANCE__EQ__NSE__NSE__MINUTE')
#df = pd.read_hdf('reliance.h5', key='data')

#df['date'] = [d.date().strftime("%Y-%m-%d") for d in df.index]
#df['time'] = [d.time().strftime("%H-%M-%S") for d in df.index]
#df.to_hdf('reliance.h5','data')
#print(df.head())
bestDate1 = 0
bestDate2 = 0
bestDate3 = 0

maxDist = 100;
maxDistP = 10000;
maxDistN = -10000;
diffArr = {};

diff = 100
diff2 = 200
diff3 = 300
#df = df[df.time > '12:00']
#dfP = dfP[dfP.time > '12:00']
nobs = 200

valuesP = dfP[dfP.timestamp >= '2020-03-20']['open'].to_numpy()
#print(valuesP[0])
openV = valuesP[0]
valuesP = np.divide(valuesP,openV)
valuesO = valuesP;

valuesP = valuesP[1:nobs]
for date in df['date'].unique()[0:400]:
	values = df[df.date == date]['open'].to_numpy()
	if (len(values) > nobs):
		openVO = values[0]
		#openVO = openVO * 100
		values = np.divide(values,openVO)
		values = values[1:nobs]
		#cos_sim = np.dot(valuesP, values)/(np.linalg.norm(valuesP)*np.linalg.norm(values))
		diffArr = valuesP - values;
		#diffPc = diffArr[diffArr > 0].sum() # your desired result.
		#diffPc = diffPc / len(diffArr[diffArr > 0])
		#diffNc = diffArr[diffArr < 0].sum() # your desired result.
		#diffNc = diffNc * len(diffArr[diffArr < 0])		
		#diff = np.sum(np.abs(diffArr))		
		diff = np.linalg.norm(diffArr)		
		#diff = abs(diff)


		if diff < maxDist:
			maxDist = diff
			bestDate1 = date
			#maxDistP = diffPc
			#maxDistN = diffNc
		#if diffPc < maxDistP and diffPc > 0:
		#	maxDistP = diffPc
		#	bestDate2 = date
			#print(maxDistP)
		#if diffNc > maxDistN and diffNc < 0:
		#	maxDistN = diffNc
		#	bestDate3 = date
			#print("maxDistN:",maxDistN)
		#elif diff < diff2:
		#	diff3 = diff2
		#	diff2 = diff
		#	bestDate3 = bestDate2
		#	bestDate2 = date


print ('Closest Date 1 is:', bestDate1, " Distance is:", maxDist)
#print('Pos Diff: ' , maxDistP, " Neg Diff: " , maxDistN)
print ('Predicting Prices for Rest of the Day:')
values = df[df.date == bestDate1][['open','time']].to_numpy()	
#print(openV)
for i in range (nobs,len(values),10):
	print("Time: " , values[i][1], " Prediction: " , openV*values[i][0]/values[0][0], " Actual Price:", valuesO[i]*openV, " Difference:", valuesO[i]*openV-openV*values[i][0]/values[0][0])

#print ('Closest Date 2 is:', bestDate2, " Distance is:", diff2 )#, " Positive Distance is:", maxDistP)
#print ('Predicting Prices for Rest of the Day:')
#values = df[df.date == bestDate2][['open','time']].to_numpy()	

#for i in range (nobs,len(values),10):
#	print("Time: " , values[i][1], " Prediction: " , openV*values[i][0]/values[0][0], " Actual Price:", valuesO[i]*openV, " Difference:", valuesO[i]*openV-openV*values[i][0]/values[0][0])

#print ('Closest Date 3 is:', bestDate3, " Distance is:", diff3)#, " Negative Distance is:", maxDistN)
#print ('Predicting Prices for Rest of the Day:')
#values = df[df.date == bestDate3][['open','time']].to_numpy()	
#for i in range (nobs,len(values),10):
#	print("Time: " , values[i][1], " Prediction: " , openV*values[i][0]/values[0][0], " Actual Price:", valuesO[i]*openV, " Difference:", valuesO[i]*openV-openV*values[i][0]/values[0][0])

#maxSim is actually distance here, which needs to be minimized
