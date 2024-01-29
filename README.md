# BOARD GAME VK API BOT

## What does it do?
A simple script that calls VK API and uploads to a conversation a picture (NYI) and greetings as a VK community bot.

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
