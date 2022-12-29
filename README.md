# ClipScrape
## _A bunch of scripts to help with clipping streams_
a bunch of scripts I made to help with clipping streams, it should work as long as yt-dlp and chat-downloader supports whatever website you wish to use
## Installation & Usage
1. install python and pip
2. pip install -r requirements.txt
3. use the scripts
    1. the links and info goes into info.json
    2. run chatScrape.py to generate a graph to see chat frequency, graphs, json, and csv output will be in the ./working directory
    3. run videoScrape.py to download time periods with high chat frequency, output videos will be in the output directory
    4. run subtitles.py to autogenerate srt subtitles with whisper (openAI), you probably need a decent gpu for this, might also need to mess with the model. srt files will be outputted into the same output directory as the videos with the same file name

TO-DOs
- [x] make a pyQT UI to make videoScrape.py less just downloading randomly (which is currently just download -3 min & +5 min from the peak chat frequency) and actually user controllable.
