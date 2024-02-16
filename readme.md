# Subtitle translator

## Description

This script relies on the openAi API which is called to translate the subtitles.

You have to have a valid api key.

A sample.ini file is included, you can use it to store the api key and script will take it, just name your configuration file as configuration.ini

This script has a fallback logic that considers failures in the response from openAI, when that happens it restart the process from the subtitle just after the last successfully translated.

**This script DOES NOT considering numbering of the subtitles**.

The script that converts sub to srt considers the below structure

```
    Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text
    Dialogue: ,0:00:14.40,0:00:18.12,Default,,0,0,0,,I am a subtitle
```