import sys
import re
from openai import OpenAI
from sub import subtitle
import configparser
import os
from time import sleep


def chat_gpt(apiKey, prompt):
    client=OpenAI(api_key=apiKey)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def linesToSubtitleObjects(linesList, subsList):
    """
    Parameters:
    linesList: an array of lines (strings) to be parsed to create subtitles objects
    subsList: list that will store the subtitle objects created during the parsing
    
    Returns:
    None
    """
    mSub = None
    processedTimeStamps = dict()
    for line in linesList:
        #print (line, end="")
        if(re.search(timeRegex, line)!=None):
            mSub = subtitle()
            mSub.timeStartAndEnd = line
            continue
        elif(re.search(blankLine, line)!=None):
            if(mSub!=None):
                subsList.append(mSub)
            mSub = None
        else:
            #print(line)
            mSub.add_text(line)

    if(mSub!=None):
        subsList.append(mSub)
    
    return
    

def parseStringResponseAllOK(responseArray, translated, destFileName):
    """
    This method will check the response from openAi and based on the BEGIN and END tags of the 
    subtitles chunk it will return None if all the subtitles were translated
    or will return the timestamp of the latest successfully translated subtitle
    
    Parameters:
    responseArray: an array of lines (strings) to be parsed to create subtitles objects
    it includes the BEGIN and ENDS tags
    translated: list that will store the translated subtitle objects
        
    Returns:
    None or timestamp
    """
    #Prepare the subslines
    linesList = list()
    for i in range(1, len(responseArray)-1):
        #print (responseArray[i])
        linesList.append(responseArray[i])
    subsList = list()
    linesToSubtitleObjects(linesList, subsList)
    
    print ("\x1b[KSubtitles Chunk list size: " + str(len(subsList)), end="\r")
    destFileObj = open(destFileName, "a")
    for xSub in subsList:
        destFileObj.write(xSub.timeStartAndEnd+"\n")
        for line in xSub.texts:
            destFileObj.write(line+"\n")
            destFileObj.write("\n")
    destFileObj.close()    
    
    sleep(0.05)
    translated.extend(subsList)
    return None

def parseStringPartialResponse(responseArray, translated, destFileName):
    firstLine = responseArray[0]
    if(firstLine!="---BEGIN---"):
        if(len(translated)>0):
            return translated[len(translated)-1].timeStartAndEnd
        else:
            return "START_FROM_SCRATCH"
    else:
        linesList = list()
        for i in range(1, len(responseArray)):
            #print (responseArray[i])
            linesList.append(responseArray[i])
        
        subsList = list()
        linesToSubtitleObjects(linesList, subsList)
        #print("latestTime: " + subsList[len(subsList)-1].timeStartAndEnd)
        #print("latest text", subsList[len(subsList)-1].texts)
        if(len(subsList)>1):
            for i in range(0, len(subsList)-1):
                #print("translated.append(subsList[i]): " + subsList[i].timeStartAndEnd)
                #print(subsList[i].texts)
                translated.append(subsList[i])
                
            return translated[len(translated)-1].timeStartAndEnd
        else:
            #This means all the chunk failed
            if(len(translated)>0):
                return translated[len(translated)-1].timeStartAndEnd
            else:
                return "START_FROM_SCRATCH"
        

def processResponse(response, translated, destFileName):
    """
    This method will check the response from openAi and based on the BEGIN and END tags of the
    subtitles chunk it will return None if all the subtitles were translated
    or will return the timestamp of the latest successfully translated subtitle
    
    Parameters:
    responseArray: an array of lines (strings) to be parsed to create subtitles objects
    it includes the BEGIN and ENDS tags
    translated: list that will store the translated subtitle objects
        
    Returns:
    None or timestamp
    """
    #print ("Parsing response")
    responseArray = response.split("\n")
    #print("Response lines: " + str(len(responseArray)))
    firstLine = responseArray[0]
    #print(firstLine)
    lastLine = responseArray[len(responseArray)-1]
    #print(lastLine)
    if(firstLine=="---BEGIN---" and lastLine=="---END---"):
        print ("\x1b[KProcessed completely from openAI", end='\r')
        
        parseStringResponseAllOK(responseArray, translated, destFileName)
        return None
    else:
        print ("\x1b[KProcessed partially", end='\r')
        result = parseStringPartialResponse(responseArray, translated, destFileName)
        return result
        #In this case will be returned the timeStartAndEnd of the latest
        #successfully translated line
    return None


def chat_gpt_dummy(apiKey, dummyPrompt):
    response = r"""---BEGIN---
0:00:18.80 --> 0:00:21.00
¡Alisó su cabello!

0:00:22.44 --> 0:00:24.40
Movió su cabeza así.

0:00:27.60 --> 0:00:30.16
¿Pensaste lo mismo?

0:00:30.32 --> 0:00:32.52
¡No, yo no!

0:00:33.96 --> 0:00:39.52
Debe ser maravilloso dormir\Nen una cama enorme en un lujoso hotel.

0:00:39.68 --> 0:00:42.00
-¿Si duermes?\N-¿Por qué, qué harías?

0:00:42.16 --> 0:00:45.08
-¿En tu noche de bodas?\N-Tomar una ducha.

0:00:45.24 --> 0:00:47.52
-¿Y luego?\N-Luego tomaría un baño.

0:00:47.68 --> 0:00:50.68
-¿Y luego?\N-Vería la vista.

0:00:50.84 --> 0:00:54.52
Debe haber un final.\NY ¿qué sucede en una noche de bodas?

---END---"""
    return response

def chat_gpt_dummybad(apiKey, dummyPrompt):
    print("Sending: " + dummyPrompt)
    response = r"""---BEGIN---
0:00:18.80 --> 0:00:21.00
¡Alisó su cabello!

0:00:22.44 --> 0:00:24.40
Movió su cabeza así.

0:00:27.60 --> 0:00:30.16
¿Pensaste lo mismo?

0:00:30.32 --> 0:00:32.52
¡No, yo no!

0:00:33.96 --> 0:00:39.52
Debe ser maravilloso dormir\Nen una cama enorme en un lujoso hotel.

0:00:39.68 --> 0:00:42.00
-¿Si duermes?\N-¿Por qué, qué harías?

0:00:42.16 --> 0:00:45.08
-¿En tu noche de bodas?\N-Tomar una ducha.

0:00:45.24 --> 0:00:47.52
-¿Y luego?\N-Luego tomaría un baño.

0:00:47.68 --> 0:00:50.68
-¿Y luego?\N-Vería la vista.

0:00:50.84 --> 0:00:54.52
Deb"""
    return response

# Create a ConfigParser object
config = configparser.ConfigParser()
config.sections()
# Read the configuration file
config.read('configuration.ini')

fileName= sys.argv[1]
mKey= config.get('DEFAULT', 'openaikey')
#mKey = config['DEFAULT']['openaikey']
destLanguage= sys.argv[2]

destFileName=None
if len(sys.argv)>3:
    destFileName=sys.argv[3]    

if(destLanguage.lower()=="es"):
    destLanguage="Spanish"
elif(destLanguage.lower()=="en"):
    destLanguage="English"

prompt="Please translate the below subtitles to "+destLanguage+" and preserve the time marks. Do not translate the ---BEGIN--- and ---END--- marks:\n"

print ("Filename: " + fileName)

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="",
)

timeRegex="^\s*[0-9]{1,3}:[0-9]{1,3}:[0-9]{1,3}\.?[0-9]{1,3}\s*-->\s*[0-9]{1,3}:[0-9]{1,3}:[0-9]{1,3}\.?[0-9]{1,3}$"
blankLine="^ *$"
file=open(fileName, "r")
line = ""
packCounter=0
linesList = list()

for line in file:
    linesList.append(line);
file.close()

mSub = None
subsList = list()
processedTimeStamps = dict()
#Here the lines of the origin file are processed. 
for line in linesList:
    #print (line, end="")
    if(re.search(timeRegex, line)!=None):
        mSub = subtitle()
        mSub.timeStartAndEnd = line
        continue
    elif(re.search(blankLine, line)!=None):
        if(mSub!=None):
            subsList.append(mSub)
        mSub = None
    else:
        try:
            mSub.add_text(line)
        except:
            print("An exception happened while trying to add a line in the sub.")
            print("Last line successfully processed is " + subsList[len(subsList)-1].timeStartAndEnd)

if(mSub!=None):
    subsList.append(mSub)


#Prepare the file name to be saved, and dump the retrieved subtitles to a file
tempFile = os.path.basename(file.name)
fileNameArray = tempFile.split(".")
destFileObj = None
if destFileName==None:
    destFileName=""
    if(fileNameArray[len(fileNameArray)-2]=="en" or fileNameArray[len(fileNameArray)-2]=="de" or fileNameArray[len(fileNameArray)-2]=="se"):
        for i in range(0,len(fileNameArray)):
            if(i==len(fileNameArray)-2):
                destFileName = destFileName+"es"+"."
            elif(i==len(fileNameArray)-1):
                destFileName= destFileName+fileNameArray[i]
            else:
                destFileName= destFileName+fileNameArray[i]+"."
            
    else:
        for i in range(0,len(fileNameArray)):
            if(i==len(fileNameArray)-1):
                destFileName = destFileName+"es"+"."+destFileName+fileNameArray[i]
            else:
                destFileName= destFileName+fileNameArray[i]+"."

    directory = os.path.dirname(file.name)

    if directory=="":
        destPath=destFileName
    else:
        destPath=directory+"/"+destFileName
        
    destFileObj = open(destPath, "w")
else:
    destFileObj = open(destFileName, "w")
    
destFileObj.close()
print("Destfile: " + destFileName);    


#Create the file

#print ("Subtitles list: " ,(len(subsList)))
position=0
counter=0
size=len(subsList)
calls=0
temp = "---BEGIN---\n"
translated = list()
subsMap = dict()
errorThreshold=1000
errorCount=0
chunkSize=20
while(position<size):
    print ("\x1b[KAlready translated: " + str(len(translated)) + " of " +str(len(subsList))+ ": " + str(len(translated)*100/len(subsList)) + "%", end=" \r")
    #print("counter: ", str(counter))
    #print("position: ", str(position))
    xSub = subsList[position]
    subsMap[xSub.timeStartAndEnd.replace("\n","")] = position
    #print("subsMap[xSub.timeStartAndEnd]: "+ xSub.timeStartAndEnd.replace("\n","")+" its position: " +str(subsMap[xSub.timeStartAndEnd.replace("\n","")]))
    #print(str(xSub.timeStartAndEnd), end='')
    temp = str(temp) +'' + str(xSub.timeStartAndEnd)
    for mSubLine in xSub.texts:
        temp = temp + mSubLine
    temp = temp + "\n"
    counter= counter+1
    position= position+1
    if(counter==chunkSize or position>=(size)):
        temp= temp + "---END---"
        #print ("************************************")
        #print ("prompt: ")
        #print(prompt+temp)
        print("\x1b[KCalling openAI...", end='\r')
        response = chat_gpt_dummy(mKey, prompt+temp)
        #print ("************************************")
        #print (response)
        #print ("************************************")
        print ("\x1b[KProcessing response", end='\r')
        result = processResponse(response, translated, destFileName)
        #print ("************************************")
        #print("result: " + result)
        
        if(result!=None):
            print("\x1b[KSomething went wrong, checking", end='\r')
            errorCount = errorCount+1
            if(errorCount>=errorThreshold):
                print("\n")
                print ("Giving up, errorThreshold was reached")
                exit()
            if(result=="START_FROM_SCRATCH"):
                position=0
                counter=0
                temp = "---BEGIN---\n"
                continue
            else:
                #print ("checking the position of the timestamp to reprocess")
                #print ("Position: " + str(subsMap.get(result)))
                position = subsMap.get(result)+1
                #print ("NEw start: " + str(position))
                counter=0
                temp = "---BEGIN---\n"
                continue
        
        #print ("************************************")
        counter=0

        #calls=calls+1
        #if(calls==1):
            #break;
        temp = "---BEGIN---\n"
print("\n")

exit()
