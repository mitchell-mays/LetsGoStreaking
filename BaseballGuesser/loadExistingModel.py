import sys
import numpy as np
sys.path.insert(0, '/media/storage/Projects/ML_SuperPower/')
import FeedForwardNeuralNetwork as FFNN
import preprocessing as pp

##################################################
##################################################
####      Test Restore Predict Models         ####
##################################################
##################################################
SETNAME = "output_2010-2017.csv"
proc = pp.preprocessor()
proc.load(datafile="processedData/" + SETNAME)

NN = FFNN.FFNN()


procTemp = pp.preprocessor()
procTemp.data.append(proc.data[0].copy())
procTemp.drop(conditionString="df[\"Batter\"] != \"Jose Altuve\"")

procTemp.drop(["Batter","Date_1", "Pitcher","Weather","Class"], axis=1)

dropCol = []
for col in procTemp.data[0].columns:
    if "Unnamed" in col:
        dropCol.append(col)

if (len(dropCol) > 0):
    procTemp.drop(dropCol, axis=1)

procTemp.makeNumeric(classThreshold=8)
procTemp.makeOutput("Label")
procTemp.equalizeSubsets()
procTemp.normalizeColumns()




data, labels = procTemp.getDataAndLabels()

print(NN.restoreTF('models/Jose_Altuve', data, labels))

#print(NN.test(data, labels))
