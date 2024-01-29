# BOARD GAME VK API BOT

## What does it do?
A simple script that calls VK API and uploads to a conversation a picture (NYI) and greetings as a VK community bot.
Board game themed.

## Usage


### Prerequisites (Windows 10 x64)
```
pip install vk_api ./pycurl_win64/pycurl-7.45.1-cp310-cp310-win_amd64.whl
```
### Startup
```
python bgfridaybot.py
```
### Pipeline
Bot wil run until it's interrupted or closed

## Note!

### PycURL
You need python 3.4-3.11 for this to function, because of pycurl.    
If you're having trouble installing pycurl on windows - go [here]( https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycurl)
to download a pre-built wheel.

There is an included windows 10 x86-64 prebuilt wheel at [./pycurl_win64](pycurl_win64/pycurl-7.45.1-cp310-cp310-win_amd64.whl).

### API key (WIP)
Supplementing a *(community API)* key with configured photo and message priviledges through console arguments is NYI, for now just edit the "key" attribute and conversation ID and PEER directly in [.py](bgfridaybot.py) file.

## Currently supported features
- Hardcoded: 
  - API key and IDs
  - List of hello prompts
  - List of "Board games of the day"
- Sending random photos from a specified folder function (if uncommented)

## Planned features
- Console arguments
  - API key(s)
  - Community ID
  - Conversation ID
  - Conversation Peer ID
  - Language
- External database of hello prompts
- [BoardGameGeek XML API](https://boardgamegeek.com/wiki/page/BGG_XML_API#) integration
  - Automatic "Board game of the day" acquiring
- Creating configurable polls in stub community
- Stable diffusion [CPU (OpenVINO)](https://github.com/bes-dev/stable_diffusion.openvino) and [GPU (streamline)](https://github.com/CompVis/stable-diffusion) integration 
  - Picture generation from "Board game of the day" prompt
  - Random board game concepts?
- Multiple language translation (EN-RU primarily)
- Various chat integrations
  - Answers to a keyword
  - Board game search engine?