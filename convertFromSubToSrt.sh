#!/bin/bash

sourceFile=$1
destFolder=$2

echo "Converting: "$sourceFile
echo "Destination folder: " $destFolder

destinationFile=$(basename -- $sourceFile)
destinationFile=`echo $destinationFile | sed 's/\.sub$/\.srt/g'`

#echo $destinationFile | awk -F"." '{if(tolower($(NF-1))=="en" ||tolower($(NF-1))=="se" ){ print "es or se" } }' 
#echo $(basename -- $sourceFile)

awk -F"," '$0 ~/^Dialogue.*/ { text=""; for(i=10; i<=NF;i++){ text=text$i }; print $2" --> "$3; print text; print "" }' $sourceFile > $destFolder$destinationFile

ls $destFolder$destinationFile
