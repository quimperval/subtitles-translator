import sys
import re
from openai import OpenAI
from sub import subtitle


def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

print ("Hello world! No call")
fileName= sys.argv[1]
mKey= sys.argv[2]

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
temp = ""
while(position<size):
    xSub = subsList[counter]
    print(xSub.timeStartAndEnd, end='')
    temp = temp +'' + xSub.timeStartAndEnd
    for mSubLine in xSub.texts:
        temp = temp + mSubLine
    counter= counter+1       
    if(counter==10):
        print (temp)
        temp = 0
        



