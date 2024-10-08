import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import time

# POST to send a picture to vk API 
import pycurl
from io import BytesIO
import json

# image file path getting
import os

# console arguments
import argparse

# csv parsing
import numpy as np

def parse_args():
    # Returns arguments as a dictionary
    
    parser = argparse.ArgumentParser(description="\nBoard game vk bot", formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=72))

    parser.add_argument("-k", "--key",          default="",type = str, required=True, help="API key")
    parser.add_argument("-gid", "--group-id",   default=0, type = int, required=True, help="ID of the community that bot belongs to")
    parser.add_argument("-cid", "--chat-id",    default=0, type = int, required=True, help="ID of the chat that bot will be sending messages to")
    parser.add_argument("-cpeer", "--chat-peer",default=0, type = int, required=True, help="PEER of the chat that bot will be sending messages to")
    parser.add_argument("-ph", "--photo-dir",   default=".",type = str, help="Directory where random photos that can be posted will be stored")
    parser.add_argument("-hp", "--hello-prompts",         default="db/hellos.csv",type = str, help=".csv file with hello prompts path, \"db/hellos.csv\" by default")
    parser.add_argument("-bgp", "--board-game-prompts",   default="db/games.csv", type = str, help=".csv file with board games list path, \"db/games.csv\" by default")
    parser.add_argument("-lang", "--language",   default="ru", type = str, choices=["en","ru"] ,help="Language of choice. Currently 'ru' and 'en' are supported")

    parser.add_argument("-ks", "--key-stub",   default="", type = str, help="Stub API key, for your admin account. Needed for polls posting. Go to https://vkhost.github.io/ to get it")
    parser.add_argument("-pdb", "--poll-database",   default="db/poll.csv", type = str, help="2d matrix for a poll, db/poll.csv by default. First entry is a name, second entry is list of rows, separated by spaces. NOTE! Only one row (poll) is supported for now")

    return parser.parse_args()

def check_time(time_struct, hr, min):
    """
    Checks if a given time struct is at a specific hour and minute.

    Parameters
    ----------
    time_struct : time.struct_time
        The time struct to check from time library.
    hr : int
        The hour to check for.
    min : int
        The minute to check for.

    Returns
    -------
    bool
        Whether the time struct is at the specified hour and minute: true or false.
    """
    return (time_struct.tm_hour == hr and time_struct.tm_min == min and time_struct.tm_sec == 0)
def check_wd(time_struct, wd):
    """
    Checks if a given time struct is on a specific weekday.

    Parameters
    ----------
    time_struct : time.struct_time
        The time struct to check from time library.
    wd : int
        The weekday to check for. Monday is 0 and Sunday is 6.

    Returns
    -------
    bool
        Whether the time struct is on the specified weekday: true or false.
    """
    return (time_struct.tm_wday == wd)
def check_morning(time_struct):
    """
    Checks if a given time struct is in the morning.

    Parameters
    ----------
    time_struct : time.struct_time
        The time struct to check from time library.

    Returns
    -------
    bool
        Whether the time struct is in the afternoon: true or false.
    """
    return check_time(time_struct, 8, 0)
def check_afternoon(time_struct):
    """
    Checks if a given time struct is in the afternoon.

    Parameters
    ----------
    time_struct : time.struct_time
        The time struct to check from time library.

    Returns
    -------
    bool
        Whether the time struct is in the afternoon: true or false.
    """
    return check_time(time_struct, 12, 30)
def check_evening(time_struct):
    """
    Checks if a given time struct is in the evening.

    Parameters
    ----------
    time_struct : time.struct_time
        The time struct to check from time library.

    Returns
    -------
    bool
        Whether the time struct is in the evening: true or false.
    """
    return check_time(time_struct, 17, 0)
def check_friday_poll(time_struct):
    """
    Checks if a given time struct is on a Friday morning.
    
    Parameters
    ----------
    time_struct : time.struct_time
        The time struct to check from time library.

    Returns
    -------
    bool
        Whether the time struct is on a Friday and at 8:10am: true or false.
    """
    return (check_wd(time_struct, 4) and check_time(time_struct, 8, 10))
def check_goodnight(time_struct):
    """
    Checks if a given time struct matches night time.

    Parameters
    ----------
    time_struct : time.struct_time
        The time struct to check from time library.

    Returns
    -------
    bool
        Whether the time struct matches night time: true or false.
    """
    return check_time(time_struct, 22, 0)

def get_photo_path(photo_root):
    """
    Returns a random photo path from the given photo directory.

    Parameters
    ----------
    photo_root : str
        The root directory of the photos.

    Returns
    -------
    str
        A random photo path from the given photo root directory.
    """
    photo_list = os.listdir(photo_root)
    photo_path = f"{photo_root}{random.choice(photo_list)}"
    print(photo_path) 
    return photo_path

def upload_photo(vk, photo_path):
    
    hidden_album = vk.photos.getMessagesUploadServer()
    print(hidden_album["upload_url"])
    
    response_buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.SSL_VERIFYPEER, 0);
    curl.setopt(curl.URL, hidden_album["upload_url"])
    curl.setopt(curl.POST, 1)
    curl.setopt(curl.HTTPPOST, [('photo', (curl.FORM_FILE, photo_path))])
    curl.setopt(curl.WRITEFUNCTION, response_buffer.write)
    curl.perform()
    bbuf = response_buffer.getvalue()
    response = json.loads(bbuf.decode('utf-8'))
    curl.close()
    
    print()
    print(response)
    print()
    print(response["server"])
    print()
    print(response["photo"])
    print()
    print(response["hash"])
    
    return response
def get_photo_attachment(vk, photo_path):
    """
    Uploads a photo to a hidden album in VK and returns an attachment string.

    :param vk: VK API object
    :param photo_path: path to the photo to upload
    :return: attachment string for the uploaded photo
    """
    photo = ""
    while(photo == ""):
        response = upload_photo(vk, photo_path)
        photo = response["photo"]
        if(photo != ""):
            break

    photo_upload = vk.photos.saveMessagesPhoto(server = response["server"], photo=response["photo"], hash=response["hash"])[0]
    print(photo_upload)
    owner_id = photo_upload["owner_id"]
    photo_id = photo_upload["id"]
    
    attachment = f"photo{owner_id}_{photo_id}"
    
    return attachment

def get_poll_attachment(vk_stub, group, poll_name, poll_matrix):
    """
    Creates a poll using the VK API stub (authenticated by your own account auth token, 
    get it on https://vkhost.github.io/) and returns an attachment string.

    :param vk_stub: VK API object
    :param group: ID of the group where the poll will be created
    :param poll_name: name of the poll
    :param poll_matrix: list of poll options, where each option is a string
    :return: attachment string for the created poll
    """
    owner_id = -int(group)
    
    poll = vk_stub.polls.create(owner_id=owner_id, question=poll_name, is_anonymous=0, add_answers=json.dumps(poll_matrix))
    print(poll)
    
    poll_id = poll["id"]
    
    attachment = f"poll{owner_id}_{poll_id}"
    return attachment

def main():
    args = parse_args();
    print(args)
    
    key = args.key
    chat_id = args.chat_id
    group_id = args.group_id
    chat_peer = args.chat_peer
    photo_root = args.photo_dir
    
    key_stub = args.key_stub
    
    recomendations_en = []
    recomendations_ru = []
    
    # get databases
    if(args.hello_prompts != "."):
        hellos =             np.genfromtxt(args.hello_prompts, delimiter=",", dtype=str, encoding='utf-8')
    if(args.board_game_prompts != "."):
        recomendations_en, recomendations_ru = np.genfromtxt(args.board_game_prompts, delimiter=",", dtype=str, unpack=True, encoding='utf-8')
    if(args.poll_database != "."):
        poll_name, poll_matrix = np.genfromtxt(args.poll_database, delimiter=",", dtype=str, unpack=True, encoding='utf-8')
        poll_matrix = poll_matrix.split()

    # Login to group bot account for messages.send
    vk_session = vk_api.VkApi(token=key)
    vk = vk_session.get_api()
    
    # Login to a personal account for polls.create, etc.
    # To get that token - go to https://vkhost.github.io/ and specify "Wall" on a personal account in "Settings" 
    stub_session = vk_api.VkApi(token=key_stub)
    vk_stub = stub_session.get_api()
    
    print(f"hellos length: {len(hellos)}")
    print(f"recomendations length: {len(recomendations_en)}")
    print(f"recomendations_ru length: {len(recomendations_ru)}")
    print(f"photos length: {len(os.listdir(photo_root))}")
    
    # set recommendations language
    if(args.language == "ru"):
        recomendations = recomendations_ru
    if(args.language == "en"):
        recomendations = recomendations_en
    
    time_now = time.localtime()
    time_prev = time_now
    
    first_time = True
   
    # Каждую секунду проверять, не настало ли время, и утром в 10:00 отправлять сообщение из списка
    while(True):
        time_now = time.localtime()
        
        # Каждую секунду
        if(time_now.tm_sec != time_prev.tm_sec):
            if(time_now.tm_sec % 60 == 0):
                print("tick/60, time: "+time.strftime("%a %b %d %H:%M:%S %Y", time_now))
            # Изначально пул сообщений пустой            
            msg_entries = {}
            if(first_time):
                 msg_entries[f"Запуск бота, время {time_now.tm_hour}:{time_now.tm_min}"] = get_photo_attachment(vk, get_photo_path(photo_root))
                 first_time = False
            # Проверить всякие условия
            if(check_morning(time_now)):
                print("утро")
                msg_entries[f"Доброе утро, {random.choice(hellos)}"] = get_photo_attachment(vk, get_photo_path(photo_root))
            if(check_friday_poll(time_now)):
                if(key_stub != ""):
                    print("опрос")
                    msg_entries["Отмечаемся"] = get_poll_attachment(vk_stub, group_id, poll_name, poll_matrix)
            if(check_afternoon(time_now)):
                print("полдень")
                if(len(recomendations) > 0):
                    msg_entries[f"Настолка дня: {random.choice(recomendations)}"] = ""
            if(check_evening(time_now)):
                print("вечер")
                # Send a photo if photo_root is not working directory
                if(photo_root != "."):
                    msg_entries["Иллюстрация дня:"] = get_photo_attachment(vk, get_photo_path(photo_root))
            if(check_goodnight(time_now)):
                print("ночи")
                msg_entries[f"Спокойной ночи, {random.choice(hellos)}"] = get_photo_attachment(vk, get_photo_path(photo_root))
            # Послать сообщения, если они есть
            if (len(msg_entries) > 0):
                for message in msg_entries:
                    id = random.randint(1, 1000000000)
                    attachment = msg_entries[message]
                    if(attachment == ""):
                        vk.messages.send(chat_id=chat_id, peer_id=chat_peer, message=message, random_id=id)
                    else:
                        vk.messages.send(chat_id=chat_id, peer_id=chat_peer, message=message, attachment=attachment, random_id=id)
            
        time_prev = time_now
        # Поспать 0.2 секунды
        time.sleep(0.2)
    
if __name__ == '__main__': 
    main()