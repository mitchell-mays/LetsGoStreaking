#import visualizeNet as vis
import os
import pandas as pd
import sys
sys.path.insert(0, '/media/storage/Projects/ML_SuperPower/')
import preprocessing as pp
import FeedForwardNeuralNetwork as FFNN
import time


#SETNAME = "output_2010-2017.csv"
SETNAME = "ENSEMBLE_INPUT.csv"
proc = pp.preprocessor()
proc.load(datafile="processedData/" + SETNAME)

dropCol = []
for col in proc.data[0].columns:
    if "Unnamed" in col:
        dropCol.append(col)

if (len(dropCol) > 0):
    proc.drop(dropCol, axis=1)

proc.data[0] = proc.data[0].dropna(axis=0, how='any')
proc.drop(["Pitcher"], axis=1)
proc.shuffle()

'''
procTemp = pp.preprocessor()
procTemp.data.append(proc.data[0].copy())

split = round((len(proc.data[0])/10)*9)
proc.data[0] = proc.data[0][:split]
procTemp.data[0] = procTemp.data[0][split + 1:]
procTemp.makeOutput("Label")
procTemp.equalizeSubsets()
procTemp.normalizeColumns()
'''

##################################################
##################################################
####      Create Ensemble Model on Data        ####
##################################################
##################################################

proc.makeOutput("Label")
proc.equalizeSubsets()
proc.normalizeColumns()



#trainData, trainLabels = proc.getDataAndLabels(regression=True)
trainData, trainLabels = proc.getDataAndLabels()
#testData, testLabels = procTemp.getDataAndLabels()



# Test 1
model = [6, 4, 4, 2]
#model = [6, 4, 4, 1]


#print(data[0:100])
#print(labels[0:100])
NN = FFNN.FFNN(trainData, trainLabels, model)
#keep_input=1, keep_hidden=1)

print("========================================================")
print("========================================================")
print("====================== Ensemble  =======================")
print("========================================================")
print("========================================================")
print("Ensemble: " + str(len(proc.data[0])))

fileName = "models/Ensemble"

accuracy = NN.train(10000, printFreq=1, fName=fileName, save=True)


#Commented out for test. REVERT AFTER TEST!!!!!!
print(accuracy)
