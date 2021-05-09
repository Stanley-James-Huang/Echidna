import os
from os import path
import ntpath

dataDirectory = '../data'
if not path.exists(dataDirectory + "/TrainingData/data.json"):          
    outputFile = open(dataDirectory + "/data.json", "a+")
    for file in os.scandir(dataDirectory + "/TrainingData"):
        with open(file) as infile:
            for line in infile:
                outputFile.write(line)