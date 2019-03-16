#!/usr/bin/python3
import sqlite3
import sys

#Setting up SQL basics
connection = sqlite3.connect("tax.db")
crsr = connection.cursor()

#Creating the table
sqlCommand = """CREATE TABLE IF NOT EXISTS tax (
ID INTEGER PRIMARY KEY,
parent INTEGER,
rank VARCHAR,
sciName VARCHAR,
comName VARCHAR,
genComName VARCHAR,
gcID INTEGER,
mgcID INTEGER);"""
crsr.execute(sqlCommand)

#Table with alternative names
sqlCommand = """CREATE TABLE IF NOT EXISTS names (
altName VARCHAR,
ID INTEGER);"""
crsr.execute(sqlCommand)

#Adding each entry to the ID database
def writeEntry(entryDict):
    dictKeys = sorted(entryDict.keys())
    values = []
    for i in dictKeys:
        if type(entryDict[i]) == str:
            values.append('"{}"'.format(entryDict[i]))
        else:
            values.append(str(entryDict[i]))
    dictKeys = ", ".join(dictKeys)
    values = ", ".join(values)
    sqlCommand = """INSERT INTO tax ({})
    VALUES ({});""".format(dictKeys, values)
    return sqlCommand

#Making sure all strings have the same quotation marks to avoid issues importing into database
def quotationReplace(string):
    out = string.replace('"', "'")
    return out

#Creating dictionary with names
def addNewName(name, nameDict, ID):
    if name not in nameDict.keys():
        nameDict[name] = ID
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
                entry["ID"] = int(line[1].strip())
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
                addNewName(name, altNames, entry["ID"])
            elif line[0].strip() == "GENBANK COMMON NAME":
                name = quotationReplace(line[1].strip())
                entry["genComName"] = name
                addNewName(name, altNames, entry["ID"])
            elif line[0].strip() == "COMMON NAME":
                name = quotationReplace(line[1].strip())
                entry["comName"] = name
                addNewName(name, altNames, entry["ID"])
            elif line[0].strip() in alternatives:
                name = quotationReplace(line[1].strip())
                addNewName(name, altNames, entry["ID"])

for name in altNames.keys():
    sqlCommand = """INSERT INTO names (altName, ID)
    VALUES ("{}", {});""".format(name, str(altNames[name]))
    crsr.execute(sqlCommand)

connection.commit()
connection.close()
