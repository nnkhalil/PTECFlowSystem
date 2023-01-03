import csv
import os

cwdPath = os.getcwd()
print(cwdPath)

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

#function that calculates laminin thickness from a spreadsheet with multiple peaks, stain in spreadsheet filename
def calculateDataForSubdir(dataPath, stain):
    lamininThicknessList = []
    for filename in sorted(os.listdir(dataPath)):
        filteredLamininThickness = []
        #for each csv, calculate cell height (or laminin thickness)
        if filename.endswith('.csv'): 
            content = open(dataPath + '/' + filename, 'r')
            hasFoundPeak = False 
            for row in content:
                newlist = row.split(',')
                #skip header
                if newlist[2].rstrip() == "Gray Value":
                    continue
                #if pixel intensity is non-zero, record the location
                if float(newlist[2].rstrip()) != 0:
                    filteredLamininThickness.append(float(newlist[1]))
                    hasFoundPeak = True
                if float(newlist[2].rstrip()) == 0 and hasFoundPeak == True:
                    break
            #calculate cell height
            if len(filteredLamininThickness) != 0:
                lamTop = max(filteredLamininThickness) 
                lamBottom = min(filteredLamininThickness)
                lamThickness = lamTop - lamBottom
                lamininThicknessList.append(lamThickness)
            #handle exceptions
            if len(filteredLamininThickness) == 0: 
                lamThickness = 0
                averageLamininThickness = 0
                lamininThicknessList.append(lamThickness)
        #print(*lamininThicknessList) #printed empty lists!!!!!
        #print(*filteredLamininThickness) #this printed empty list!
    averageLamininThickness = sum(lamininThicknessList)/len(lamininThicknessList)
    #for each subdir, calculate average of all csvs
    writeListToCSV(lamininThicknessList, dataPath, stain, averageLamininThickness)


#calculate laminin Thickness per IMAGE (averaging 10 ROIs) and save results to csv
for folderName in os.listdir(cwdPath + "/Main"): #folder name = chip (eg. "Nutritive N4 T2")
    for subdirName in os.listdir(cwdPath + "/Main/"+ folderName): #subfolder name = image (eg. "zstack_syringe4...001")
        newPath = cwdPath + "/Main/"+ folderName + "/" + subdirName 
        calculateDataForSubdir(newPath, "lamininThickness")
        

#calculate laminin thickness per CHIP (averaging 5 images) and save results to csv
for folderName in os.listdir(cwdPath + "/Main"): # eg. "Nutritive N4 T2"
    finalLamThicknessPerChip = []
    finalLamThicknessPerChip.clear()   
    #for each csv (filename in subdir), pull the average
    for subdirName in os.listdir(cwdPath + "/Main/"+ folderName): #eg. "zstack_syringe4...001"
         for filename in sorted(os.listdir(cwdPath + "/Main/"+ folderName + "/" +subdirName)): #eg. cellHeightResults.csv
            if "lamininThicknessResults" in filename:
                content = open(cwdPath + "/Main/"+ folderName + "/" + subdirName + '/' + filename, 'r')
                for row in content:
                    newlist = row.split(',')
                    if "Average lamininThickness (microns)" in newlist[0]:
                        finalLamThicknessPerChip.append(float(newlist[1]))
    averageLamThicknessPerChip = sum(finalLamThicknessPerChip)/len(finalLamThicknessPerChip)
    finalDataPath = cwdPath + "/Main/" + folderName
    writeListToCSV(finalLamThicknessPerChip, finalDataPath, "finalLamThicknessPerChip", averageLamThicknessPerChip)  
