import csv
import os

cwdPath = os.getcwd()
print(cwdPath)

#function that calculates cilia length from last peak in spreadsheet, stain in spreadsheet filename
def halfData(dataPath, stain):
    for filename in sorted(os.listdir(dataPath)):
        #for each csv, 
        if "Results_NaK_ATPase" in filename: 
            content = open(dataPath + '/' + filename, 'r')
            with open(dataPath + "/" + "Filtered_Results_"+ stain, 'w') as csvfile:
                fileWriter = csv.writer(csvfile)
                for row in content: 
                    newlist = row.split(',')
                    if newlist[1].rstrip() == "Distance":
                        fileWriter.writerow([newlist[0].rstrip(), newlist[1].rstrip(), newlist[2].rstrip()])
                        continue
                    remainder = float(newlist[1])*10 % 4 #check if divisible by 0.4
                    if remainder == 0 or remainder == 0.000:
                        fileWriter.writerow([float(newlist[0]), float(newlist[1]), float(newlist[2])])

#get rid of data points associated with step size of 0.2 um
for folderName in os.listdir(cwdPath + "/Main"): #folder name = chip (eg. "Nutritive N4 T2")
    for subdirName in os.listdir(cwdPath + "/Main/"+ folderName): #subfolder name = image (eg. "zstack_syringe4...001")
        newPath = cwdPath + "/Main/"+ folderName + "/" + subdirName 
        halfData(newPath, "NaK_ATPase")