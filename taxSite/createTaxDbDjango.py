#!/usr/bin/python3
from django.db import models
from taxInfo.models import Tax, Names

#Adding each entry to the ID database
def writeEntry(entryDict):
    dictKeys = sorted(entryDict.keys())
    values = []
    for i in dictKeys:
        if type(entryDict[i]) == str:
            values.append("{}={}".format(i, entryDict[i]))
        else:
            values.append("{}={}".format(i, str(entryDict[i])))
    entry = "tax = Tax({})".format(", ".join(values))
    exec(entry)
    tax.save()

#Making sure all strings have the same quotation marks to avoid issues importing into database
def quotationReplace(string):
    out = string.replace('"', "'")
    return out

#Creating dictionary with names
def addNewName(name, nameDict, idNumber):
    if name not in nameDict.keys():
        nameDict[name] = idNumber
    else:
        nameDict[name] = 0 #If a name is found for multiple species it is not useful for the search

#Inserting data into table
with open(sys.argv[1], 'r') as data:
    entry = {}
    altNames = {}
    alternatives = ["SYNONYM", "INCLUDES", "MISSPELLING", "ACRONYM", "ANAMORPH", "BLAST NAME", "EQUIVALENT NAME", "GENBANK ACRONYM", "GENBANK ANAMORPH", "GENBANK SYNONYM", "IN-PART", "MISNOMER", "TELEOMORPH"]
    for line in data:
        line = line.strip()
        if line == "//":
            #Add entry into table
            sqlCommand = writeEntry(entry)
            crsr.execute(sqlCommand)
            entry = {}
        else:
            line = line.split(":")
            if line[0].strip() == "ID":
                entry["idNumber"] = int(line[1].strip())
            elif line[0].strip() == "PARENT ID":
                entry["parent"] = int(line[1].strip())
            elif line[0].strip() == "RANK":
                entry["rank"] = quotationReplace(line[1].strip())
            elif line[0].strip() == "GC ID":
                entry["gcID"] = int(line[1].strip())
            elif line[0].strip() == "MGC ID":
                entry["mgcID"] = int(line[1].strip())
            elif line[0].strip() == "SCIENTIFIC NAME":
                name = quotationReplace(line[1].strip())
                entry["sciName"] = name
                addNewName(name, altNames, entry["idNumber"])
            elif line[0].strip() == "GENBANK COMMON NAME":
                name = quotationReplace(line[1].strip())
                entry["genComName"] = name
                addNewName(name, altNames, entry["idNumber"])
            elif line[0].strip() == "COMMON NAME":
                name = quotationReplace(line[1].strip())
                entry["comName"] = name
                addNewName(name, altNames, entry["idNumber"])
            elif line[0].strip() in alternatives:
                name = quotationReplace(line[1].strip())
                addNewName(name, altNames, entry["idNumber"])

for name in altNames.keys():
    entry = Names(altName=name, idNumber=altNames[name])
    entry.save()
