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

def parse_args():
    # Returns arguments as a dictionary
    
    parser = argparse.ArgumentParser(description="\nBoard game vk bot", formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=72))

    parser.add_argument("-k", "--key",          default="",type = str, required=True, help="API key")
    parser.add_argument("-gid", "--group-id",   default=0, type = int, required=True, help="ID of the community that bot belongs to")
    parser.add_argument("-cid", "--chat-id",    default=0, type = int, required=True, help="ID of the chat that bot will be sending messages to")
    parser.add_argument("-cpeer", "--chat-peer",default=0, type = int, required=True, help="PEER of the chat that bot will be sending messages to")
    parser.add_argument("-ph", "--photo-dir",   default=".",type = str, help="Directory where random photos that can be posted will be stored")

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
    photo_path = f"{photo_root}/{random.choice(photo_list)}"
    print(photo_path) 
    return photo_path
def get_photo_attachment(vk, photo_path):
    """
    Uploads a photo to a hidden album in VK and returns an attachment string.

    :param vk: VK API object
    :param photo_path: path to the photo to upload
    :return: attachment string for the uploaded photo
    """
    
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
    
    photo_upload = vk.photos.saveMessagesPhoto(server = response["server"], photo=response["photo"], hash=response["hash"])[0]
    print(photo_upload)
    owner_id = photo_upload["owner_id"]
    photo_id = photo_upload["id"]
    
    attachment = f"photo{owner_id}_{photo_id}"
    
    return attachment

nicknames_morning = [
    ", Феликс, земля тебе пухом", 
    ", зависимые от пиццы", 
    ".", 
    ". Есть предложения по новым настолкам?", 
    " любителям потупить в еврики", 
    ". Че, в субботу партеечку в Покорение Марса на 7 часов?)", 
    ". Когда новые чудеса напечатаете?", 
    "!", 
    "?"
    ]
hellos = [
    ", любители настольных игр! 🎲",
    ", герои настольных полей! 🏰",
    ", мастера стратегии! 🧠",
    ", чемпионы дружелюбных сражений! 🏆",
    ", исследователи игровых миров! 🌐",
    ", игровые архитекторы! 🏛️",
    ", знатоки настольных хитростей! 🔍",
    ", волшебники игральных карт! 🃏",
    ", командиры дипломатических миссий! 🤝",
    ", стратегические умы искусства настольных игр! 🎯",
    ", лорды игровых доминионов! 👑",
    ", бесстрашные путешественники в мире настольных приключений! 🌍",
    ", архитекторы настольных империй! 🏰",
    ", владыки карточных стратегий! 🃏",
    ", гении игрового мастерства! 🧠",
    ", магистры кубиков и костей! 🎲",
    ", капитаны игровых флотов! ⚓",
    ", дипломаты игровых переговоров! 🤝",
    ", короли игровых столов! 👑",
    ", творцы игровых легенд! 📜",
    ", герои настольных квестов! 🗝️",
    ", стратегические мозговые штурмы! 🤔",
    ", маги игровых заклинаний! 🧙",
    ", владыки деревянных досок! 🪑",
    ", защитники игровых королевств! 🛡️",
    ", победители в битве за настольные территории! 🗺️",
    ", звезды игрового небосклона! ⭐",
    ", карточные магнаты! 💳",
    ", архитекторы домов игральных карт! 🏠",
    ", гении игрового планирования! 📐",
    ", адмиралы игровых флотов! 🚢",
    ", магистры стратегии и тактики! 📚",
    ", вожди настольных племен! 👥",
    ", чемпионы карточных сражений! 🏆",
    ", владыки игровых миров! 🌍",
    ", друзья дома игральных карт! 🃏",
    ", капитаны игровых кораблей! 🚢",
    ", архитекторы настольных крепостей! 🏰",
    ", рыцари игровых доспехов! ⚔️",
    ", магистры игровых ходов! 🎲",
    ", владыки кубиков и костей! 🎲",
    ", капитаны игровых экспедиций! 🚀",
    ", архитекторы игровых лабиринтов! 🌀",
    ", великие стратеги игровых полей! 🌐",
    ", легендарные воины карточных битв! ⚔️",
    ", владыки настольных игр! 👑",
    ", путешественники по доске судьбы! 🛣️",
    ", магистры настольных магии! 🧙",
    ", короли игровых стратегий! 👑",
    ", войны игровых миров! ⚔️",
    ", герои настольных эпопей! 📜",
    ", игровые архитекторы историй! 🏰",
    ", владыки дипломатических игр! 🤝",
    ", мудрые кураторы настольных судеб! ⚖️",
    ", великие творцы игровых миров! 🌐",
    ", магистры игровых иллюзий! 🎭",
    ", герои настольных квестов и приключений! 🗺️",
    ", владыки игровых доминионов! 👑",
    ", архитекторы игровых эпопей! 🏛️",
    ", защитники игровых королевств! 🏰",
    ", капитаны карточных судов! ⚓",
    ", магистры дома игровых карт! 🏠",
    ", чемпионы настольных сражений! 🏆",
    ", владыки игровых хроник! 📖",
    ", воины игровых доменов! ⚔️",
    ", архитекторы игровых стратегий! 📐",
    ", магистры карточных историй! 📜",
    ", короли игровых доминионов! 👑",
    ", великие стратеги настольных полей! 🌐",
    ", легендарные капитаны карточных флотов! ⚓",
    ", владыки игровых доспехов! 🛡️",
    ", маги игровых заклинаний! 🧙",
    ", герои настольных кубиков и костей! 🎲",
    ", путеводители по лабиринтам настольных игр! 🌀",
    ", стратегические мозговые штурмы! 🤔",
    ", вожди настольных племен! 👥",
    ", чемпионы карточных сражений! 🏆",
    ", владыки игровых миров! 🌍",
    ", друзья дома игральных карт! 🃏",
    ", капитаны игровых кораблей! 🚢",
    ", архитекторы настольных крепостей! 🏰",
    ", рыцари игровых доспехов! ⚔️",
    ", магистры игровых ходов! 🎲",
    ", владыки кубиков и костей! 🎲",
    ", капитаны игровых экспедиций! 🚀",
    ", архитекторы игровых лабиринтов! 🌀",
    ", великие стратеги игровых полей! 🌐",
    ", легендарные воины карточных битв! ⚔️",
    ", владыки настольных игр! 👑",
    ", путешественники по доске судьбы! 🛣️",
    ", магистры настольных магии! 🧙",
    ", короли игровых стратегий! 👑",
    ", войны игровых миров! ⚔️",
    ", герои настольных эпопей! 📜",
    ", игровые архитекторы историй! 🏰",
    ", владыки дипломатических игр! 🤝",
    ", мудрые кураторы настольных судеб! ⚖️",
    ", великие творцы игровых миров! 🌐",
    ", магистры игровых иллюзий! 🎭",
    ", герои настольных квестов и приключений! 🗺️",
    ", владыки игровых доминионов! 👑",
    ", архитекторы игровых эпопей! 🏛️",
    ", защитники игровых королевств! 🏰",
    ", капитаны карточных судов! ⚓",
    ", любители настольных игр! 😊",
    ", друзья настольных приключений! 😄",
    ", герои настольных битв! 🛡️",
    ", мастера настольных стратегий! 🎲",
    ", стражи настольных карт! 🃏",
    ", покорители настольных досок! 🎮",
    ", чемпионы настольных сражений! 🏆",
    ", волшебники настольных реальностей! ✨",
    ", джентльмены и дамы настольных игр! 👫",
    ", владыки настольных территорий! 👑",
    ", игровые стратеги! 🎯",
    ", борцы за настольное владение! 🏰",
    ", настольные архитекторы! 🏗️",
    ", хозяева настольных карт! 🗺️",
    ", любители настольных ходов! 🚶‍♂️",
    ", настольные герои! 🦸‍♂️",
    ", завсегдатаи настольных игр! 🎲",
    ", мудрецы настольных правил! 📜",
    ", исследователи настольных миров! 🔍",
    ", великие игроманы! 🎭",
    ", настольные философы! 🤔",
    ", властители настольных доминант! 👊",
    ", игровые архитекторы! 🏰",
    ", стратегические маги! 🧙",
    ", виртуозы настольных планов! 🎨",
    ", покорители настольных лабиринтов! 🌀",
    ", любители тактических настольных решений! 🤓",
    ", капитаны настольных флотов! ⚓",
    ", орды настольных варваров! 🏹",
    ", настольные гении! 🧠",
    ", архитекторы игровых миров! 🌐",
    ", креативные мозаичисты настольных игр! 🎨",
    ", стратегические волшебники! ✨",
    ", покорители настольных королевств! 👑",
    ", дипломаты настольных столов! 🤝",
    ", владыки кубиков! 🎲",
    ", настольные интеллектуалы! 🧠",
    ", хранители настольных тайн! 🕵️",
    ", герои деталей! 🧩",
    ", великие архитекторы настольных миров! 🌍"]
recomendations = [
    "Gloomhaven",
    "Twilight Imperium: Fourth Edition",
    "Through the Ages: A New Story of Civilization",
    "Brass: Birmingham",
    "Scythe",
    "Great Western Trail",
    "Gaia Project",
    "Pandemic Legacy: Season 1",
    "Terraforming Mars",
    "Mage Knight Board Game",
    "Spirit Island",
    "Dominant Species",
    "A Feast for Odin",
    "Lisboa",
    "Arkham Horror: The Card Game",
    "Root",
    "The Crew: Mission Deep Sea",
    "Eclipse: Second Dawn for the Galaxy",
    "Underwater Cities",
    "Dune: Imperium",
    "Twilight Struggle",
    "Viticulture: Essential Edition",
    "Anachrony",
    "The Gallerist",
    "Feast for Odin",
    "Dominion",
    "Concordia",
    "Architects of the West Kingdom",
    "7 Wonders Duel",
    "Brass: Lancashire",
    "Mombasa",
    "Through the Ages: A Story of Civilization",
    "Agricola",
    "Orléans",
    "Champions of Midgard",
    "Tzolk'in: The Mayan Calendar",
    "The Voyages of Marco Polo",
    "Puerto Rico",
    "Grand Austria Hotel",
    "Star Wars: Rebellion",
    "Five Tribes",
    "Eldritch Horror",
    "Blood Rage",
    "On Mars",
    "The 7th Continent",
    "Le Havre",
    "Everdell",
    "Clans of Caledonia",
    "Paladins of the West Kingdom",
    "Pax Pamir (Second Edition)",
    "Great Zimbabwe",
    "Troyes",
    "Praga Caput Regni",
    "Caverna: The Cave Farmers",
    "Keyflower",
    "Aeon's End",
    "Ora et Labora",
    "Teotihuacan: City of Gods",
    "Middara",
    "Anno 1800",
    "Under Falling Skies",
    "Maracaibo",
    "Brass: Lancashire",
    "Twice as Clever",
    "Pipeline",
    "Hansa Teutonica",
    "Kingdom Death: Monster",
    "Dwellings of Eldervale",
    "The Isle of Cats",
    "Viscounts of the West Kingdom",
    "Lost Ruins of Arnak",
    "The Quacks of Quedlinburg",
    "The Castles of Burgundy",
    "Aeon's End: Legacy",
    "Mage Knight: Ultimate Edition",
    "Eclipse",
    "Paladins of the West Kingdom",
    "Grand Austria Hotel",
    "Nemesis",
    "Lisboa",
    "Concordia",
    "The Gallerist",
    "Great Western Trail",
    "Architects of the West Kingdom",
    "Dominant Species",
    "Aeon's End: Legacy",
    "Root",
    "Eldritch Horror",
    "Terraforming Mars",
    "Champions of Midgard",
    "Dominion",
    "Brass: Lancashire",
    "Five Tribes",
    "The Voyages of Marco Polo",
    "Teotihuacan: City of Gods",
    "Orléans",
    "Scythe",
    "Pandemic Legacy: Season 1",
    "Arkham Horror: The Card Game",
    "Twilight Struggle",
    "7 Wonders Duel",
    "Everdell",
    "Paladins of the West Kingdom",
    "Clans of Caledonia",
    "Le Havre",
    "Agricola",
    "Blood Rage",
    "The Castles of Burgundy",
    "On Mars",
    "Caverna: The Cave Farmers",
    "Twilight Imperium: Fourth Edition",
    "Anachrony",
    "Maracaibo",
    "Kingdom Death: Monster",
    "Dwellings of Eldervale",
    "The Isle of Cats",
    "Viscounts of the West Kingdom",
    "Lost Ruins of Arnak",
    "The Quacks of Quedlinburg",
    "The Crew: The Quest for Planet Nine",
    "Under Falling Skies",
    "Twice as Clever",
    "Pipeline",
    "Hansa Teutonica",
    "Nemesis",
    "Aeon's End",
    "Ora et Labora",
    "Underwater Cities",
    "Middara",
    "Anno 1800"
]
recomendations_ru = [
     "Мрачная Гавань",
     "Сумеречная Империя: Четвертое издание",
     "Сквозь века: новая история цивилизации",
     "Брасс: Бирмингем",
     "Серп",
     "Великая Западная тропа",
     "Проект Гайя",
     "Наследие пандемии: 1 сезон",
     "Терраформирование Марса",
     "Настольная игра маг-рыцарь",
     "Остров духов",
     "Доминантные виды",
     "Во Славу Одина",
     "Лиссабон",
     "Ужас Аркхэма: Карточная игра",
     "Корни",
     "Экипаж: Миссия в глубоком море",
     "Затмение: Второй рассвет галактики",
     "Подводные города",
     "Дюна: Империум",
     "Сумеречная борьба",
     "Виноградарство: Основное издание",
     "Анахронность",
     "Галерист",
     "Доминион",
     "Конкордия",
     "Архитекторы Западного Королевства",
     "7 чудес: дуэль",
     "Брасс: Ланкашир",
     "Момбаса",
     "Сквозь века: история цивилизации",
     "Агрикола",
     "Орлеан",
     "Чемпионы Мидгарда",
     "Цзолк'ин: Календарь майя",
     "Путешествия Марко Поло",
     "Пуэрто-Рико",
     "Отель Гранд Австрия",
     "Звездные войны: Восстание",
     "Пять племен",
     "Древний ужас",
     "Кровавая ярость",
     "На Марсе",
     "7-й континент",
     "Le Havre",
     "Эверделл",
     "Кланы Каледонии",
     "Паладины Западного Королевства",
     "Пакс Памир (Второе издание)",
     "Великий Зимбабве",
     "Труа",
     "Прага Капут Регни",
     "Каверна: Пещерные фермеры",
     "Ключевой цветок",
     "Конец Эона",
     "Ора и Лабора",
     "Теотиуакан: Город богов",
     "Миддара",
     "Анно 1800",
     "Под падающим небом",
     "Маракайбо",
     "Брасс: Ланкашир",
     "Дважды умнее",
     "Трубопровод",
     "Ганза Тевтоника",
     "Королевство Смерти: Монстр",
     "Жилища Элдервейла",
     "Остров кошек",
     "Виконты Западного королевства",
     "Затерянные руины Арнака",
     "Кведлинбургские шарлатаны",
     "Замки Бургундии",
     "Конец Эона: Наследие",
     "Рыцарь-маг: Ultimate Edition",
     "Затмение",
     "Немезида",
     "Лиссабон",
     "Галерист",
     "Миддара"
]

facts = [
    "Игра 'Ticket to Ride' была выпущена в 2004 году и стала популярной в настольном сообществе.",
    "В 2005 году вышла 'Twilight Imperium: Third Edition', ставшая культовой в жанре настольных стратегий.",
    "Игра 'Agricola', выпущенная в 2007 году, стала известной своей глубокой стратегией в фермерской тематике.",
    "В 2005 году была выпущена 'Betrayal at House on the Hill', где игроки строят дом и сталкиваются с предательством.",
    "Игра 'Dominion', выпущенная в 2008 году, внесла свой вклад в популяризацию доминионов - игр, где строится колода.",
    "В 2011 году вышла 'Eclipse', настольная игра об космическом завоевании и дипломатии.",
    "Игра '7 Wonders', выпущенная в 2010 году, стала одной из самых успешных карточных игр за последнее десятилетие.",
    "В 2008 году вышла 'Stone Age', настольная игра, в которой игроки управляют древним племенем.",
    "Игра 'Pandemic', выпущенная в 2008 году, позволяет игрокам объединить усилия для борьбы с эпидемией.",
    "В 2013 году была выпущена 'Splendor', где игроки соревнуются за драгоценные камни и развивают свои торговые империи.",
    "Игра 'Codenames', появившаяся в 2015 году, стала хитом благодаря своей уникальной комбинации слов и шпионского действия.",
    "В 2007 году вышла 'Race for the Galaxy', настольная игра о колонизации космоса.",
    "Игра 'Small World', выпущенная в 2009 году, предоставляет игрокам управление различными фэнтезийными расами.",
    "В 2014 году вышла 'Dead of Winter: A Crossroads Game', комбинирующая выживание и зомби-апокалипсис в настольном формате.",
    "Игра 'Dixit', выпущенная в 2008 году, стала известной своей креативной механикой и иллюстрациями",
    "Игра 'Codenames', выпущенная в 2015 году, получила множество наград, включая Spiel des Jahres.",
    "В 2016 году появилась 'Scythe', настольная игра, сочетающая в себе стратегию и альтернативную историю.",
    "Игра 'Pandemic Legacy: Season 1', выпущенная в 2015 году, стала первой настольной игрой с изменяемым сюжетом.",
    "В 2017 году вышла 'Gloomhaven', настольная игра, ставшая феноменом среди любителей настольных стратегий.",
    "Игра 'Terraforming Mars', выпущенная в 2016 году, получила признание за свою глубокую стратегию и научно-фантастическую тематику.",
    "В 2015 году появилась 'Codenames', карточная игра, ставшая хитом благодаря своей простоте и вариативности.",
    "Игра 'Scythe', выпущенная в 2016 году, предложила игрокам уникальное сочетание механик и красочный альтернативный мир.",
    "В 2015 году вышла '7 Wonders Duel', карточная игра для двух игроков, получившая множество положительных отзывов.",
    "Игра 'Pandemic Legacy: Season 2', продолжение первого сезона, была выпущена в 2017 году и продолжила популярность серии.",
    "В 2015 году появилась 'Blood Rage', настольная игра в жанре 'Доски управления армией', завоевавшая любовь игроков.",
    "Игра 'Star Wars: Rebellion', выпущенная в 2016 году, позволяет игрокам пережить эпические сражения во вселенной Star Wars.",
    "В 2017 году вышла 'Kingdomino', настольная игра, получившая премию Spiel des Jahres за лучшую игру года.",
    "Игра 'Azul', выпущенная в 2017 году, стала хитом благодаря своей красочной мозаичной механике и простым правилам.",
    "В 2016 году появилась 'Great Western Trail', настольная игра об эпохе постройки железных дорог в США.",
    "Игра 'Clank! A Deck-Building Adventure', выпущенная в 2016 году, сочетает в себе строительство колоды и элементы приключения.",
    "В 2015 году вышла 'Potion Explosion', настольная игра с уникальной механикой создания волшебных зелий.",
    "Игра 'The Crew: The Quest for Planet Nine', выпущенная в 2019 году, стала популярной среди любителей кооперативных игр.",
    "В 2016 году появилась 'Terraforming Mars', настольная игра, ставшая хитом благодаря своей научно-фантастической тематике.",
    "Игра 'Azul: Summer Pavilion', выпущенная в 2019 году, является продолжением успешной игры 'Azul'.",
    "В 2017 году вышла 'Gloomhaven', настольная игра, ставшая феноменом среди любителей настольных стратегий.",
    "Игра 'Root', выпущенная в 2018 году, предлагает уникальный опыт в мире лесных обитателей и политических интриг.",
    "В 2018 году появилась 'Everdell', настольная игра с красочным дизайном, в которой игроки строят свой город.",
    "Игра 'Underwater Cities', выпущенная в 2018 году, погружает игроков в строительство подводных городов и управление ресурсами.",
    "В 2018 году вышла 'The Mind', уникальная карточная игра, в которой игроки сотрудничают, не обмениваясь словами.",
    "Игра 'Architects of the West Kingdom', выпущенная в 2018 году, позволяет игрокам стать архитекторами средневековых поселений.",
    "В 2018 году появилась 'Chronicles of Crime', настольная игра с использованием виртуальной реальности для расследования преступлений.",
    "Игра 'Brass: Birmingham', выпущенная в 2018 году, является обновленным вариантом классической игры о промышленном развитии.",
    "В 2019 году вышла 'Wingspan', настольная игра о наблюдении за птицами и создании экологически устойчивого среды.",
    "Игра 'Teotihuacan: City of Gods', выпущенная в 2018 году, переносит игроков в древний мир строительства пирамид и развития цивилизации.",
    "В 2019 году появилась 'Paladins of the West Kingdom', настольная игра о защите королевства и строительстве крепостей.",
    "Игра 'Root: The Underworld Expansion', выпущенная в 2019 году, расширяет мир 'Root' новыми фракциями и возможностями.",
    "В 2018 году вышла 'Cryptid', настольная игра об исследовании загадочных существ и поиске их местоположения.",
    "Игра 'The Quacks of Quedlinburg', выпущенная в 2018 году, позволяет игрокам стать врачами-шарлатанами и готовить зелья.",
    "В 2019 году появилась 'Res Arcana', настольная игра о магии, ресурсах и стратегическом планировании.",
    "Игра 'Parks', выпущенная в 2019 году, вдохновлена национальными парками США и приглашает игроков в путешествие по природе.",
    "В 2018 году вышла 'Everdell: Pearlbrook', первое дополнение к игре 'Everdell' с новыми расами и механиками.",
    "Игра 'Tapestry', выпущенная в 2019 году, предлагает игрокам вести свою цивилизацию через века и достигнуть процветания.",
    "В 2018 году появилась 'Just One', кооперативная вечеринка с карточными загадками и минимальным количеством компонентов.",
    "Игра 'Wingspan: European Expansion', выпущенная в 2019 году, расширяет мир 'Wingspan' новыми видами птиц и регионами.",
    "В 2018 году вышла 'Chronicles of Crime: Noir', дополнение к игре 'Chronicles of Crime' с новыми делами и персонажами.",
    "Игра 'Dune: Imperium', выпущенная в 2020 году, основана на культовом научно-фантастическом романе Фрэнка Герберта.",
    "В 2020 году появилась 'Lost Ruins of Arnak', настольная игра, сочетающая элементы джунглей, археологии и стратегии.",
    "Игра 'Calico', выпущенная в 2020 году, предоставляет игрокам возможность создавать уникальные покрывала для кошачьих друзей.",
    "В 2021 году вышла 'The Crew: Mission Deep Sea', дополнение к оригинальной космической карточной игре 'The Crew'.",
    "Игра 'Viscounts of the West Kingdom', выпущенная в 2020 году, является частью серии о строительстве королевства в средневековье.",
    "В 2020 году появилась 'Fort', настольная игра, вдохновленная детством и поисками сокровищ.",
    "Игра 'Dwellings of Eldervale', выпущенная в 2020 году, сочетает в себе элементы стратегии, фэнтези и героических приключений.",
    "В 2021 году вышла 'The Isle of Cats: Don't forget the kittens!', дополнение к игре 'The Isle of Cats' с новыми задачами и котятами.",
    "Игра 'Beyond the Sun', выпущенная в 2020 году, позволяет игрокам исследовать космос и строить космические империи.",
    "В 2021 году появилась 'Oath: Chronicles of Empire and Exile', настольная игра с уникальной системой изменяемого мира.",
    "Игра 'Marvel United', выпущенная в 2020 году, позволяет игрокам собирать команду супергероев Marvel и сражаться с злодеями.",
    "В 2020 году вышла 'The Search for Planet X', настольная игра, где игроки занимаются астрономическими исследованиями.",
    "Игра 'Praga Caput Regni', выпущенная в 2020 году, переносит игроков в средневековый Прага, где они строят город.",
    "В 2021 году появилась 'Lost Ruins of Arnak: Expedition Leaders', дополнение к игре 'Lost Ruins of Arnak' с новыми лидерами.",
    "Игра 'Viscounts of the West Kingdom: Tomesaga', выпущенная в 2020 году, представляет собой кампанию с книгами и тайнами.",
    "В 2021 году вышла 'Dune: Imperium - Rise of Ix', дополнение к игре 'Dune: Imperium' с новыми фракциями и картами.",
    "Игра 'Summoner Wars: Second Edition', выпущенная в 2021 году, является переизданием популярной карточной стратегии.",
    "В 2020 году появилась 'Twisted Fables', настольная игра, в которой классические сказочные персонажи вступают в сражение.",
    "Игра 'Endless Winter: Paleoamericans', выпущенная в 2021 году, предлагает уникальный опыт в мире древних американцев.",
    "В 2020 году вышла 'Stellar', карточная игра, посвященная исследованию космоса и открытию новых галактик.",
    "'Scythe' предлагает увлекательное сочетание стратегии и альтернативной истории.",
    "'Everdell' поразит вас красочным дизайном и возможностью строить свой город.",
    "'Lost Ruins of Arnak' перенесет вас в мир джунглей, археологии и стратегических решений.",
    "'The Crew: Mission Deep Sea' – космическая карточная игра с приключенческим настроением и кооперативным геймплеем.",
    "'Dune: Imperium' основана на культовом научно-фантастическом романе и предлагает уникальный опыт.",
    "'Calico' позволяет вам создавать уникальные покрывала для кошачьих друзей в уютной атмосфере.",
    "'Beyond the Sun' предоставляет возможность исследовать космос и строить космические империи.",
    "'A Feast for Odin' позволяет вам строить свое поселение и управлять ресурсами в средневековье.",
    "'Marvel United' предлагает собрать команду супергероев Marvel и сразиться с злодеями.",
    "'Twilight Imperium: Fourth Edition' – это эпическая космическая сага с длительными сражениями за галактику.",
    "'Oath: Chronicles of Empire and Exile' предлагает уникальную систему изменяемого мира и стратегии.",
    "'The Isle of Cats: Don't forget the kittens!' – дополнение к игре с новыми задачами и милыми котятами.",
    "'Dwellings of Eldervale' сочетает стратегию, фэнтези и героические приключения в увлекательной форме.",
    "'Viscounts of the West Kingdom' представляет строительство королевства в средневековье с книгами и тайнами.",
    "'The Crew: The Quest for Planet Nine' – кооперативная игра с путешествием в космос в поисках загадочной планеты.",
    "'Praga Caput Regni' переносит игроков в средневековую Прагу с элементами стратегии и развития.",
    "'Wingspan: European Expansion' расширяет мир 'Wingspan' новыми видами птиц и регионами.",
    "'Summoner Wars: Second Edition' – переиздание популярной карточной стратегии с улучшенными правилами.",
    "'Endless Winter: Paleoamericans' предлагает уникальный опыт в мире древних американцев и стратегии.",
    "'Stellar' – карточная игра, посвященная исследованию космоса и открытию новых галактик.",
    ]

def main():
    args = parse_args();
    print(args)
    
    key = args.key
    chat_id = args.chat_id
    chat_peer = args.chat_peer
    photo_root = args.photo_dir
        
    vk_session = vk_api.VkApi(token=key)
    vk = vk_session.get_api()
    
    print(f"hellos length: {len(hellos)}")
    print(f"facts length: {len(facts)}")
    print(f"recomendations length: {len(recomendations)}")
    print(f"recomendations_ru length: {len(recomendations_ru)}")
    print(f"photos length: {len(os.listdir(photo_root))}")
    
    time_now = time.localtime()
    time_prev = time_now
   
    # Каждую секунду проверять, не настало ли время, и утром в 10:00 отправлять сообщение из списка
    while(True):
        time_now = time.localtime()
        
        # Каждую секунду
        if(time_now.tm_sec != time_prev.tm_sec):
            if(time_now.tm_sec % 60 == 0):
                print("tick/60, time: "+time.strftime("%a %b %d %H:%M:%S %Y", time_now))
            # Изначально пул сообщений пустой            
            msg_entries = {}
            
            # Проверить всякие условия
            if(check_morning(time_now)):
                print("утро")
                msg_entries[f"Доброе утро{random.choice(hellos)}"] = ""
            if(check_friday_poll(time_now)):
                print("опрос")
                msg_entries["А опрос создавать кто-то будет?"] = ""
            if(check_afternoon(time_now)):
                print("полдень")
                msg_entries[f"Настолка дня: {random.choice(recomendations_ru)}"] = ""
            if(check_evening(time_now)):
                print("вечер")
                # Send a photo if photo_root is not working directory
                if(photo_root != "."):
                    msg_entries["Иллюстрация дня:"] = get_photo_attachment(vk, get_photo_path(photo_root))
            if(check_goodnight(time_now)):
                print("ночи")
                msg_entries[f"Спокойной ночи{random.choice(hellos)}"] = ""
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