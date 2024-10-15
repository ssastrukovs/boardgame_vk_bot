# BOARD GAME VK API BOT

## What does it do?
A simple script that calls VK API and uploads to a conversation a picture and greetings as a VK community bot.

Board games' themed.

## Usage

### QUICK START
Install [python](https://www.python.org/downloads/)

Create a file "envargs.txt" and put necessary arguments in it (see [Arguments](#arguments) section)

#### Windows 
Run with Powershell (or [run it in Explorer](launchbot.ps1)) :
```
./launchbot.ps1
```
#### Linux
Allow for execution and run
```
chmod +x launchbot.sh
./launchbot.sh
```
All dependencies shall download automatically.     
If you did not fill envargs.txt or supplied invalid args, it'll prompt you.

### Prerequisites 
```
pip install -r requirements.txt
```
### Startup
Mandatory arguments:
```
python bgfridaybot.py -k <API key> -gid <group id, as in URL> -cid <chat id, as in URL> -cpeer <chat peer, get it somehow>
```
For other arguments, see "Arguments" section of README

### Arguments
```
python bgfridaybot.py -k KEY -gid GROUP_ID -cid CHAT_ID -cpeer CHAT_PEER [-ph 
PHOTO_DIR] [-hp HELLO_PROMPTS] [-bgp BOARD_GAME_PROMPTS] [-lang {en,ru}]

  -k KEY, --key KEY                                                 API key
  -gid GROUP_ID, --group-id GROUP_ID                                ID of the community that bot belongs to
  -cid CHAT_ID, --chat-id CHAT_ID                                   ID of the chat that bot will be sending messages to
  -cpeer CHAT_PEER, --chat-peer CHAT_PEER                           PEER of the chat that bot will be sending messages to
  -ph PHOTO_DIR, --photo-dir PHOTO_DIR                              Directory where random photos that can be posted will be stored
  -hp HELLO_PROMPTS, --hello-prompts HELLO_PROMPTS                  .csv file with hello prompts path, "db/hellos.csv" by default
  -bgp BOARD_GAME_PROMPTS, --board-game-prompts BOARD_GAME_PROMPTS  .csv file with board games list path, "db/games.csv" by default
  -lang {en,ru}, --language {en,ru}                                 Language of choice. Currently 'ru' and 'en' are supported
  -ks KEY_STUB, --key-stub KEY_STUB                                 Stub API key, for your admin account. Needed for polls posting. Go to https://vkhost.github.io/ to get it
  -pdb POLL_DATABASE, --poll-database POLL_DATABASE                 2d matrix for a poll, db/poll.csv by default. First entry is a name, second entry is list of rows, separated by spaces. NOTE! Only one row (poll) is supported for now
```

If creating custom .csv databases, please keep them similar to provided ones
### Polls
To enable polls functionality, you need to be an administrator of bot's community and a key from https://vkhost.github.io/, bound to your personal account.  
Supply that key as -ks, and every Friday morning you'll have a board game query in your VK chat!


### Pipeline
Bot wil run until it's interrupted or closed

## Currently supported features
- Sending prompts to a chat:
  - "Good morning, ..."
  - "Board game of the day: ..." 
    - "ru" and "en" languages
  - "Good night, ..."
- Sending random photos from a specified folder, if that folder path is specified
- Creating configurable polls as a bot's community administrator

## Planned features
- [BoardGameGeek XML API](https://boardgamegeek.com/wiki/page/BGG_XML_API#) integration
  - Automatic "Board game of the day" acquiring
- Stable diffusion [CPU (OpenVINO)](https://github.com/bes-dev/stable_diffusion.openvino) and [GPU (streamline)](https://github.com/CompVis/stable-diffusion) integration 
  - Picture generation from "Board game of the day" prompt
  - Random board game concepts?
- Multiple language translation (EN-RU primarily), not only board games' names
- Various chat integrations
  - Answers to a keyword
  - Board game search engine?
  - docker?