import csv
import os

#get num pixels to calculate % orthogonal coverage

def writeToCSV(list, filePath, stain, averageValue):
  with open (filePath + "/" + stain + " Coverage", 'w') as csvfile:
    fileWriter = csv.writer(csvfile)
    i = 1
    for line in list:
      k = str(i)
      fileWriter.writerow(["Pixel Coverage " + k + "(%)", line])
      i = i + 1
    fileWriter.writerow(["Average Pixel Coverage (%)", averageValue])


def calculateChipCoverage(stain, chipFolder):
  totPixels = 100*2048 #total number of pixels (arbitrary num)
  pixelCoverageList = []
  for imageFolder in os.listdir(chipFolder):
    for filename in os.listdir(chipFolder + "/" + imageFolder):
      if "Filtered" in filename:
        #calculate pixelCoverage
        content = open(chipFolder + "/" + imageFolder + "/" + filename, 'r')
        pixelCoverage = 0
        numPixels = 0
        for line in content:
          row = line.split(',') 
          if row[2].rstrip() == "Gray Value":
            continue #skip header
          if float(row[2].rstrip()) != 0:
            numPixels = numPixels + 2048*float(row[2])/255
        pixelCoverage = numPixels/totPixels*100
        pixelCoverageList.append(pixelCoverage)
  averageValue = sum(pixelCoverageList)/len(pixelCoverageList)
  writeToCSV(pixelCoverageList, chipFolder, stain, averageValue)


#calculate pixel coverage per spreadsheet
cwdPath = os.getcwd()
for chipFolder in os.listdir(cwdPath + "/Main"):
  dataPath = cwdPath + "/Main/" + chipFolder
  if os.path.isfile(dataPath):
    continue
  calculateChipCoverage("NaK_ATPase", dataPath) 
