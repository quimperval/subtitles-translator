# Subtitle translator

## Description

### Translator

This script **translateSubs.py** relies on the openAi API which is called to translate the subtitles.

You have to have a valid api key.

A sample.ini file is included, you can use it to store the api key and script will take it, just name your configuration file as configuration.ini

This script has a fallback logic that considers failures in the response from openAI, when that happens it restart the process from the subtitle just after the last successfully translated.

**This script DOES NOT considering numbering of the subtitles**.

*VERY IMPORTANT!!*

    You have to remove the numbers listing each subtitle. 
    The files has to have the milliseconds separated by dot, and not by comma.
    The file has not to have the start with the UTF-8 bytes marker

Below you can get the way to match the conditions

#### Remove subtitles numbering

If you have a file with subtitles numbering you can remove it using this command in the terminal
    
    awk '$0 ~ /^[0-9]+$/{ next; } { print $0}' subtitle.srt

### Reformat the time to use . instead of , for the milliseconds

    sed -E  '/^\s*[0-9]{1,3}:[0-9]{1,3}:[0-9]{1,3},?[0-9]{1,3}\s*-->\s*[0-9]{1,3}:[0-9]{1,3}:[0-9]{1,3},?[0-9]{1,3}$/s/,/\./g'

### Remove the UTF-8 bytes

    sed '1s/^\xEF\xBB\xBF//'


#### Execute the script

The syntax to use the python script is 
    
    python3 translateSubs.py filename.srt es

#### Add another target language

where *es* is the destination language, I use the short names of languages used for subtitles, you could add any other language in the code where it says: 

    if(destLanguage.lower()=="es"):
        destLanguage="Spanish"
    elif(destLanguage.lower()=="en"):
        destLanguage="English"

you could add another condition to be added in the prompt in the line: 

    prompt="Please translate the below subtitles to "+destLanguage+" and preserve the time marks. Do not translate the ---BEGIN--- and ---END--- marks:\n"


### Subtitle format converter from sub to srt

The script that converts sub to srt considers the below structure

```
    Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
    Dialogue: ,0:00:14.40,0:00:18.12,Default,,0,0,0,,I am a subtitle
```


