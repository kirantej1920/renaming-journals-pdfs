
import os
import re
import sys
from random import randint

def getFullName(fileName):
    return os.path.join(path, fileName)
white_space_seperator = " "
md5Dict = { }
md5Log = "md5.log"
path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else '.'
invalid_chars = '[<>:\"/\\|?*]'
#files = os.listdir(path)
files = []
repeated = 0
for root, dirs, pdfFiles in os.walk('.'):
      for file in pdfFiles:
            if file.endswith('.pdf'):
                  files.append(os.path.join(root, file))
if os.path.isfile(md5Log):
    print "Over-writing " + md5Log + " !!"
    os.remove(md5Log)
os.system("touch " + md5Log)
#os.system( "echo 'Md5Sum  FileName ' > " + md5Log)
for fileName in files:
	#fileName = fileName.replace("'","\\'")
	#print "Processing " + fileName
	command = 'md5sum "' + fileName + '" >>' + md5Log
	#print command 
	os.system(command)

fp = open(md5Log, "rb")
for line in fp:
	md5Sum = line[:line.find(" ")].strip()
	fileName = line[line.find(" "):].strip()
	if md5Dict.has_key(md5Sum):
		print fileName + " is repeated !!"
		print "Its original File is " + md5Dict.get(md5Sum)
		repeated += 1
	else: 
		md5Dict[md5Sum] = fileName
print "----------------------------------------------"
print "Total items found "+str(len(files))
print "Total Unique Items found "+str(len(md5Dict))
print "Total Duplicates found " + str(repeated)
print "Check "+ md5Log + " for detail md5 Details"

