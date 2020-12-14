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


def format_CBECI(csvfile, jsDataFile, columns, name):
    columnTuple = tuple(columns)
    csvReader = csv.DictReader(csvfile, columnTuple)
    first = True
    minRowList = []
    maxRowList = []
    guessRowList = []
    for row in csvReader:
        if first:
            first = False
            continue
        del row["Timestamp"]

        row['MAX'] = float(row['MAX'])
        row['MIN'] = float(row['MIN'])
        row['GUESS'] = float(row['GUESS'])
        date = row["Date and Time"].split('T')[0]

        year, month, day = date.split("-")
        dateFormat = "{}/{}/{}".format(day, month, year[-2:])
        row["Date and Time"] = dateFormat

        guessRowList.append({
            "Date": row["Date and Time"],
            "Estimated Consumption": row["GUESS"]
        })
        maxRowList.append({
            "Date": row["Date and Time"],
            "Maximum Consumption": row["MAX"]
        })

        minRowList.append({
            "Date": row["Date and Time"],
            "Minimum Consumption": row["MIN"]
        })

    jsDataFile.write("export const " + name + "Estimated = [\n")
    for row in guessRowList[::-1]:
        json.dump(row, jsDataFile)
        jsDataFile.write(',\n')
    jsDataFile.write("];\n\n")

    jsDataFile.write("export const " + name + "Minimum = [\n")
    for row in minRowList[::-1]:
        json.dump(row, jsDataFile)
        jsDataFile.write(',\n')
    jsDataFile.write("];\n")
    
    jsDataFile.write("export const " + name + "Maximum = [\n")
    for row in maxRowList[::-1]:
        json.dump(row, jsDataFile)
        jsDataFile.write(',\n')
    jsDataFile.write("];\n")
    jsDataFile.close()
    csvfile.close()

csvfiles = ["BECI.csv", "EECI.csv", "CBECI.csv"]
jsDataFiles = ["BECI.js", "EECI.js", "CBECI.js"]
names = ["BECI", "EECI", "CBECI"]

for i in range(3):
    csvfile = open(csvfiles[i],'r')
    jsDataFile = open(jsDataFiles[i],'w')
    pdCSVReader = pd.read_csv(csvfiles[i])
    columns = pdCSVReader.columns
    if i == 2:
        format_CBECI(csvfile, jsDataFile, columns, names[i])
        break
    generate_js_objects(csvfile, jsDataFile, columns, names[i])



