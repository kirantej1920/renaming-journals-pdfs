renaming-journals-pdfs
======================

This project tries to rename the pdf files of the science journals
This project is very quickly set-up 

TODO
1) Cleaning and Efficient implementation of the script

#Usage: 

python checkMd5sum.py >& check-duplicated.log
python rename.py >& rename.log

#Kindly take the backup of the original before applying this script.
#Also you can re-verify the number of PDF files before and after running the script

#Shell Command for the same :
find . -name *.pdf | wc -l  
#Above command can be used before and after applying the script to ensure no pdf files has been lost ;)

