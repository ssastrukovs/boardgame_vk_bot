"""
Board game vk bot: send random board game prompts to vk group chat
"""

from dataclasses import dataclass
import random
import time
import json
import os
import argparse

# csv parsing
import numpy as np
import vk_api

# POST to send a picture to vk API
import requests


def parse_args():
    """
    Returns arguments as a dictionary
    """

    parser = argparse.ArgumentParser(
        description="\nBoard game vk bot",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=72),
    )

    parser.add_argument(
        "-k", "--key", default="", type=str, required=True, help="API key"
    )
    parser.add_argument(
        "-gid",
        "--group-id",
        default=0,
        type=int,
        required=True,
        help="ID of the community that bot belongs to",
    )
    parser.add_argument(
        "-cid",
        "--chat-id",
        default=0,
        type=int,
        required=True,
        help="ID of the chat that bot will be sending messages to",
    )
    parser.add_argument(
        "-cpeer",
        "--chat-peer",
        default=0,
        type=int,
        required=True,
        help="PEER of the chat that bot will be sending messages to",
    )
    parser.add_argument(
        "-ph",
        "--photo-dir",
        default=".",
        type=str,
        help="Directory where random photos that can be posted will be stored",
    )
    parser.add_argument(
        "-hp",
        "--hello-prompts",
        default="db/hellos.csv",
        type=str,
        help='.csv file with hello prompts path, "db/hellos.csv" by default',
    )
    parser.add_argument(
        "-bgp",
        "--board-game-prompts",
        default="db/games.csv",
        type=str,
        help='.csv file with board games list path, "db/games.csv" by default',
    )
    parser.add_argument(
        "-lang",
        "--language",
        default="ru",
        type=str,
        choices=["en", "ru"],
        help="Language of choice. Currently 'ru' and 'en' are supported",
    )

    parser.add_argument(
        "-ks",
        "--key-stub",
        default="",
        type=str,
        help="Stub API key, for your admin account. \
        Needed for polls posting. Go to https://vkhost.github.io/ to get it",
    )
    parser.add_argument(
        "-pdb",
        "--poll-database",
        default="db/poll.csv",
        type=str,
        help="2d matrix for a poll, db/poll.csv by default. \
        First entry is a name, second entry is list of rows, \
        separated by spaces. NOTE! Only one row (poll) is supported for now",
    )

    return parser.parse_args()


def check_time(time_struct, hr, mint):
    """
    Checks if a given time struct is at a specific hour and minute.

    Parameters
    ----------
    time_struct : time.struct_time
        The time struct to check from time library.
    hr : int
        The hour to check for.
    mint : int
        The minute to check for.

    Returns
    -------
    bool
        Whether the time struct is at the specified hour and minute: true or false.
    """
    return (
        time_struct.tm_hour == hr
        and time_struct.tm_min == mint
        and time_struct.tm_sec == 0
    )


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
    return time_struct.tm_wday == wd


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
    return check_wd(time_struct, 4) and check_time(time_struct, 8, 10)


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
    """
    Uploads a photo to a hidden album in VK and returns an upload server response.

    :param vk: VK API object
    :param photo_path: path to the photo to upload
    :return: upload server response
    """
    hidden_album = vk.photos.getMessagesUploadServer()
    print(hidden_album["upload_url"])
    print(f"photo_path = {photo_path}")

    with open(photo_path, "rb") as f:
        response = json.loads(
            requests.post(
                url=hidden_album["upload_url"], files={"photo": f}, timeout=60
            ).content
        )

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
    response = json.loads("{}")
    while len(photo) == 0:
        response = upload_photo(vk, photo_path)
        photo = response["photo"]
        print(f"got photo ~~{photo}~~ len {len(photo)}")
        if len(photo):
            break

    photo_upload = vk.photos.saveMessagesPhoto(
        server=response["server"], photo=response["photo"], hash=response["hash"]
    )[0]
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

    poll = vk_stub.polls.create(
        owner_id=owner_id,
        question=poll_name,
        is_anonymous=0,
        add_answers=json.dumps(poll_matrix),
    )
    print(poll)

    poll_id = poll["id"]

    attachment = f"poll{owner_id}_{poll_id}"
    return attachment


@dataclass
class PollDescriptor:
    """
    Class for VK poll descriptor,
    bound by poll name, poll group id and poll
    configuration matrix
    """

    def __init__(self, group_id=0, poll_name="", poll_matrix=np.ndarray([])):
        self.group_id = group_id
        self.name = poll_name
        self.matrix = poll_matrix


class VkMsgQueue:
    """
    Class for VK photos queue, bound by token, chat id and peer.
    """

    msg_entries = {}

    def __init__(self, token="", chat_id=0, chat_peer=0):
        """
        Creates a new VK session with a given token
        that sends msgs to a given chat id and peer
        """
        self.token = token
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()
        self.chat_id = chat_id
        self.chat_peer = chat_peer

    def enqueue_msg(self, do_enqueue=True, msg=""):
        """
        Add a message to the queue.
        If do_enqueue is False, the message will not be sent
        """
        if not do_enqueue:
            return
        print(f"sending msg: {msg}")
        self.msg_entries[msg] = msg

    def enqueue_photo(self, do_enqueue=True, msg="", photo_root="."):
        """
        Add a message to the queue.
        If do_enqueue is False, the message will not be sent
        """
        if not do_enqueue or photo_root == ".":
            return
        print(f"sending photo: {msg}")
        self.msg_entries[msg] = get_photo_attachment(
            self.vk, get_photo_path(photo_root)
        )

    def enqueue_poll(
        self, do_enqueue=True, msg="", poll: PollDescriptor = PollDescriptor()
    ):
        """
        Add a poll to the queue.
        If do_enqueue is False, the poll will not be sent
        """
        if (
            not do_enqueue
            or poll.group_id == 0
            or poll.name == ""
            or poll.matrix.size == 0
        ):
            return
        print(f"sending poll: {msg}")
        self.msg_entries[msg] = get_poll_attachment(
            self.vk, poll.group_id, poll.name, poll.matrix
        )

    def clear_send_all(self):
        """
        Send all messages in the queue.
        """
        if self.token == "" or self.chat_id == 0 or self.chat_peer == 0:
            return
        for item in self.msg_entries.items():
            msgid = random.randint(1, 1000000000)
            message = item[0]
            attachment = item[1]
            if attachment == "":
                self.vk.messages.send(
                    chat_id=self.chat_id,
                    peer_id=self.chat_peer,
                    message=message,
                    random_id=msgid,
                )
            else:
                self.vk.messages.send(
                    chat_id=self.chat_id,
                    peer_id=self.chat_peer,
                    message=message,
                    attachment=attachment,
                    random_id=msgid,
                )

        self.msg_entries = {}

    def get_vk(self):
        """
        Return vk methods descriptor, stored in class
        """
        return self.vk


def main():
    """
    Main procedure.
    """

    args = parse_args()
    print(args)

    photo_root = args.photo_dir

    recomendations_en = []
    recomendations_ru = []

    # get databases
    hellos = []
    poll_descr = PollDescriptor()
    if args.hello_prompts != ".":
        hellos = np.genfromtxt(
            args.hello_prompts, delimiter=",", dtype=str, encoding="utf-8"
        )
    if args.board_game_prompts != ".":
        recomendations_en, recomendations_ru = np.genfromtxt(
            args.board_game_prompts,
            delimiter=",",
            dtype=str,
            unpack=True,
            encoding="utf-8",
        )
    if args.poll_database != ".":
        poll_name, poll_matrix = np.genfromtxt(
            args.poll_database, delimiter=",", dtype=str, unpack=True, encoding="utf-8"
        )
        poll_matrix = poll_matrix.split()
        poll_descr = PollDescriptor(args.group_id, poll_name, poll_matrix)

    # Login to group bot account for messages.send
    vk_queue_photos = VkMsgQueue(args.key, args.chat_id, args.chat_peer)

    # Login to a personal account for polls.create, etc.
    # To get that token - go to https://vkhost.github.io/
    # and specify "Wall" on a personal account in "Settings"
    vk_queue_polls = VkMsgQueue(args.key_stub, args.chat_id, args.chat_peer)

    print(f"hellos length: {len(hellos)}")
    print(f"recomendations length: {len(recomendations_en)}")
    print(f"recomendations_ru length: {len(recomendations_ru)}")
    print(f"photos length: {len(os.listdir(photo_root))}")

    # set recommendations language
    recomendations = []
    if args.language == "ru":
        recomendations = recomendations_ru
    if args.language == "en":
        recomendations = recomendations_en

    time_now = time.localtime()
    time_prev = time_now

    first_time = True

    # Every second send some kind of message
    while True:
        time_now = time.localtime()

        # Каждую секунду
        if time_now.tm_sec == time_prev.tm_sec:
            continue

        if time_now.tm_sec % 60 == 0:
            print("tick/60, time: " + time.strftime("%a %b %d %H:%M:%S %Y", time_now))

        # First time start indication
        vk_queue_photos.enqueue_photo(
            first_time,
            f"Запуск бота, время {time_now.tm_hour}:{time_now.tm_min}",
            photo_root,
        )
        first_time = False

        # Actual Sendings
        vk_queue_photos.enqueue_photo(
            check_morning(time_now), f"Доброе утро, {random.choice(hellos)}", photo_root
        )
        vk_queue_polls.enqueue_poll(
            check_friday_poll(time_now), "Отмечаемся", poll_descr
        )
        if len(recomendations) > 0:
            vk_queue_photos.enqueue_msg(
                check_afternoon(time_now),
                f"Настолка дня: {random.choice(recomendations)}",
            )
        vk_queue_photos.enqueue_photo(
            check_evening(time_now), "Иллюстрация дня:", photo_root
        )
        vk_queue_photos.enqueue_photo(
            check_goodnight(time_now),
            f"Спокойной ночи, {random.choice(hellos)}",
            photo_root,
        )

        # Send if we have any
        vk_queue_photos.clear_send_all()
        vk_queue_polls.clear_send_all()

        time_prev = time_now
        # maybe add asyncs
        time.sleep(0.2)


if __name__ == "__main__":
    main()
