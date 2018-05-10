#import visualizeNet as vis
import os
import pandas as pd
import sys
sys.path.insert(0, '/media/storage/Projects/ML_SuperPower/')
import preprocessing as pp
import FeedForwardNeuralNetwork as FFNN
import time


'''
SETNAME = "output_2010-2017.csv"

proc = pp.preprocessor()

proc.load(datafile="data/output_2010.csv")
proc.load(datafile="data/output_2011.csv")
proc.load(datafile="data/output_2012.csv")
proc.load(datafile="data/output_2013.csv")
proc.load(datafile="data/output_2014.csv")
proc.load(datafile="data/output_2015.csv")
proc.load(datafile="data/output_2016.csv")
proc.load(datafile="data/output_2017.csv")
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
proc.data[0].to_csv("processedData/"+SETNAME)
'''


##################################################
##################################################
####      Test Restore Predict Models         ####
##################################################
##################################################
SETNAME = "output_2010-2017.csv"
proc = pp.preprocessor()
proc.load(datafile="processedData/" + SETNAME)

NN = FFNN.FFNN()
NN.restoreTF('models/David_Dahl')

procTemp = pp.preprocessor()
procTemp.data.append(proc.data[0].copy())
procTemp.drop(conditionString="df[\"Batter\"] != \"David Dahl\"")

procTemp.drop(["Batter","Date_1", "Date_2", "Pitcher","Weather","Class"], axis=1)

dropCol = []
for col in procTemp.data[0].columns:
    if "Unnamed" in col:
        dropCol.append(col)

if (len(dropCol) > 0):
    procTemp.drop(dropCol, axis=1)

procTemp.makeNumeric(classThreshold=8)
procTemp.makeOutput("Label")
#procTemp.equalizeSubsets()
procTemp.normalizeColumns()

data, labels = procTemp.getDataAndLabels()
print(NN.test(data, labels))


'''
##################################################
##################################################
####      Create Batter Models on Data        ####
##################################################
##################################################
SETNAME = "output_2010-2017.csv"
proc = pp.preprocessor()
proc.load(datafile="processedData/" + SETNAME)

batterFile = open("data/2018_Batters_All.txt","r")
batterRead = batterFile.readlines()

modelAccuracyFile = open("models/ACCURACY.txt","a")
modelAccuracyFile.close()


for batterLine in batterRead:
    procTemp = pp.preprocessor()
    procTemp.data.append(proc.data[0].copy())
    procTemp.drop(conditionString="df[\"Batter\"] != \"" + batterLine[:-2] + "\"")

    if (len(procTemp.data[0]) < 10):
        continue

    procTemp.drop(["Batter","Date_1", "Date_2", "Pitcher","Weather","Class"], axis=1)
    #Optional
    #proc.drop(["BA_LG","HPP_LG", "CPAB_LG", "CPP_LG", "BA_LG_PP","HPP_LG_PP", "CPAB_LG_PP", "CPP_LG_PP"], axis=1)

    #print(procTemp.data[0])
    procTemp.makeNumeric(classThreshold=8)
    procTemp.makeOutput("Label")
    procTemp.equalizeSubsets()
    procTemp.normalizeColumns()

    #proc.drop(conditionString="df[\"Date\"] < 0.5")
    procTemp.shuffle()
    data, labels = procTemp.getDataAndLabels()
    #print(labels)
    #time.sleep(15)
    #proc.showFiles()


    # Test 1
    model = [35, 24, 24, 2]
    #model = [27, 24, 24, 2]
    #dataFile = pd.read_csv("/media/storage/Projects/PreviousPycharmProjects/BaseballGuesser/data/output_2017.csv")
    #data = dataFile.drop(dataFile.columns[len(dataFile.columns)-(model[-1]):len(dataFile.columns)], axis=1)
    #labels = dataFile[dataFile.columns[len(dataFile.columns)-(model[-1]):len(dataFile.columns)]]

    #print(data[0:100])
    #print(labels[0:100])
    NN = FFNN.FFNN(data, labels, model)
    #keep_input=1, keep_hidden=1)

    print("========================================================")
    print("========================================================")
    print("========== Batter: " + batterLine[:-2] + "  ============")
    print("========================================================")
    print("========================================================")
    print(batterLine + ": " + str(len(proc.data[0])))

    fileName = "models/" + batterLine[:-2].replace(" ","_")

    accuracy = NN.train(10000, printFreq=100, fName=fileName, save=True)
    #print(NN.train(printFreq=100, crossVal=10)
    modelAccuracyFile = open("models/ACCURACY.txt","a")
    modelAccuracyFile.write(fileName + ":" + str(accuracy) + "\r\n")
    modelAccuracyFile.close()

'''

'''
##################################################
##################################################
####     Create Pitcher Models on Data        ####
##################################################
##################################################

pitcherFile = open("data/2018_Pitchers_All.txt","r")
pitcherRead = pitcherFile.readlines()

modelAccuracyFile = open("models/ACCURACY.txt","a")
modelAccuracyFile.close()

for pitcherLine in pitcherRead:
    procTemp = pp.preprocessor()
    procTemp.data.append(proc.data[0].copy())
    procTemp.drop(conditionString="df[\"Pitcher\"] != \"" + pitcherLine[:-1] + "\"")

    if (len(procTemp.data[0]) < 10):
        print("No data")
        continue

    procTemp.drop(["Batter","Date_1", "Date_2", "Pitcher","Weather","Class"], axis=1)
    #Optional
    #proc.drop(["BA_LG","HPP_LG", "CPAB_LG", "CPP_LG", "BA_LG_PP","HPP_LG_PP", "CPAB_LG_PP", "CPP_LG_PP"], axis=1)

    #print(procTemp.data[0])
    procTemp.makeNumeric(classThreshold=8)
    procTemp.makeOutput("Label")
    procTemp.normalizeColumns()

    #proc.drop(conditionString="df[\"Date\"] < 0.5")
    procTemp.shuffle()
    data, labels = procTemp.getDataAndLabels()
    #print(labels)
    #time.sleep(15)
    #proc.showFiles()


    # Test 1
    model = [35, 24, 24, 2]
    #model = [27, 24, 24, 2]
    #dataFile = pd.read_csv("/media/storage/Projects/PreviousPycharmProjects/BaseballGuesser/data/output_2017.csv")
    #data = dataFile.drop(dataFile.columns[len(dataFile.columns)-(model[-1]):len(dataFile.columns)], axis=1)
    #labels = dataFile[dataFile.columns[len(dataFile.columns)-(model[-1]):len(dataFile.columns)]]

    #print(data[0:100])
    #print(labels[0:100])
    NN = FFNN.FFNN(data, labels, model)
    #keep_input=1, keep_hidden=1)

    print("========================================================")
    print("========================================================")
    print("========== Batter: " + pitcherLine[:-1] + "  ============")
    print("========================================================")
    print("========================================================")
    print(pitcherLine + ": " + str(len(proc.data[0])))

    fileName = "models/" + pitcherLine[:-1].replace(" ","_")

    accuracy = NN.train(10000, printFreq=100, fName=fileName, save=True)
    #print(NN.train(printFreq=100, crossVal=10)
    modelAccuracyFile = open("models/ACCURACY.txt","a")
    modelAccuracyFile.write(fileName + ":" + str(accuracy) + "\r\n")
    modelAccuracyFile.close()
'''
