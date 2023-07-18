lengthmarks_w_z = {
    # "ŗ": "r",
    # "Ŗ": "R",

# Ā
    "ah": "ā",
    "â": "ā",
    "à": "ā",
    "á": "ā",
    "ä": "ā",

# Ē
    "eh": "ē",
    "ê": "ē",
    "è": "ē",
    "é": "ē",
    "ë": "ē",

# Ī
    "ih": "ī",
    "î": "ī",
    "ì": "ī",
    "í": "ī",
    "ï": "ī",

# O
    "ô": "o",
    "ò": "o",
    "ó": "o",
    "ö": "o",
    "oh": "o",

# Ū
    "uh": "ū",
    "û": "ū",
    "ù": "ū",
    "ú": "ū",
    "ü": "ū",

# W, Z
    "w": "v",
    "z": "c",
}

z_cap = {
    "S ": "┌■",
    "S,": "┌²",
    "S.": "┌³",
    "S:": "┌¹",
    "S:": "┌·",
    "S!": "┌°",
    "S?": "┌┘",
    "S*": "┌×",
    "S/": "┌¤",
    "S»": "┌▓",
    'S"': '┌│',
    "S”": "┌┤",
    "S'": "┌┴",
    "S)": "┌├",
    "S-": "┌┬",

    "S": "Z",

    "┌■": "S ",
    "┌²": "S,",
    "┌³": "S.",
    "┌¹": "S:",
    "┌·": "S:",
    "┌°": "S!",
    "┌┘": "S?",
    "┌×": "S*",
    "┌¤": "S/",
    "┌▓": "S»",
    '┌│': 'S"',
    "┌┤": "S”",
    "┌┴": "S'",
    "┌├": "S)",
    "┌┬": "S-",
}

st_tzch_exc = {
    "greezt": "▲¶",
    "īdzt": "▲↨",
    "areizt": "▲↓",
    "lauzt": "▲←",  # Klaustiņš (no Gulbja Pēc 100 g.)

    # atžirgt, grāmatžurnāls/politžurnāls
    "atzchir": "▲▀",
    "tzchurn": "▲▄",
}

st_tzch_sch_zch = {
    "zt": "st",
    "tatzch": "tač",
    "atzch": "atš",
    "tzch": "č",
    "zch": "ž",
}

# atžirgt, grāmatžurnāls/politžurnāls
tzch = {
    "tzchurn": "tžurn",
    "atzchir": "atžir",
}

s_š_č = {
    "ş": "s",
    "tatsch": "tač",
    "atsch": "atš",
    "tsch": "č",
    "sch": "š",
}

prefixes = {
# UZ
    " us": " uz",
    "/us": "/uz",
    "«us": "«uz",
    '"us': '"uz',
    "„us": "„uz",
    "'us": "'uz",
    "(us": "(uz",
    "-us": "-uz",

# UZ
    " mazus": " mazuz",
    "/mazus": "/mazuz",
    "«mazus": "«mazuz",
    '"mazus': '"mazuz',
    "„mazus": "„mazuz",
    "'mazus": "'mazuz",
    "(mazus": "(mazuz",
    "-mazus": "-mazuz",

# NEUZ
    " neus": " neuz",
    "/neus": "/neuz",
    "«neus": "«neuz",
    '"neus': '"neuz',
    "„neus": "„neuz",
    "'neus": "'neuz",
    "(neus": "(neuz",
    "-neus": "-neuz",

# JĀUZ
    " jāus": " jāuz",
    "/jāus": "/jāuz",
    "«jāus": "«jāuz",
    '"jāus': '"jāuz',
    "„jāus": "„jāuz",
    "'jāus": "'jāuz",
    "(jāus": "(jāuz",
    "-jāus": "-jāuz",

# IZ
    " is": " iz",
    "/is": "/iz",
    "«is": "«iz",
    '"is': '"iz',
    "„is": "„iz",
    "'is": "'iz",
    "(is": "(iz",
    "-is": "-iz",

# IZ
    " mazis": " maziz",
    "/mazis": "/maziz",
    "«mazis": "«maziz",
    '"mazis': '"maziz',
    "„mazis": "„maziz",
    "'mazis": "'maziz",
    "(mazis": "(maziz",
    "-mazis": "-maziz",

# NEIZ
    " neis": " neiz",
    "/neis": "/neiz",
    "«neis": "«neiz",
    '"neis': '"neiz',
    "„neis": "„neiz",
    "'neis": "'neiz",
    "(neis": "(neiz",
    "-neis": "-neiz",

# JĀIZ
    " jāis": " jāiz",
    "/jāis": "/jāiz",
    "«jāis": "«jāiz",
    '"jāis': '"jāiz',
    "„jāis": "„jāiz",
    "'jāis": "'jāiz",
    "(jāis": "(jāiz",
    "-jāis": "-jāiz",

# AIZ
    " ais": " aiz",
    "/ais": "/aiz",
    "«ais": "«aiz",
    '"ais': '"aiz',
    "„ais": "„aiz",
    "'ais": "'aiz",
    "(ais": "(aiz",
    "-ais": "-aiz",

# AIZ
    " mazais": " mazaiz",
    "/mazais": "/mazaiz",
    "«mazais": "«mazaiz",
    '"mazais': '"mazaiz',
    "„mazais": "„mazaiz",
    "'mazais": "'mazaiz",
    "(mazais": "(mazaiz",
    "-mazais": "-mazaiz",

# NEAIZ
    " neais": " neaiz",
    "/neais": "/neaiz",
    "«neais": "«neaiz",
    '"neais': '"neaiz',
    "„neais": "„neaiz",
    "'neais": "'neaiz",
    "(neais": "(neaiz",
    "-neais": "-neaiz",

# JĀAIZ
    " jāais": " jāaiz",
    "/jāais": "/jāaiz",
    "«jāais": "«jāaiz",
    '"jāais': '"jāaiz',
    "„jāais": "„jāaiz",
    "'jāais": "'jāaiz",
    "(jāais": "(jāaiz",
    "-jāais": "-jāaiz",

# BEZ
    " mas": " maz",
    "/mas": "/maz",
    "«mas": "«maz",
    '"mas': '"maz',
    "„mas": "„maz",
    "'mas": "'maz",
    "(mas": "(maz",
    "-mas": "-maz",

# BEZ
    " bes": " bez",
    "/bes": "/bez",
    "«bes": "«bez",
    '"bes': '"bez',
    "„bes": "„bez",
    "'bes": "'bez",
    "(bes": "(bez",
    "-bes": "-bez",

    "iztab": "istab",
    "aizberg": "aisberg",
}

ee_exc_1 = {
    "neeee!": "☼☺",
    "neee!": "☼☻",
    " nee!": "☼♣",
    "/nee!": "☼♠",
    "«nee!": "☼•",
    '"nee!': "☼◘",
    "„nee!": "☼○",
    "'nee!": "☼◙",
    "(nee!": "☼♂",
    "-nee!": "☼♀",

    "neeeee": "☼♪", # neieie

    "neeee": "☼╬",
    "eeee": "☼═", # ieie

    "neee": "☼╠", # neie
    "iee": "☼╦",

    # neesmu, neej, neefektīvs, neelpo, neecēt
    " nees": "♫♥",
    "/nees": "♫♦",
    "«nees": "♫♣",
    '"nees': "♫♠",
    "„nees": "♫•",
    "'nees": "♫◘",
    "(nees": "♫○",
    "-nees": "♫◙",

    " neej": "►♥",
    "/neej": "►♦",
    "«neej": "►♣",
    '"neej': "►♠",
    "„neej": "►•",
    "'neej": "►◘",
    "(neej": "►○",
    "-neej": "►◙",

    " neef": "◄♥",
    "/neef": "◄♦",
    "«neef": "◄♣",
    '"neef': "◄♠",
    "„neef": "◄•",
    "'neef": "◄◘",
    "(neef": "◄○",
    "-neef": "◄◙",

    " neel": "↕♥",
    "/neel": "↕♦",
    "«neel": "↕♣",
    '"neel': "↕♠",
    "„neel": "↕•",
    "'neel": "↕◘",
    "(neel": "↕○",
    "-neel": "↕◙",

    " neecē": "‼♥",
    "/neecē": "‼♦",
    "«neecē": "‼♣",
    '"neecē': "‼♠",
    "„neecē": "‼•",
    "'neecē": "‼◘",
    "(neecē": "‼○",
    "-neecē": "‼◙",

    # neekranizēts, neekvivalents, neekvadoras/toriāls, neekonomiski, neekoloģiski, neeksistē
    "eekrani": "¶☺",
    "eekviv": "¶☻",
    "eekva": "¶♥",
    "eekono": "¶♦",
    "eekol": "¶♠",
    "eeksis": "¶♣",
}

ee_exc_2 = {
    "☼♪": "neieie",
    "☼╬": "neiee",
    "☼═": "ieie",
    "☼╠": "neie",
}