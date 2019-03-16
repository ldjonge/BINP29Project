#!/usr/bin/python3
import sqlite3
import sys

def main():
#Reading in the query, account for input both formatted as string and otherwise
    if len(sys.argv) == 2:
        try:
            query = int(sys.argv[1]) #Check if the user entered an ID
        except ValueError:
            query = sys.argv[1].upper()
    elif len(sys.argv) > 2:
        query = " ".join(sys.argv[1:]).upper()
    else:
        print("Please define a taxon to search")
        return

    connection = sqlite3.connect("tax.db")
    crsr = connection.cursor()

    taxonPath = []
    #Finding the query:
    if type(query) == str:
        sqlCommand = """SELECT ID FROM names WHERE upper(altName) = '{}';""".format(query)
        crsr.execute(sqlCommand)
        try:
            ID = crsr.fetchone()[0]
        except TypeError:
            print("Query unknown, check your spelling")
            return
    else:
        ID = str(query)

    if int(ID) == 0:
        print("This name is used for multiple species, choose an alternative name for more information")
        return
    else:
        sqlCommand = """SELECT ID, parent, sciName, comName, genComName, gcID, mgcID FROM tax WHERE ID = {};""".format(ID)
        crsr.execute(sqlCommand)
        speciesInfo = crsr.fetchone()
        if speciesInfo == None:
            print("Invalid query, ID not found")
            return
        else:
            parent = int(speciesInfo[1]) #Formatted as int for testing later
            sciName = speciesInfo[2]
            comName = speciesInfo[3]
            genComName = speciesInfo[4]
            gcID = speciesInfo[5]
            mgcID = speciesInfo[6]

        #Finding Parent sequences:
        while parent != 1 and parent !=0:  #As 1 is the root containing all organisms, all paths should lead back to 1. In case 1 is used as query, parent of 0 is also excluded.
            sqlCommand = """SELECT parent, sciName FROM tax WHERE ID = {};""".format(str(parent))
            crsr.execute(sqlCommand)
            speciesInfo = crsr.fetchone()
            if len(taxonPath)%4 == 0:
                taxonPath.insert(0, "\n\t\t{}".format(speciesInfo[1]))
            else:
                taxonPath.insert(0, speciesInfo[1])
            parent = int(speciesInfo[0])

        #Printing output
        print("Taxon ID:\t\t\t{}".format(ID))
        print("Scientific Name:\t\t{}".format(sciName))
        if comName:
            print("Common Name:\t\t\t{}".format(comName))
        if genComName:
            print("Genbank Common Name:\t\t{}".format(genComName))
        if gcID:
            print("Genetic Code:\t\t\t{}".format(gcID))
        if mgcID:
            print("Mitochondrial Genetic Code:\t{}".format(mgcID))
        print("Lineage:\t{}".format("; ".join(taxonPath)))

if __name__ == '__main__':
    main()
