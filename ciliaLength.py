import csv
import os

cwdPath = os.getcwd()

def writeListToCSV(list, dataPath, filename, averageValue):
    with open(dataPath + "/" + filename, 'w') as csvfile:
        fileWriter = csv.writer(csvfile)
        i = 0
        for line in list:
            k = str(i)
            fileWriter.writerow([filename + k + "(microns)", line])
            i = i + 1
        fileWriter.writerow(["Average " + filename + " (microns)", averageValue])

#calculate cilia length (length of last peak in spreadsheet), cilia coverage (cilia pixels / fixed area x100) per IMAGE
for folderName in os.listdir(cwdPath + "/Main"): #folder name (eg. "Nutritive N4 T2")
    for subdirName in os.listdir(cwdPath + "/Main/"+ folderName): #subfolder name (eg. "zstack_syringe4...001")
        newPath = cwdPath + "/Main/"+ folderName + "/" + subdirName 
        for filename in sorted(os.listdir(newPath)):
            filteredCiliaLocation = []
            coveredPixels = 0
            totPixels = 100*2048 #max width and length of an image in pixels
            #for each csv, calculate cilia length
            if "Results_cilia1" in filename: 
                with open(newPath + "/" + "ciliaStats", 'w') as csvfile:
                    fileWriter = csv.writer(csvfile)
                    content = open(newPath + '/' + filename, 'r')
                    lines = content.readlines()
                    hasFoundPeak = False 
                    totArea = 0
                    for row in reversed(lines): #read file backwards to read last peak first
                        newlist = row.split(',')
                        #if pixel intensity is non-zero, record the location and add num white pixels
                        if float(newlist[2].rstrip()) != 0:
                            filteredCiliaLocation.append(float(newlist[1]))
                            coveredPixels = coveredPixels + 2048*float(newlist[2])/255 #number of pixels calculated from: gray value (avg) = (255*NumPixels + 0) / 2048
                            hasFoundPeak = True
                        if float(newlist[2].rstrip()) == 0 and hasFoundPeak == True:
                            break
                    pixelCoverage = coveredPixels/totPixels * 100
                    fileWriter.writerow(["Cilia Pixel Coverage (%)", pixelCoverage])
                #calculate cell height
                    if len(filteredCiliaLocation) != 0:
                        cTop = max(filteredCiliaLocation) 
                        cBottom = min(filteredCiliaLocation)
                        ciliaLength = cTop - cBottom 
                        fileWriter.writerow(["Max Cilia Length (microns)", ciliaLength])


#calculate cilia stats per CHIP (averaging 5 images) 
for folderName in os.listdir(cwdPath + "/Main"): # eg. "Nutritive N4 T2"
    finalChipLength = []
    finalChipCoverage = []
    finalChipLength.clear() 
    finalChipCoverage.clear()  
    #for each csv (filename in subdir), pull the average
    for subdirName in os.listdir(cwdPath + "/Main/"+ folderName): #eg. "zstack_syringe4...001"
        newPath = cwdPath + "/Main/"+ folderName + "/" + subdirName 
        for filename in sorted(os.listdir(newPath)): #eg. cellHeightResults.csv
            if "ciliaStats" in filename:
                content = open(newPath + '/' + filename, 'r')
                i = 0
                j = 0
                for row in content:
                    newlist = row.split(',')
                    if "Max" in newlist[0]:
                        finalChipLength.append(float(newlist[1]))
                    if "Coverage" in newlist[0]:
                        finalChipCoverage.append(float(newlist[1]))
                averageChipLength = sum(finalChipLength)/len(finalChipLength)
                averageChipCoverage = sum(finalChipCoverage)/len(finalChipCoverage)
                writeListToCSV(finalChipLength, cwdPath + "/Main/"+ folderName, "CiliaLength", averageChipLength)
                writeListToCSV(finalChipCoverage, cwdPath + "/Main/"+ folderName, "CiliaCoverage", averageChipCoverage)

