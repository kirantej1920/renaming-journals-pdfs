import os
import re
import sys
from random import randint

def getFullName(fileName):
    return os.path.join(path, fileName)
white_space_seperator = " "
path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else '.'
invalid_chars = '[<>:\"/\\|?*]'
#files = os.listdir(path)
files = []
for root, dirs, pdfFiles in os.walk('.'):
      for file in pdfFiles:
            if file.endswith('.pdf'):
                  files.append(os.path.join(root, file))
renamed = 0
totalPdfFiles = 0
alreadyRenamed = 0
notPossibleToRename = 0
tool = "pdftotext"
options = " -l 1 "
#options = " -f 2 -l 2 "
for fileName in files:
    if fileName.find("/RENAMED/")>=0:
	alreadyRenamed += 1
	continue
    dirName = os.path.dirname(fileName)
    if not os.path.exists(dirName+"/RENAMED"):
    	os.makedirs(dirName+"/RENAMED")
    if not os.path.exists(dirName+"/NOT-RENAMED"):
    	os.makedirs(dirName+"/NOT-RENAMED")
    #print "Processing : " + fileName
    try:
        if fileName.lower()[-3:] != "pdf":
	    print "\t -- Not a PDF File\n"
            continue
	totalPdfFiles += 1
	#fileName1 = fileName.replace(" ","\ ")	
	#fileName1 = fileName1.replace(",","\,")
	textFileName = "temp.txt"
	fileName1 = fileName
        command = tool + options + " " + "'" + str(fileName) + "'" + " " + textFileName 
        #command = tool + options + " " + str(fileName1) + " " + textFileName 
	#print "Command: " + command
	os.system(command)
	#textFileName = fileName.replace("pdf","txt")
	fp = open(textFileName, "rb")
	count = 0
	finalName = ""
	alreadyRead = ""
	startReading = 0
	if options.find("2") > 0:
		startReading = 1
	for line in fp:
		#if count > 0:
		#	break
		#bufferStr = line.strip()
		bufferStr = line
		#print "Read: " + bufferStr
		#print "StartReading " + str(startReading)
		if bufferStr is None:
			print("\tUnexpected END\n")
		bufferStrUpper = bufferStr.upper()
		if bufferStrUpper == "":
			continue
		if bufferStrUpper == "\t":
			continue
		if bufferStrUpper == "\n":
			if startReading == 0: 
				startReading = 1
				continue
			#if startReading == 1:
			#	if finalName != "":
			#		break	
		if bufferStrUpper.find("ARTICLE") >= 0:
			continue
		if bufferStrUpper.find("CLINICAL STUDIES") == 0:
			continue
		if bufferStrUpper.find("TABLE") >= 0:
			continue
		if bufferStrUpper.find("CONTENTS") >= 0:
			continue
		if bufferStrUpper.find("EDITORIAL") >= 0:
			finalName = "EDITORIAL-"
			continue
		if bufferStrUpper.find("WWW") >= 0 :
			continue
		if bufferStrUpper.find(".COM") >= 0 :
			continue
		if bufferStrUpper.find(", 20") >= 0:
			continue
			#if finalName != "":
		#		break
		if bufferStrUpper.find(", 19") >= 0:
			if finalName != "":
				break
		if bufferStrUpper.find("J NEUROSURG") == 0 :
			continue
		if bufferStrUpper.find(".COM") >= 0 :
			continue
		if bufferStrUpper.find(",") >= 0:
			if finalName != "":
				break
		if bufferStrUpper.find("M.D") >= 0:
			break
		if bufferStrUpper.find("MD") >= 0:
			break
		if bufferStrUpper.find("F.R.C.S") >= 0:
			break
		if bufferStrUpper.find("P.H.D.") >= 0:
			break
		if bufferStrUpper.find("PH.D") >= 0:
			break
		if bufferStrUpper.find("FRCS") >= 0:
			break
		if bufferStrUpper.find("B.A") >= 0:
			break
		if bufferStrUpper.find("DEPT") >= 0:
			break
		if bufferStrUpper.find("DEPARTMENT") >= 0:
			break
		#if bufferStrUpper.find("BA") >= 0:
		#	break
		if bufferStrUpper.find("ABSTRACT") >= 0:
			break
		bufferStrUpper = bufferStrUpper.replace(",","_")
		bufferStrUpper = bufferStrUpper.replace(" ","_")
		bufferStrUpper = bufferStrUpper.replace('"',"_")
		bufferStrUpper = bufferStrUpper.replace('&',"_")
		bufferStrUpper = bufferStrUpper.replace(':',"_")
		bufferStrUpper = bufferStrUpper.replace('#',"_")
		bufferStrUpper = bufferStrUpper.replace('%',"_")
		bufferStrUpper = bufferStrUpper.replace('@',"_")
		bufferStrUpper = bufferStrUpper.replace('!',"_")
		bufferStrUpper = bufferStrUpper.replace('*',"_")
		bufferStrUpper = bufferStrUpper.replace('+',"_")
		bufferStrUpper = bufferStrUpper.replace('/',"_")
		bufferStrUpper = bufferStrUpper.replace('.',"_")
		if startReading == 1:
			finalName += bufferStrUpper.replace("\n","_")
		if startReading == 0:
			alreadyRead += bufferStrUpper.replace("\n","_")
	if startReading ==0:
		finalName = alreadyRead
	finalName = re.sub('_+','_',finalName)
	#print "FinalName " + finalName
	finalName = finalName.strip("_") #Removing leading/trailing underscores (_)
	
	if finalName == "" or len(finalName) <= 3:
		#if finalName.find("RENAMED") < 0:
		#	finalName = dirName + "/NOT-RENAMED/" + fileName[fileName.rfind("/")+1:]
		#else:
		finalName = dirName + "/" + fileName[fileName.rfind("/")+1:]
		print "\tNot Possible to rename " + fileName + "\n"
		notPossibleToRename+=1
	else:
        	renamed += 1
		finalName = finalName[0:250]
		finalName += ".pdf"
		if os.path.isfile(finalName):
			print finalName + "already exists!! Appending some numbering"
			finalName = finalName.replace(".pdf",str(randint(1,100))+".pdf")
		if finalName.find("RENAMED") < 0:
			finalName = dirName + "/RENAMED/" + finalName[finalName.rfind("/")+1:]
		else:
			finalName = dirName + "/" + finalName[finalName.rfind("/")+1:]
		cmd = "mv '" + fileName + "' '" + finalName + "'"
		os.system(cmd)
			
	#finalName = getFullName(finalName).replace(" ","_").strip()
	#finalName = finalName.replace(",","")
	#finalName = finalName.replace("\"","")
	#print "FileName " +fileName
	#print "FinalName " +finalName.strip()
	#finalName = finalName.replace("_",white_space_seperator)  # Seperator should be changed initially 
	#if move == 1:
        #os.rename(os.path.abspath(fileName), os.path.abspath(finalName.strip()))
       	print('\tOriginal file: {} | New title: {}\n'.format(fileName, finalName))
    except Exception as e:
        print(e)
        print('\tfile: {}'.format(fileName))
print('\n----------------------------------')
print('PDF files found: {}\nFiles renamed: {}\nAlready renamed: {}\nNot possible to  rename: {}\n'.format(len(files), renamed, alreadyRenamed,notPossibleToRename))
