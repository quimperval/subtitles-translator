import sys
import re
from openai import OpenAI
from sub import subtitle


def chat_gpt(apiKey, prompt):
    client=OpenAI(api_key=apiKey)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

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

print ("Hello world! No call")
fileName= sys.argv[1]
mKey= sys.argv[2]

destLanguage= sys.argv[3]

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
for line in linesList:
    print (line, end="")
    if(re.search(timeRegex, line)!=None):
        mSub = subtitle()
        mSub.timeStartAndEnd = line
        continue
    elif(re.search(blankLine, line)!=None):
        if(mSub!=None):
            subsList.append(mSub)
        mSub = None
    else:
        mSub.add_text(line)

if(mSub!=None):
    subsList.append(mSub)
    
print ("Subtitles list: " ,(len(subsList)))    
position=0
counter=0
size=len(subsList)
#Create a dict that stores the timestamp and the position of the subtitle in the list. 
#If something fails during the translation and the response from the openai 
#Then restart the process from the point where the last subtitle was processed
#By default do it from the penultimate subtitle in the response.
calls=0
temp = "---BEGIN---\n"
while(position<size):
    print("counter: ", str(counter))
    print("position: ", str(position))
    xSub = subsList[position]
    print(str(xSub.timeStartAndEnd), end='')
    temp = str(temp) +'' + str(xSub.timeStartAndEnd)
    for mSubLine in xSub.texts: 
        temp = temp + mSubLine
    temp = temp + "\n"
    counter= counter+1
    position= position+1       
    if(counter==10 or position>=(size)):
        temp= temp + "---END---"
        print ("************************************")
        print (chat_gpt_dummy(mKey, prompt+temp))
        print ("************************************")
        counter=0

        calls=calls+1
        if(calls==1):
            break;
        temp = "---BEGIN---\n"

#print ("Total calls, "+str(calls))
