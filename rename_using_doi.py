#				PREAMBLE
#  The GNU General Public License is a free, copyleft license for
#software and other kinds of works.
#
#  The licenses for most software and other practical works are designed
#to take away your freedom to share and change the works.  By contrast,
#the GNU General Public License is intended to guarantee your freedom to
#share and change all versions of a program--to make sure it remains free
#software for all its users.  We, the Free Software Foundation, use the
#GNU General Public License for most of our software; it applies also to
#any other work released this way by its authors.  You can apply it to
#your programs, too.
#
#  When we speak of free software, we are referring to freedom, not
#price.  Our General Public Licenses are designed to make sure that you
#have the freedom to distribute copies of free software (and charge for
#them if you wish), that you receive source code or can get it if you
#want it, that you can change the software or use pieces of it in new
#free programs, and that you know you can do these things.
#
#  To protect your rights, we need to prevent others from denying you
#these rights or asking you to surrender the rights.  Therefore, you have
#certain responsibilities if you distribute copies of the software, or if
#you modify it: responsibilities to respect the freedom of others.
#
#  For example, if you distribute copies of such a program, whether
#gratis or for a fee, you must pass on to the recipients the same
#freedoms that you received.  You must make sure that they, too, receive
#or can get the source code.  And you must show them these terms so they
#know their rights.
#
#  Developers that use the GNU GPL protect your rights with two steps:
#(1) assert copyright on the software, and (2) offer you this License
#giving you legal permission to copy, distribute and/or modify it.
#
#  For the developers' and authors' protection, the GPL clearly explains
#that there is no warranty for this free software.  For both users' and
#authors' sake, the GPL requires that modified versions be marked as
#changed, so that their problems will not be attributed erroneously to
#authors of previous versions.
#
#  Some devices are designed to deny users access to install or run
#modified versions of the software inside them, although the manufacturer
#can do so.  This is fundamentally incompatible with the aim of
#protecting users' freedom to change the software.  The systematic
#pattern of such abuse occurs in the area of products for individuals to
#use, which is precisely where it is most unacceptable.  Therefore, we
#have designed this version of the GPL to prohibit the practice for those
#products.  If such problems arise substantially in other domains, we
#stand ready to extend this provision to those domains in future versions
#of the GPL, as needed to protect the freedom of users.
#
#  Finally, every program is threatened constantly by software patents.
#States should not allow patents to restrict development and use of
#software on general-purpose computers, but in those that do, we wish to
#avoid the special danger that patents applied to a free program could
#make it effectively proprietary.  To prevent this, the GPL assures that
#patents cannot be used to render the program non-free.
#
#  The precise terms and conditions for copying, distribution and
#modification follow.
#

import os
import re
import sys
from random import randint
import urllib2, cookielib
from BeautifulSoup import BeautifulSoup

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
repeatCount = 0
myMap = {}
tool = "pdftotext"
options = " -l 1 "
#options = " -f 2 -l 2 "
proxy = "http://dx.doi.org/"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
for fileName in files:
    #print files
    #if fileName.find("/RENAMED/")>=0:
    #alreadyRenamed += 1
    #continue
    	dirName = os.path.dirname(fileName)
    	if not os.path.exists(dirName+"/RENAMED"):
    		os.makedirs(dirName+"/RENAMED")
    	if not os.path.exists(dirName+"/NOT-RENAMED"):
    		os.makedirs(dirName+"/NOT-RENAMED")
    #print "Processing : " + fileName
	
        if fileName.lower()[-3:] != "pdf":
	    print "\t -- Not a PDF File\n"
            continue
	totalPdfFiles += 1
	fileName1 = fileName.replace(" ","\ ")	
	fileName1 = fileName1.replace(",","\,")
	fileName1 = fileName1.replace("\"","\\\"")
	textFileName = "temp.txt"
	# fileName = fileName1
        command = tool + options + " " + "'" + str(fileName) + "'" + " " + textFileName 
        #command = tool + options + " " + str(fileName1) + " " + textFileName 
	#print "Command: " + command
	os.system(command)
	#textFileName = fileName.replace("pdf","txt")
	fp = open(textFileName, "rb")
	count = 0
	finalName = ""
	for line in fp:
	    if line.lower().find("doi:") > -1:
		print "Processing File: " + fileName
                #print "Unprocessed DOI:" + line
                #print line
		doiString = line
		temp = doiString[doiString.lower().find("doi:")+4:].strip()
		if len(temp) == 0:
			print "Read next line and get the doi information"
			temp = fp.next()
		if temp.endswith(")"):
			temp = temp[:temp.rfind(")")]
		#print "Processed  DOI : " + temp
		if temp.find(",") != -1:
			temp = temp[:temp.find(",")]
		if temp.find(" ") != -1:
			temp = temp[:temp.find(" ")]
		#print temp
		web_link = proxy + temp	
		print "Web_link: " + web_link
		command = "wget " + web_link + " -q -O temp"
		#print command
		os.system(command)
		soup = BeautifulSoup(open("./temp"))
		if soup.title is None:
			print "Could not extract title"
		else:
			title =  soup.title.string.strip(" \t\n")
			print "Original Title<tag>: " + title
			if title.find("JNS -  Neurosurgical Focus") > -1:
				title = soup.h3.getText()
			elif title.find("British Journal of Neurosurgery") > -1:
				title = title
			elif title.find("Journal of Neurosurgery") > -1:
				title = soup.h3.getText()
			elif title.find("Elsevier: Article Locator") > -1:
				title = soup.h1.nextSibling.string
			elif title.find("Wolters Kluwer Health - Article Landing Page") > -1:
				title = "Wolters Kluwer Health - Article Landing Page -- So Cannot be renamed"
#			else:
#				if(soup.h1 is None):
#					title = "Cannot be renamed"
#				else:
#					title = soup.h1.getText()
			print "Title: " + title 
		print "\n"
