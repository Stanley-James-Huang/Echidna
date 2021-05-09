import requests
import json
import time
import pycritter
from pathlib import Path
from os import path

bestiaries = open("bestiaries.txt", "r")
dataDirectory = '../data'
while True:
    # get next bestiary to read
    bestiaryId = bestiaries.readline().rstrip('\n') 

    # if line is empty
    # end of file is reached
    if not bestiaryId:
        break
    
    bestiaryJSON = pycritter.get_published(bestiaryId)
    bestiaryName = bestiaryJSON["name"].replace(" ", "_").replace("/", "_")
    page = 1
    while True:
        time.sleep(0.5) #be polite, wait a little between requests!
        result = pycritter.get_published_creatures(bestiaryId, page)
        if not result:
            break
        if path.exists(dataDirectory + "/RawBestiaries" + bestiaryName + str(page) + ".txt"):
            break
        file = open(dataDirectory + "/RawBestiaries" + bestiaryName + str(page) + ".txt", "a+")
        for creature in result:
            #file.write("<|startoftext|>\n" + json.dumps(creature, indent=4) + "\n<|endoftext|>\n") #hack to pretty print the creatures
            file.write(json.dumps(creature) + '\n')
        file.close()
        page += 1
    
