import sys
import numpy as np
sys.path.insert(0, '/media/storage/Projects/ML_SuperPower/')
import FeedForwardNeuralNetwork as FFNN
import preprocessing as pp
import pandas as pd
import os

##################################################
##################################################
####     Create Ensemble input by running     ####
####      test data through base models       ####
##################################################
##################################################

SETNAME = "output_2010-2018_test.csv"
TRAINNAME = "ENSEMBLE_INPUT.csv"

#Below used in testing values
testFileNamePit = "data/testFilePitch.csv"
testFileNameBat = "data/testFileBat.csv"

#Load test data into preprocessor
proc = pp.preprocessor()
proc.load(datafile="processedData/" + SETNAME)


#Load all Batters and Pitchers
with open("data/2018_Batters_All.txt","r") as f:
    batterRead = f.read().splitlines()

with open("data/2018_Pitchers_All.txt","r") as f:
    pitcherRead = f.read().splitlines()


modelAccuracyFile = open("models/ACCURACY.txt","r")
modelAccuracyRead = modelAccuracyFile.readlines()
modelAccuracyFile.close()

modelAccuracies  = {}
for accLine in modelAccuracyRead:
    lineVal = accLine.split('/')[1]
    modelAccuracies[lineVal.split(':')[0].replace('_',' ')] = float(lineVal.split(':')[1])

#Create generic NN to be reused in reloading existing models
NN = FFNN.FFNN()


counter = 0
for batterLine in batterRead:
    counter+= 1

    procTemp = pp.preprocessor()
    procTemp.data.append(proc.data[0].copy())
    procTemp.drop(conditionString="df[\"Batter\"] != \"" + batterLine + "\"")
    procTemp.drop(conditionString="~df[\"Pitcher\"].isin(" + str(pitcherRead) + ")")

    if (len(procTemp.data[0]) <= 0):
        continue

    dropCol = []
    for col in procTemp.data[0].columns:
        if "Unnamed" in col:
            dropCol.append(col)

    if (len(dropCol) > 0):
        procTemp.drop(dropCol, axis=1)

    #print(procTemp.data[0].head(n=5))
    #pitcherColumn = procTemp.data[0]["Pitcher"]
    uniqueColumn = procTemp.data[0]["Pitcher"].str.cat(procTemp.data[0]["Batter"], sep='|').str.cat(procTemp.data[0]["Date_1"], sep='|').str.cat(procTemp.data[0]["Date_2"].astype("str"), sep='|')
    labelColumn = procTemp.data[0]["Label"]
    procTemp.drop(["Batter","Date_1", "Pitcher","Weather","Class"], axis=1)
    procTemp.makeNumeric(columns=["Time", "Sky", "Label", "Date_0"], loadPath="preprocessMeta/LabelEncoders/Batter_" + batterLine + "_")
    procTemp.makeOutput("Label")
    procTemp.normalizeColumns(loadFile="preprocessMeta/Batter_"+batterLine)
    #will need to separate train and test before normalizing
    #print(procTemp.data[0].head(n=5))
    data, labels = procTemp.getDataAndLabels()

    if (not os.path.isfile('models/' + batterLine.replace(" ","_") + ".model")) or (not batterLine in modelAccuracies):
        print("No model found for: " + batterLine)
        continue

    rawOuts = NN.restoreTF('models/' + batterLine.replace(" ","_"), data, labels)
    #temp2 = np.argmax(rawOuts, axis=1) == labels
    #print("==================================================")
    #print(np.mean(np.argmax(labels, axis=1) == np.argmax(rawOuts, axis=1)))
    #print("==================================================")

    #include accuracy of batter model as data point, repeat for all points
    modelAcc = modelAccuracies[batterLine]
    modelAccCol = np.repeat(modelAcc, len(uniqueColumn))
    #print(counter)

    if counter == 1:
        allValues = pp.preprocessor()
        allValues.data.append(pd.DataFrame(rawOuts))
        #allValues.data[0]["Pitcher"] = pitcherColumn.values
        allValues.data[0]["Unique"] = uniqueColumn.values
        allValues.data[0]["Label"] = labelColumn.values
        allValues.data[0]["BatterModelAcc"] = modelAccCol
    else:
        temp = pd.DataFrame(rawOuts)
        #temp["Pitcher"] = pitcherColumn.values
        temp["Unique"] = uniqueColumn.values
        temp["Label"] = labelColumn.values
        temp["BatterModelAcc"] = modelAccCol
        allValues.data[0] = allValues.data[0].append(temp)


allValues.data[0].to_csv(testFileNameBat)


counter = 0
for pitcherLine in pitcherRead:
    counter+= 1

    procTemp = pp.preprocessor()
    procTemp.data.append(proc.data[0].copy())
    procTemp.drop(conditionString="df[\"Pitcher\"] != \"" + pitcherLine + "\"")
    procTemp.drop(conditionString="~df[\"Batter\"].isin(" + str(batterRead) + ")")

    if (len(procTemp.data[0]) <= 0):
        continue

    dropCol = []
    for col in procTemp.data[0].columns:
        if "Unnamed" in col:
            dropCol.append(col)

    if (len(dropCol) > 0):
        procTemp.drop(dropCol, axis=1)

    #pitcherColumn = procTemp.data[0]["Pitcher"]
    uniqueColumn = procTemp.data[0]["Pitcher"].str.cat(procTemp.data[0]["Batter"], sep='|').str.cat(procTemp.data[0]["Date_1"], sep='|').str.cat(procTemp.data[0]["Date_2"].astype("str"), sep='|')
    procTemp.drop(["Batter","Date_1", "Pitcher","Weather","Class"], axis=1)
    procTemp.makeNumeric(columns=["Time", "Sky", "Label", "Date_0"], loadPath="preprocessMeta/LabelEncoders/Pitcher_" + pitcherLine + "_")
    procTemp.makeOutput("Label")
    procTemp.normalizeColumns(loadFile="preprocessMeta/Pitcher_"+pitcherLine)
    #will need to separate train and test before normalizing
    #print(procTemp.data[0].head(n=5))
    data, labels = procTemp.getDataAndLabels()

    if not os.path.isfile('models/' + pitcherLine.replace(" ","_") + ".model")  or (not pitcherLine in modelAccuracies):
        print("No model found for: " + pitcherLine)
        continue

    rawOuts = NN.restoreTF('models/' + pitcherLine.replace(" ","_"), data, labels)

    #include accuracy of batter model as data point, repeat for all points
    modelAcc = modelAccuracies[pitcherLine]
    modelAccCol = np.repeat(modelAcc, len(procTemp.data[0]))
    #print(counter)

    if counter == 1:
        allPitch = pp.preprocessor()
        allPitch.data.append(pd.DataFrame(rawOuts))
        allPitch.data[0]["Unique"] = uniqueColumn.values
        #allPitch.data[0]["Pitcher"] = pitcherColumn.values
        allPitch.data[0]["PitcherModelAcc"] = modelAccCol
    else:
        temp = pd.DataFrame(rawOuts)
        #temp["Pitcher"] = pitcherColumn.values
        temp["Unique"] = uniqueColumn.values
        temp["PitcherModelAcc"] = modelAccCol
        allPitch.data[0] = allPitch.data[0].append(temp)

allPitch.data[0].to_csv(testFileNamePit)

allValues.data[0] = allValues.data[0].set_index('Unique').join(allPitch.data[0].set_index('Unique'), lsuffix='_b', rsuffix='_p')

allValues.data[0] = allValues.data[0].dropna(axis=0, how='any')
allValues.data[0].to_csv("processedData/"+TRAINNAME)
