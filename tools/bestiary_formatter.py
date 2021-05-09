import os
from os import path
import json
import ntpath
import math

from collections import OrderedDict 

creature_order = [
    "name",
    {
        "flavor" :
        [
            "description",
            "nameIsProper"
        ]
    },
    {
        "stats" :
        [
            "size",
            "race",
            "alignment",
            "armorType",
            "armorClass",
            "numHitDie",
            "speed",
            {
                "abilityScores" : [
                    "strength",
                    "dexterity",
                    "constitution",
                    "intelligence",
                    "wisdom",
                    "charisma"
                ],
            },
            "proficiencyBonus",
            "damageVulnerabilities",
            "damageResistances",
            "damageImmunities",
            "conditionImmunities",
            "senses",
            "languages",
            "challengeRating",
            "experiencePoints",
            "legendaryActionsPerRound",
            "legendaryActionsDescription",
            "savingThrows",
            "skills",
            "additionalAbilities",
            "actions",
            "reactions",
            "legendaryActions",
            "hitDieSize"
        ]
    }
]

def cleanSymbols(creatureJSON):
    for key, value in creatureJSON.items():
        if isinstance(value, dict):
            cleanSymbols(value)
        elif isinstance(value, str):
            creatureJSON[key].replace('\\n', '\n')
            creatureJSON[key].replace('\\u2022', '•')
        
        
# Filters out useless fields in the JSON
# Reorders existing fields to be where we want them
def filterJSON(creatureJSON):
    del creatureJSON["_id"]
    del creatureJSON["publishedBestiaryId"]
    del creatureJSON["__v"]
    del creatureJSON["sharing"]
    del creatureJSON["flavor"]["faction"]
    del creatureJSON["flavor"]["imageUrl"]
    del creatureJSON["flavor"]["environment"]

def reorderAndSeedImpl(creature_order, creatureJSON, name_seed):#, abilityMods_seed):
    for entry in creature_order:
        if isinstance(entry, dict):
            for k, v in entry.items():
                creatureJSON.move_to_end(k)
                reorderAndSeedImpl(v, creatureJSON[k], name_seed)#, abilityMods_seed)
        elif isinstance(entry, str):
            if any(entry == requiresSeed for requiresSeed in ["size", "damageVulnerabilities", "reactions", "legendaryActions", "legendaryActionsDescription", "actions", "additionalAbilities"]):
                creatureJSON["name_seed_" + entry] = name_seed
                # creatureJSON["abilityMods_seed_" + entry] = abilityMods_seed
            creatureJSON.move_to_end(entry)
        else:
            creatureJSON.move_to_end(entry)

def reorderAndSeedJSON(creatureJSON):
    name_seed = creatureJSON["name"] + ", isProper={}".format(creatureJSON["flavor"]["nameIsProper"])
    #abilityMods_seed = {k : (math.floor((v - 10)/2) if v is not None else None) for (k,v) in creatureJSON["stats"]["abilityScores"].items() }
    #abilityMods_seed["proficiency"] = creatureJSON["stats"]["proficiencyBonus"]
    reorderAndSeedImpl(creature_order, creatureJSON, name_seed)#, abilityMods_seed)
    
dataDirectory = '../data'
for file in os.scandir(dataDirectory + "/RawBestiaries"):
    bestiary = open(file.path, "r")
    if path.exists(dataDirectory + "/TrainingData/" + ntpath.basename(file.path)):
        bestiary.close()
        continue
    outputFile = open(dataDirectory + "/TrainingData/" + ntpath.basename(file.path), "a+")
    while True:
        creature = bestiary.readline().rstrip('\n') 
        if not creature:
            break
        # convert to Ordereddict 
        creatureJSON = json.loads(creature, object_pairs_hook=OrderedDict)

        filterJSON(creatureJSON)
        #cleanSymbols(creatureJSON)
        reorderAndSeedJSON(creatureJSON)

        outputFile.write("<-|start|->\n" + json.dumps(creatureJSON, sort_keys=False, indent=4) + "\n<-|end|->\n")
    bestiary.close()
    outputFile.close()
