#import visualizeNet as vis
import os
import pandas as pd
import sys
sys.path.insert(0, '/media/storage/Projects/ML_SuperPower/')
import preprocessing as pp
import FeedForwardNeuralNetwork as FFNN
import time


#Load Train data into preprocessor
SETNAME = "output_2010-2018_train.csv"
proc = pp.preprocessor()
proc.load(datafile="processedData/" + SETNAME)


with open("data/2018_Batters_All.txt","r") as f:
    batterRead = f.read().splitlines()

with open("data/2018_Pitchers_All.txt","r") as f:
    pitcherRead = f.read().splitlines()


#Drop index Column
dropCol = []
for col in proc.data[0].columns:
    if "Unnamed" in col:
        dropCol.append(col)

if (len(dropCol) > 0):
    proc.drop(dropCol, axis=1)


with open("models/ACCURACY.txt","r") as f:
    ACCValues = f.read().splitlines()

'''
alreadyCaptured = {}
for accVal in ACCValues:
    print(accVal.split("/")[1].split(":")[0])
    alreadyCaptured[accVal.split("/")[1].split(":")[0]] = 1
'''


##################################################
##################################################
####      Create Batter Models on Data        ####
##################################################
##################################################
for batterLine in batterRead:
    #if batterLine.replace(" ", "_") in alreadyCaptured:
    #    continue

    procTemp = pp.preprocessor()
    procTemp.data.append(proc.data[0].copy())
    #Drop all rows except current batter
    procTemp.drop(conditionString="df[\"Batter\"] != \"" + batterLine + "\"")

    #Drop all rows that are do not meet Pitcher Criteria (pitching in 2018)
    procTemp.drop(conditionString="~df[\"Pitcher\"].isin(" + str(pitcherRead) + ")")

    #If less then 10 rows, do not create a model
    if (len(procTemp.data[0]) < 10):
        continue

    #Drop Meta data
    procTemp.drop(["Batter","Date_1", "Pitcher","Weather","Class"], axis=1)

    #Preprocess
    procTemp.makeNumeric(columns=["Time", "Sky", "Label", "Date_0"], savePath="preprocessMeta/LabelEncoders/Batter_" + batterLine + "_")
    procTemp.makeOutput("Label")
    procTemp.equalizeSubsets()
    procTemp.normalizeColumns(saveFile="preprocessMeta/Batter_" + batterLine)
    procTemp.shuffle()

    #Get into NN compatible Data and Labels
    data, labels = procTemp.getDataAndLabels()


    #Create Deep Neural Net to fit specs
    model = [36, 24, 24, 2]
    NN = FFNN.FFNN(data, labels, model)


    print("========================================================")
    print("========================================================")
    print("========== Batter: " + batterLine + "  ============")
    print("========================================================")
    print("========================================================")
    print(batterLine + ": " + str(len(proc.data[0])))

    fileName = "models/" + batterLine.replace(" ","_")

    accuracy = NN.train(10000, crossVal=0, printFreq=100, fName=fileName, save=True)

    modelAccuracyFile = open("models/ACCURACY.txt","a")
    modelAccuracyFile.write(fileName + ":" + str(accuracy) + "\r\n")
    modelAccuracyFile.close()



##################################################
##################################################
####     Create Pitcher Models on Data        ####
##################################################
##################################################


for pitcherLine in pitcherRead:
    procTemp = pp.preprocessor()
    procTemp.data.append(proc.data[0].copy())
    #Drop all rows except current Pitcher
    procTemp.drop(conditionString="df[\"Pitcher\"] != \"" + pitcherLine + "\"")

    #Drop all rows that are do not meet Batter Criteria (batting in 2018)
    procTemp.drop(conditionString="~df[\"Batter\"].isin(" + str(batterRead) + ")")

    if (len(procTemp.data[0]) < 10):
        print("No data")
        continue

    procTemp.drop(["Batter","Date_1", "Pitcher","Weather","Class"], axis=1)


    procTemp.makeNumeric(columns=["Time", "Sky", "Label", "Date_0"], savePath="preprocessMeta/LabelEncoders/Pitcher_" + pitcherLine + "_")
    procTemp.makeOutput("Label")
    procTemp.normalizeColumns(saveFile="preprocessMeta/Pitcher_" + pitcherLine)
    procTemp.shuffle()
    data, labels = procTemp.getDataAndLabels()


    model = [36, 24, 24, 2]
    NN = FFNN.FFNN(data, labels, model)

    print("========================================================")
    print("========================================================")
    print("========== Pitcher: " + pitcherLine + "  ============")
    print("========================================================")
    print("========================================================")
    print(pitcherLine + ": " + str(len(proc.data[0])))

    fileName = "models/" + pitcherLine.replace(" ","_")

    accuracy = NN.train(10000, printFreq=100, crossVal=0, fName=fileName, save=True)

    modelAccuracyFile = open("models/ACCURACY.txt","a")
    modelAccuracyFile.write(fileName + ":" + str(accuracy) + "\r\n")
    modelAccuracyFile.close()
