import csv
import os

cwdPath = os.getcwd()

#function that writes a list to a csv with stain in its filename
def writeListToCSV(list, dataPath, stain, averageValue):
    with open(dataPath + "/" + stain + "Results", 'w') as csvfile:
        fileWriter = csv.writer(csvfile)
        i = 0
        for line in list:
            k = str(i)
            fileWriter.writerow([stain + k + "(microns)", line])
            i = i + 1
        fileWriter.writerow(["Average " + stain + " (microns)", averageValue])

def calculateDataForSubdir(dataPath, stain):
    cellHeightList = []
    for filename in sorted(os.listdir(dataPath)):
        #for each csv, calculate cell height (or laminin thickness)
        if filename.endswith('.csv') and "_"+stain in filename: 
            content = open(dataPath + '/' + filename, 'r')
            filteredCellHeight = []
            for row in content:
                newlist = row.split(',')
                #skip header
                if newlist[1].rstrip() == "Gray Value" or newlist[1].rstrip() == "Distance":
                    continue
                #if pixel intensity is 255, record the cell location
                if int(float(newlist[2].rstrip())) == 255:
                    filteredCellHeight.append(float(newlist[1]))
            # if len(filteredCellHeight) == 0: #let me know if any csv need to be re-done
            #     print(dataPath + filename)
            #     continue 
            #calculate cell height
            cellTop = max(filteredCellHeight) 
            cellBottom = min(filteredCellHeight)
            if cellTop == cellBottom: #let me know if there was only one detected element
                print(dataPath + filename)
                continue
            cellHeight = cellTop - cellBottom
            cellHeightList.append(cellHeight)
    #for each subdir, calculate average of all csvs
    averageCellHeight = sum(cellHeightList)/len(cellHeightList)
    writeListToCSV(cellHeightList, dataPath, stain, averageCellHeight)


#finalLamininThicknessPerChip = []

for folderName in os.listdir(cwdPath + "/Main"): #folder name = chip (eg. "Nutritive N4 T2")
    for subdirName in os.listdir(cwdPath + "/Main/"+ folderName): #subfolder = image (eg. "zstack_syringe4...001")
        dataPath = cwdPath + "/Main/"+ folderName + "/" + subdirName 
        # calculateDataForSubdir(dataPath, "lamininThickness")
        calculateDataForSubdir(dataPath, "cellHeight")

for folderName in os.listdir(cwdPath + "/Main"): 
    finalCellHeightPerChip = []
    finalCellHeightPerChip.clear()   
    #for each csv (filename in subdir), pull the average
    for subdirName in os.listdir(cwdPath+ "/Main/"+ folderName): #eg. "zstack_syringe4...001"
         for filename in sorted(os.listdir(cwdPath+ "/Main/"+ folderName + "/" +subdirName)): #eg. cellHeightResults.csv
            if "cellHeightResults" in filename:
                content = open(cwdPath+ "/Main/"+ folderName + "/" +subdirName + '/' + filename, 'r')
                for row in content:
                    newlist = row.split(',')
                    if "Average cellHeight (microns)" in newlist[0]:
                        finalCellHeightPerChip.append(float(newlist[1]))
    averageCellHeightPerChip = sum(finalCellHeightPerChip)/len(finalCellHeightPerChip)
    finalDataPath = cwdPath + "/Main/" + folderName
    writeListToCSV(finalCellHeightPerChip, finalDataPath, "finalCellHeightPerChip", averageCellHeightPerChip)  

            # if "lamininThicknessResults" in filename:
            #     content = open(dataPath + '/' + filename, 'r')
            #     for row in content:
            #         newlist = row.split(',')
            #         if "AveragelamininThickness(microns)" in newlist[0]:
            #             finalLamininThicknessPerChip.append(float(newlist[1]))
    
    #writeListToCSV(finalLamininThicknessPerChip, finalDataPath, "finalLamininThicknessPerChip", "NaN")
    #in each main folder (foldername) save final results per chip
