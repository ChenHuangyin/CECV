import csv
import json
import pandas as pd

def generate_js_objects(csvfile, jsDataFile, columns, name):
    columnTuple = tuple(columns)
    csvReader = csv.DictReader(csvfile, columnTuple)
    first = True
    estimatedRowList = []
    minimumRowList = []
    for row in csvReader:
        if first:
            first = False
            continue
        if row['Minimum TWh per Year'] == '#DIV/0!':
            row['Minimum TWh per Year'] = minimumRowList[-1]['Minimum TWh per Year']
        row['Estimated TWh per Year'] = float(row['Estimated TWh per Year'])
        row['Minimum TWh per Year'] = float(row['Minimum TWh per Year'])
        date = row["Date"]
        year, month, day = date.split("/")
        if int(month) < 10:
            month = '0' + month
        dateFormat = "{}/{}/{}".format(day, month, year[-2:])
        row["Date"] = dateFormat


        estimatedRowList.append({
            "Date": row["Date"],
            "Estimated TWh per Year": row["Estimated TWh per Year"]
        })
        minimumRowList.append({
            "Date": row["Date"],
            "Minimum TWh per Year": row["Minimum TWh per Year"]
        })
        
    jsDataFile.write("export const " + name + "Estimated = [\n")
    for row in estimatedRowList[::-1]:
        json.dump(row, jsDataFile)
        jsDataFile.write(',\n')
    jsDataFile.write("];\n\n")

    jsDataFile.write("export const " + name + "Minimum = [\n")
    for row in minimumRowList[::-1]:
        json.dump(row, jsDataFile)
        jsDataFile.write(',\n')
    jsDataFile.write("];\n")

    jsDataFile.close()
    csvfile.close()

csvfiles = ["BECI.csv", "EECI.csv"]
jsDataFiles = ["BECI.js", "EECI.js"]
names = ["BECI", "EECI"]

for i in range(2):
    csvfile = open(csvfiles[i],'r')
    jsDataFile = open(jsDataFiles[i],'w')
    pdCSVReader = pd.read_csv(csvfiles[i])
    columns = pdCSVReader.columns
    generate_js_objects(csvfile, jsDataFile, columns, names[i])
