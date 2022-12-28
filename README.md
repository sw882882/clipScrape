a bunch of scripts I made to help with clipping streams, it should work as long as yt-dlp and chat-downloader supports whatever website you wish to use

the links and info goes into info.json

run chatScrape.py to generate a graph to see chat frequency

run videoScrape.py to download time periods with high chat frequency

run subtitles.py to autogenerate srt subtitles with whisper (openAI), you probably need a decent gpu for this, might also need to mess with the model.

TO-DOs
- [ ] make a pyQT UI to make videoScrape.py less just downloading randomly and actually user controllable
