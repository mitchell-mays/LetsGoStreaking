#import visualizeNet as vis
import os
import pandas as pd
import sys
sys.path.insert(0, '/media/storage/Projects/ML_SuperPower/')
import preprocessing as pp
import FeedForwardNeuralNetwork as FFNN
import time



#SETNAME = "output_2010-2017.csv"
SETNAME = "output_2010-2018.csv"
TRAINNAME = "output_2010-2018_train.csv"
TESTNAME = "output_2010-2018_test.csv"

proc = pp.preprocessor()
years = ["2010","2011","2012","2013","2014","2015","2016","2017","2018"]

for year in years:
    proc.load(datafile="data/output_" + year + ".csv")

proc.merge(trust=True)

#########################################################
#General Cleanup
#########################################################
#########################################################

#Regex for parsing weather values
#Get wind speed
proc.data[0]["Wind"] = proc.data[0]["Weather"].str.extract('Wind (\d*)')
proc.cleanNumeric(columns=["Wind"])

#Get temp in degrees F
proc.data[0]["Temp"] = proc.data[0]["Weather"].str.extract('(\d*)&deg')
proc.cleanNumeric(columns=["Temp"])

#Get weather type
proc.data[0]["Sky"] = proc.data[0]["Weather"].str.extract('(Dome|Drizzle|Rain|Overcast|Cloudy|Sunny)')

#Split hits/no hits
proc.addColumnFromData("Label", "df[\"Class\"] > 0")

#map day/month/year
proc.splitColumns(columns=["Date"], delim=',', expectedColumns=3, errLeft=True)
proc.addColumnFromData("Date", "df[\"Date_1\"] + \",\" + df[\"Date_2\"].map(str)")
proc.cleanNumeric(columns=["Date"])

#Drop mistaken Time values
proc.drop(conditionString="df[\"Time\"] == \"Game\"")
proc.drop(conditionString="df[\"Time\"] == \"First\"")
proc.drop(conditionString="df[\"Time\"] == \"Logos\"")
proc.drop(conditionString="df[\"Time\"] == \"Video\"")

#Drop ill fit data (less than 50 ABs or less than 10 IP)
proc.drop(conditionString="df[\"AB\"] < 50")
proc.drop(conditionString="df[\"IP\"] < 10")

#Drop NAs
proc.data[0] = proc.data[0].dropna(axis=0, how='any')


#Split into train and test sets
#train set will be used to train base AND ensemble models
#test will be final outcome test


dfsTrain = []
dfsTest = []
for year in years:
    procTemp = pp.preprocessor()
    procTemp.data.append(proc.data[0].copy())
    procTemp.drop(conditionString="df[\"Date_2\"].astype('int64') != " + year)
    procTemp.shuffle()
    dfTrain = procTemp.data[0].head(n=(round((len(procTemp.data[0])/8)*7)))
    print(len(dfTrain))
    dfTest = procTemp.data[0][len(dfTrain)+1:]
    print(len(dfTest))

    dfsTrain.append(dfTrain)
    dfsTest.append(dfTest)

proc.data = []
procTest = pp.preprocessor()

for year in range(len(dfsTrain)):
    proc.data.append(dfsTrain[year])
    procTest.data.append(dfsTest[year])

proc.merge(trust=True)
procTest.merge(trust=True)
print(len(proc.data[0]))
print(len(procTest.data[0]))

proc.data[0].to_csv("processedData/"+TRAINNAME)
procTest.data[0].to_csv("processedData/"+TESTNAME)
