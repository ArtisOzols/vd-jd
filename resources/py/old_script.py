def clean_words(text):
# Adds word or its part with letters to dictionary
# key - key to be added; val - value to be added; d - dictionary, letters - list of characters to add before or after key and val; before_key - add letters before (1) or after (0) key or val. 
    def add_letters(key, val, d, letters=[""], before_key=0):
        if before_key:
            for i in letters:
                d[i+key] = i+val
        else:
            for i in letters:
                d[key+i] = val+i
        return d

# Replaces words/substrings with starting or ending characters can be in front of words in a given text.
# key - word or its part to be transform; val - word or its part to be transform to; text - text to transform; starts_ends - add characters that are before or after word ("1" for adding them in front, "2" at the end, "0" before and after word) 
    def starts_ends_with(key, val, text, starts_ends=0):
        text = " " + text + " "
        s_list = [" ", "(", "[", '"', "/", "\n", "\t"] if starts_ends == 1 or starts_ends == 0 else [""]
        e_list = [" ", ",", ".", "!", "?", ":", ";", ")", "]", "/", "\n", "\t"] if starts_ends == 2 or starts_ends == 0 else [""]

        for s in s_list: 
            for e in e_list:
                text = text.replace(s + key + e, s + val + e)
                if starts_ends != 2:
                    symb_list = ["⌂", "☼", "𓀠", "𓀡", "𓀢", "𓀣", "𓀤", "𓀥", "𓀀", "𓀁", "𓀂", "𓀃", "𓀐", "𓀑", "𓀒", "𓀓", "𓀔", "𓀕", "𓀉", "𓀊", "𓀋", "𓀞", "𓀟", "𓁍", "𓁎", "𓊀", "𓊁", "𓊂", "𓊃", "𓊄", "𓊅", "𓊆", "𓊇", "𓊈", "𓊉", "𓊊", "𓊋", "𓊌", "𓊍", "𓊎", "𓊏", "𓊐", "𓊑", "𓊒", "𓊓", "𓊔", "𓊕", "𓊖", "𓊗", "𓊘", "𓊙", "𓊚", "𓊛", "𓊜", "𓊝", "𓊞", "𓊟", "𓁏", "𓁨", "𓁋", "𓁄", "𓁁", "𓏠", "𓏡", "𓏢", "𓏣", "𓏤", "𓏥", "𓏦", "𓏧", "𓏨", "𓏩", "𓏪", "𓏫", "𓏬", "𓏭", "𓏮", "𓏯", "𓏰", "𓏱", "𓏲", "𓏳", "𓏴", "𓏵", "𓏶", "𓏷", "𓏸", "𓏹", "𓏺", "𓏻", "𓏼", "𓏽", "𓏾", "𓏿", "𓐀", "𓐁", "𓐂", "𓐃", "𓐄", "𓐅", "𓐆", "𓐇", "𓐈", "𓐉", "𓐊", "𓐋", "𓐌", "𓐍", "𓐎", "𓐏"]
                    if not any([key.istitle(), key[0] in symb_list, key[0] == " "]):
                        text = text.replace(s + ("Ꞩ" if key[0] == "ẜ" else "S" if key[0] == "ſ" else key[0].capitalize())+key[1:] + e, s + ("Ꞩ" if val[0] == "ẜ" else "S" if val[0] == "ſ" else val[0].capitalize())+val[1:] + e)
        return text[1:-1]

# Adds exceptions for word transformation.
# e_list - list of words that will be added in dictionary; d - dictionary in witch exceptions will be added; decode - codes/decodes exceptions with symbol.
# Example (transforms all "f" into "ẜ", except word "febr"):
#   exceptions(["febr"], d, 0)            output: d = {"febr":"𓀠"}
#   d.update({"f": "ẜ"})                  output: d = {"febr":"𓀠", "f":"ẜ"}
#   exceptions(["febr"], d, 1)            output: d = {"febr":"𓀠", "f":"ẜ", "𓀠":"febr"}
# Symbols: https://www.fileformat.info/info/unicode/block/egyptian_hieroglyphs/utf8test.htm
    def exceptions(e_list, d, decode):
        e_list_title = []
        for i in e_list:
            if i[0] == " ":
                continue
            if i[0]=="ẜ":
                e_list_title.append("Ꞩ"+i[1:])
            elif i[0]=="ſ":
                e_list_title.append("S"+i[1:])
            else:
                e_list_title.append(i.capitalize())
        e_list = e_list_title + e_list
        
        symb_list = ["𓀠", "𓀡", "𓀢", "𓀣", "𓀤", "𓀥", "𓀀", "𓀁", "𓀂", "𓀃", "𓀐", "𓀑", "𓀒", "𓀓", "𓀔", "𓀕", "𓀉", "𓀊", "𓀋", "𓀞", "𓀟", "𓁍", "𓁎", "𓊀", "𓊁", "𓊂", "𓊃", "𓊄", "𓊅", "𓊆", "𓊇", "𓊈", "𓊉", "𓊊", "𓊋", "𓊌", "𓊍", "𓊎", "𓊏", "𓊐", "𓊑", "𓊒", "𓊓", "𓊔", "𓊕", "𓊖", "𓊗", "𓊘", "𓊙", "𓊚", "𓊛", "𓊜", "𓊝", "𓊞", "𓊟", "𓁏", "𓁨", "𓁋", "𓁄", "𓁁", "𓏠", "𓏡", "𓏢", "𓏣", "𓏤", "𓏥", "𓏦", "𓏧", "𓏨", "𓏩", "𓏪", "𓏫", "𓏬", "𓏭", "𓏮", "𓏯", "𓏰", "𓏱", "𓏲", "𓏳", "𓏴", "𓏵", "𓏶", "𓏷", "𓏸", "𓏹", "𓏺", "𓏻", "𓏼", "𓏽", "𓏾", "𓏿", "𓐀", "𓐁", "𓐂", "𓐃", "𓐄", "𓐅", "𓐆", "𓐇", "𓐈", "𓐉", "𓐊", "𓐋", "𓐌", "𓐍", "𓐎", "𓐏"]
        if len(e_list) > len(symb_list):
            symb_list = ["⌂"+i for i in symb_list] + ["☼"+i for i in symb_list] 
            
        i = 0
        if not decode:
            for key in e_list:
                d[key] = symb_list[i]
                i += 1
        else:
            for key in e_list:
                d[symb_list[i]] = key
                i += 1
        return d
            
    prefixes = ['Jahap', 'Jahat', 'Jahno', 'Jahsa', 'Jahais', 'Jahaiſ', 'jahais', 'jahaiſ', 'Jahis', 'Jahiſ', 'jahis', 'jahiſ', 'jahap', 'jahat', 'jahno', 'Jahpahr', 'jahpahr', 'Jahpa', 'jahpa', 'Jahpee', 'jahpee', 'Jahee', 'jahee', 'jahsa', 'Jahus', 'Jahuſ', 'jahus', 'jahuſ', 'jahẜa', 'Jahẜa', 'Neap', 'Neat', 'Neno', 'Nesa', 'Neais', 'Neaiſ', 'neais', 'neaiſ', 'Neis', 'Neiſ',  'neis', 'neiſ', 'neap', 'neat', 'neno', 'Nepahr', 'nepahr', 'Nepa', 'nepa', 'Nepee', 'nepee', 'Neee', 'neee', 'nesa', 'Neus', 'Neuſ', 'neus', 'neuſ', 'neẜa', 'Neẜa', 'Ap', 'At', 'Bes', 'Beſ', 'Jah', 'jah', 'Ne', 'ne', 'No', 'Sa', 'Ais', 'Aiſ', 'ais', 'aiſ', 'Is', 'Iſ', 'is', 'iſ', 'ap', 'at', 'bes', 'beſ', 'no', 'Pahr', 'pahr', 'Pa', 'pa', 'Pee', 'pee', 'Ee', 'ee', 'sa', 'Us', 'Uſ', 'us', 'uſ', 'ẜa', 'Ꞩa']
    vowels = ["a", "e", "i", "oh", "o", "u"]
    flexions_n_f = ["ahm", "ahs", "as", "ai", "u", "ah", "a"]
    flexions_n_m = ["ohs", "eem", "am", "ah", "us", "os", "oh", "o", "u", "s", "a", "i", ""]
    flexions_n_mf = ["ohs", "eem", "ahm", "ahs", "am", "ah", "ai", "os", "us", "as", "oh", "o", "u", "s", "a", "i", ""]
    flexions_a_m = ["ajahm", "ajahs", "ajohs", "ajeem", "ajam", "ajah", "ajos", "ajai", "ais", "ohs", "ahs", "ah", "oh", "ee", "os", "o"]
    flection_a_f = ["ehm", "ehs", "es", "ei", "eh", "e", "i", ]

    flexions_v_ = ["ehju", "ahm", "aht", "am", "u", "i", "a", ""]
    flexions_v_I = ['inu', 'inaht', 'inahm', 'ina', 'ihẜim', 'ihẜeet', 'ihẜi', 'ihẜchu', 'ihsim', 'ihseet', 'ihsi', 'ihschu', 'ihs', 'enu', 'enat', 'enam', 'en']
    flexions_v_II = ['ẜim', 'ẜeet', 'ẜi', 'ẜchu', 't', 'sim', 'seet', 'si', 'schu', 's', 'ju', 'ji', 'jat', 'jam', 'jaht', 'jahm', 'ja']
    flexions_v_III = ['ẜimees', 'ẜeetees', 'ẜees', 'ẜchos', 'simees', 'simees', 'seetees', 'sees', 'schos', 'jos', 'jees', 'jahtees', 'jahs', 'jahmees', 'damees']

    # https://www.lviap.lv/grammar/verbs/konjugacija/
    # https://laacz.lv/tmp/loc.php?

    vd0 = {
        "ā": "ah",
        "ē": "eh",
        "ī": "ih",
        "ū": "uh",
        "ş": "ẜ",
        "Ş": "Ꞩ",
    }
    exc = [" fm", " fon", " of ", " fakt", "fahſ", "fani", "fakult", "fabul", "fant", "fize", "feder", "fasahd", "faẜahd", "fafahd", "festi", "fefti", "feẜti", "finahl", "finan", "fili", "film", "firm", "fiſik", "form", "foto", "folkhl", "futb", "funkz", "front", "florenz", "flahz", "ahfrik", "draft", "defiz", "efekt", "infra", "infekzij", "kafij", "katastrof", "kataftrof", "kataẜtrof", "koef", "konflikt", "naft", "ofizi", "prof", "rudolf", "ruhdolf", "sfehr", "ẜfehr", "ffehr", " wef", " alfa", "asfalt", "affalt", "aẜfalt", "fran", " fr.", "febr", "friz", "fritsch", "frid", "frie", "freil", "nfrei", "freib", "freim", "feld", "firzk", "fabrik", "falzgr"]
    exc = exc + ["schihd", "schira"]
    exceptions(exc, vd0, 0)
    vd0.update({
            "ferti": "𓐧",
            "ferwi": "𓐨",    #serviss
            "ferb": "𓐩",
        "fer": "𓐦",
            "𓐧": "ẜerti",
            "𓐨": "ẜerwi",
            "𓐩": "ẜerb",

            "lafik": "𓐪",
            "lasfik": "𓐤",
            "laffik": "𓐤",
            "laẜfik": "𓐤",
            "ekfik": "𓐫",    #Meksika
            "fiksn": "𓐬",
            "fikfn": "𓐬",
            "fikẜn": "𓐬",
        "fik": "𓐥",      #identifik grafik kwalifik klasifik klaẜifik sertifik ẜertifik
            "𓐪": "laẜik",
            "𓐤": "laẜẜik",
            "𓐫": "ekẜik",
            "𓐬": "ẜikẜn",
    "f": "ẜ",
        "𓐦": "fer",
        "𓐥": "fik",

        " arveen": "𓐭",
        " Arveen": "♦𓐦",
        "nervu": "𓐮",
        "Nervu": "♦𓐥",
        "orvehģ": "𓐣",
    "rv": "w",
        "𓐭": " arween",
        "♦𓐦": " Arween",
        "𓐮": "nerwu",
        "♦𓐥": "Nerwu",
        "𓐣": "orwehģ",
        
        "eļved": "𓐢",
        "eemeļv": "𓐐",
        "auruļvad": "𓐑",
        "uļve": "𓐒",
        "pļveid": "𓐓",
        "araļv": "𓐔",
    "ļv": "w",
        "𓐢": "eļwed",
        "𓐐": "eemeļw",
        "𓐑": "auruļwad",
        "𓐒": "uļwe",
        "𓐓": "pļweid",
        "𓐔": "araļw",

    "vv": "w",

    " sa - ": " ẜa",
    " sa -": " ẜa",
    " sa – ": " ẜa",
    " sa –": " ẜa",

    " ro - ": " ro",
    " ro -": " ro",
    " ro – ": " ro",
    " ro –": " ro",

    ", ro ": ", ko ",
    " ro ": " no ",

    "ä": "â",
    "q": "g",
    "&gt;ņ": "iņ",
    "&gt;": ", ",
    ">": ", ",
    "v. t.": "u. t.",
    "v. z.": "u. z.",
    "sch": "ẜch",
    })
    exceptions(exc, vd0, 1)
    vd0.update({
    "fafahd": "faẜahd",
    "fasahd": "faẜahd",
    "fefti": "feẜti",
    "festi": "feẜti",
    "kataftrof": "kataẜtrof",
    "katastrof": "kataẜtrof",
    "ffehr": "ẜfehr",
    "sfehr": "ẜfehr",
    "affalt": "aẜfalt",
    "asfalt": "aẜfalt",
    })

    vd_s_e_with = {}
    # add_letters("minn", "wiņņ", vd_s_e_with, ["eem", "ahm", "ahs", "ẜch", "ai", "as", "ah", "am", "us", "os", "ohs", "i", "a", "u"])
    # add_letters("miņņ", "wiņņ", vd_s_e_with, ["eem", "ahm", "ahs", "ẜch", "ai", "as", "ah", "am", "us", "os", "ohs", "i", "a", "u"])
    # add_letters("winn", "wiņņ", vd_s_e_with, ["eem", "ahm", "ahs", "ẜch", "ai", "as", "ah", "am", "us", "os", "ohs", "i", "a", "u"])
    # add_letters("min", "wiņ", vd_s_e_with, ["eem", "ahm", "ahs", "ẜch", "ai", "as", "ah", "am", "us", "os", "ohs", "i", "a", "u"])
    # add_letters("miņ", "wiņ", vd_s_e_with, ["eem", "ahm", "ahs", "ẜch", "ai", "as", "ah", "am", "us", "os", "ohs", "i", "a", "u"])
    # add_letters("win", "wiņ", vd_s_e_with, ["eem", "ahm", "ahs", "ẜch", "ai", "as", "ah", "am", "us", "os", "ohs", "i", "a", "u"])
    # exceptions(["Marek", "marato", "Marato"], vd_s_e_with, 0)
    # add_letters("nemar", "newar", vd_s_e_with, ["ehẜchu", "ehjahm", "ehjaht", "ehseet", "ehẜeet", "ehsim", "ehẜim", "ehtu", "ehju", "ehji", "ehsi", "ehẜi", "ehja", "eet", "ehs", "eht", "am", "at", "ot", "oht", "u", "i", ""] )
    # add_letters("nemarr", "newarr", vd_s_e_with, ["ehẜchu", "ehjahm", "ehjaht", "ehseet", "ehẜeet", "ehsim", "ehẜim", "ehtu", "ehju", "ehji", "ehsi", "ehẜi", "ehja", "eet", "ehs", "eht", "am", "at", "ot", "oht", "u", "i", ""] )
    # add_letters("mar", "war", vd_s_e_with, ["ehẜchu", "ehjahm", "ehjaht", "ehseet", "ehẜeet", "ehsim", "ehẜim", "ehtu", "ehju", "ehji", "ehsi", "ehẜi", "ehja", "eet", "ehs", "eht", "am", "at", "ot", "oht", "u", "i", "", "as", "a"] )
    # add_letters("marr", "warr", vd_s_e_with, ["ehẜchu", "ehjahm", "ehjaht", "ehseet", "ehẜeet", "ehsim", "ehẜim", "ehtu", "ehju", "ehji", "ehsi", "ehẜi", "ehja", "eet", "ehs", "eht", "am", "at", "ot", "oht", "u", "i", "", "as", "a"] )
    # exceptions(["Marek", "marato", "Marato"], vd_s_e_with, 1)
    add_letters("miss", "wiẜ", vd_s_e_with, flexions_n_f+["am", "iem", "i", "us", "os", "ohs"])
    add_letters("wiss", "wiẜ", vd_s_e_with, flexions_n_f+["am", "iem", "i", "us", "os", "ohs"])
    add_letters("miẜẜ", "wiẜ", vd_s_e_with, flexions_n_f+["am", "iem", "i", "us", "os", "ohs"])
    add_letters("wiẜẜ", "wiẜ", vd_s_e_with, flexions_n_f+["am", "iem", "i", "us", "os", "ohs"])
    add_letters("pus", "puẜ", vd_s_e_with, flection_a_f)
    add_letters("sam", "ẜaw", vd_s_e_with, flexions_n_mf[:-1])
    add_letters("ẜam", "ẜaw", vd_s_e_with, flexions_n_mf[:-1])
    add_letters("samehj", "ẜawehj", vd_s_e_with, flexions_n_mf[:-1])
    add_letters("ẜamehj", "ẜawehj", vd_s_e_with, flexions_n_mf[:-1])
    add_letters("maẜ", "maſ", vd_s_e_with, flexions_a_m[:8]+flexions_n_mf+["ais", "ee"])
    add_letters("mas", "maſ", vd_s_e_with, flexions_a_m[:8]+flexions_n_mf+["ais", "ee"])
    add_letters("maẜahk", "maſahk", vd_s_e_with, flexions_a_m[:8]+flexions_n_mf+["ais", "ee"])
    add_letters("masahk", "maſahk", vd_s_e_with, flexions_a_m[:8]+flexions_n_mf+["ais", "ee"])
    add_letters("maẜak", "maſak", vd_s_e_with, flexions_a_m[:8]+flexions_n_mf+["ais", "ee"])
    add_letters("masak", "maſak", vd_s_e_with, flexions_a_m[:8]+flexions_n_mf+["ais", "ee"])
    add_letters("dim", "diw", vd_s_e_with, ["desmit", "ahm", "ahs", "ohs", "eem", "as", "am", "ah", "us", "os", "u", "a", "i"])
    add_letters("drauds", "draudſ", vd_s_e_with, flection_a_f)
    add_letters("draudẜ", "draudſ", vd_s_e_with, flection_a_f)
    vd_s_e_with.update({
	    "mehds": "mehdſ",
	    "nemehds": "nemehdſ",
        "miss": "wiẜs",
        "miẜẜ": "wiẜs",
        "miẜs": "wiẜs",
        "wiss": "wiẜs",
        "wiẜẜ": "wiẜs",
        "mis": "wis",
        "het": "bet",
        'mairs': 'wairs',
        "maj": "waj",
        'mahs': 'maſ',
        'nemahs': 'nemaſ',
        "moi": "waj",
        "woi": "waj",
        "nam": "naw",  
        "neds": "nedſ",
        "ẜchi": "ẜchih",
        "uu": "un",
        "uņ": "un",
        "ro": "to",
        "ļa": "ka",
        "ue": "ne",
        "ns": "us",
        "uo": "no",
        "jam": "jaw",
        "mai": "wai",
        "uav": "naw",
        "pchc": "pehc",
        'tadehl': 'tahdehļ',
        "ta": "tah",
        'sameem': 'ẜaweem',
        'nav': 'naw',
    	"neka": "nekah",
        'lihds': 'lihdſ',
        "lihhs": "lihdſ",
        "llhds": "lihdſ",
        'gandrihs': 'gandrihſ',
        'gadā': 'gadâ',
        'drihs': 'drihſ',
        'dimi': 'diwi',
        'deeẜgan': 'deeſgan',
        'deesgan': 'deeſgan',
        "pilnigi": "pilnihgi",
        "melti": "welti",
        "temihm": "tewihm",
        "temih": "tewih",
        "tem": "tew",
        "tehmam": "tehwam",
        "tehma": "tehwa",
        "tehmu": "tehwu",
        "tehms": "tehws",
        "tehmi": "tehwi",
        "mehl": "wehl",
        "mehls": "wehls",
        'mehlu': "wehlu",
    })

    vd_s_with = {}
    exceptions(["winnes", "wines", "mission", "miẜẜion", "Marek", "marato", "beeẜchu"], vd_s_with, 0)
    vd_s_with.update({
        "Jnd": "Ind",
        "Iclg": "Jelg",
        'Jelgam': 'Jelgaw',         
        "Jgg": "Ig",            #Igauņi
        "pce": "pee",
        "Ģch": "Ꞩch",

        "minn": "wiņņ",
        "miņņ": "wiņņ",
        "winn": "wiņņ",
        "min": "wiņ",
        "miņ": "wiņ",
        "win": "wiņ",

        "nahm": "nahw",
        "nonahm": "nonahw",
        "saķķ": "ſaķ",
        "ẜaķķ": "ſaķ",
        "seķķ": "ſeķ",
        "ẜeķķ": "ſeķ",

        "ẜẜrihmer": "ẜkrihwer",
        "ssrihmer": "ẜkrihwer",
        "ẜẜrihwer": "ẜkrihwer",
        "ssrihwer": "ẜkrihwer",

        "ẜẜohl": "ẜkohl",
        "maẜẜar": "waẜar",

        "miss": "wiẜẜ",
        "wiss": "wiẜẜ",
        "miẜẜ": "wiẜẜ",
        "pamiss": "pawiẜẜ",
        "pawiss": "pawiẜẜ",
        "pamiẜẜ": "pawiẜẜ",
        "mis": "wiẜ",
        "miẜ": "wiẜ",
        "wis": "wiẜ",
        "pamis": "pawiẜ",
        "pamiẜ": "pawiẜ",
        "pawis": "pawiẜ",

        "mairak": "wairahk",
        "mairahk": "wairahk",
        "mihr": "wihr",
        "mahrd": "wahrd",
        "luhs": "juhs",
        # "meeschņ": "weeẜchņ",
        "meeẜchņ": "weeẜchņ",
        # "meesch": "meeſch",
        "meeẜch": "meeſch",
        # "kroeesch": "kweeẜch",
        "kroeeẜch": "kweeẜch",
        "Oeew": "Deew",
        "deewtalpo": "deewkalpo",
        "deewkaloo": "deewkalpo",
        "lecp": "leep",
        "dahrs": "dahrſ",
        "leelak": "leelahk",
        "leepaj": "leepahj",
        "kuldig": "kuldihg",
        "maldib": "waldib",
        "maldihb": "waldihb",
        "malde": "walde",
        'malo': 'walo',
        'mallo': 'wallo',

        'grahmj': 'grahwj',
        'gluschi': 'gluſchi',
        'gluẜchi': 'gluſchi',

        "kurscm": "kurſem",
        "kurẜcm": "kurſem",

        "kurscb": "kurẜch",
        "kurẜcb": "kurẜch",

        "kursck": "kurẜch",
        "kurẜck": "kurẜch",

        "kurscem": "kurẜeem",
        "kurẜcem": "kurẜeem",

        "smeht": "ẜweht",
        "Dezemben": "Dezember",
        'zilmek': 'zilwek',
        'temi': 'tewi',
        'tama': 'tawa',
        'tadehl': 'tahdehļ',
        'stipr': 'ẜtipr',
        'sirg': 'ſirg',
        'ẜirg': 'ſirg',
        'pulkst': 'pulkẜt',
        'muiẜch': 'muiſch',
        'muhsu': 'muhẜu',
        'mainadſiņ': 'wainadſiņ',
        'latm': 'latw',
        'ihst': 'ihẜt',
        'neihst': 'neihẜt',
        'esso': 'eẜẜo',
        'esot': 'eẜot',
        'neesso': 'neeẜẜo',
        'neeso': 'neeẜo',
        "ds": "dſ",
        'esmu': 'eẜmu',
        'neesmu': 'neeẜmu',
        'dſhim': 'dſihw',
        'nedſhim': 'nedſihw',
            "deemſch": "𓐪",
            "diemſch": "𓐩",
        'deem': 'deew',
        'deem': 'deew',
            "𓐪": "deemſch",
            "𓐩": "deemſch",
        'dauds': 'daudſ',
        'nedauds': 'nedaudſ',
        'baẜni': 'baſni',
        'basni': 'baſni',
        'baſni': 'baſni',
        'awiẜ': 'awihſ',
        'awis': 'awihſ',
        'dmesel': 'dwehsel',
	    'Rig': "Rihg",
        'nemar': 'newar',
        'jahmar': 'jahwar',
        'mar': "war",

        'sin': 'ſin',
        'ẜin': 'ſin',
        'nesin': 'neſin',
        'neẜin': 'neſin',
        'pasin': 'paſin',
        'paẜin': 'paſin',
        
        'sasiņ': 'saſiņ',
        'saẜiņ': 'saſiņ',
        'ẜasiņ': 'ẜaſiņ',
        'ẜaẜiņ': 'ẜaſiņ',
        
        'nepasin': 'nepaſin',
        'nepaẜin': 'nepaſin',
        'jahsin': 'jahſin',
        'jahẜin': 'jahſin',
        'jahpasih': 'jahpaſih',
        'jahpaẜih': 'jahpaſih',

        'siņ': 'ſiņ',
        'ẜiņ': 'ſiņ',
        'nesiņ': 'neſiņ',
        'neẜiņ': 'neſiņ',
        'pasiņ': 'paſiņ',
        'paẜiņ': 'paſiņ',
        'nepasiņ': 'nepaſiņ',
        'nepaẜiņ': 'nepaſiņ',

        'ziņa': 'ſiņa',

        'meet': "weet",
        'nomeet': "noweet",
        'nemeet': "neweet",
        'ismeet': "isweet",
        'iſmeet': "iſweet",
        'sameet': "ẜaweet",
        'ẜameet': "ẜaweet",
        
        'mehla': "wehla",
        'mehleẜch': "wehleẜch",

        'masar': 'waẜar',
        'maẜar': 'waẜar',
        'pamasar': 'pawaẜar',
        'pamaẜar': 'pawaẜar',

        "nemas": "nemaſ",
        "nemaẜ": "nemaſ",
        "pamas": "pamaſ",
        "pamaẜ": "pamaſ",
        "wismaẜ": "wismaſ",
        "wismas": "wismaſ",
        "wiẜmaẜ": "wiẜmaſ",
        "wiẜmas": "wiẜmaſ",

        "beeẜch": "beeſch",
        "wisbeeẜch": "wisbeeſch",
        "wiẜbeeẜch": "wiẜbeeſch",

        "brihẜch": "brihſch",

    })
    exceptions(["winnes", "wines", "mission", "miẜẜion", "Marek", "marato", "beeẜchu"], vd_s_with, 1)
    add_letters("ds", "dſ", vd_s_with, prefixes, True)
    add_letters("mehl", "wehl", vd_s_with, ['jahno', 'jahee', 'jahpahr', 'jahpa', 'jahis', 'jahiſ', 'neno', 'neee', 'nepahr', 'Nepa', 'nepa', 'neis', 'neiſ', 'no', 'ee', 'pahr', 'wis', 'wiẜ', 'pa', 'is', 'iſ'], True)
    #pa taisno mehl-> wehl nevar, jo ir vārds mēle, kas traucē
    vd_e_with = {
        "S": "s",
            "s.": "𓐮",
        "ẜ": "s",
            "𓐮": "s.",
        "lcs": "les",
        "pcs": "pes",
    }

    vd_x_with = {
            "ksembu": "𓐮",  #Luksemburga
            "kẜembu": "𓐭",
            "ksemp": "𓐬",   #eksemplārs
            "kẜemp": "𓐫",
            "semin": "𓐪",   #seminārs
            "ẜemin": "𓐩",
            "Ꞩemin": "𓐨",
            "semio": "𓐧",   #semiotika
            "ẜemio": "𓐦",
            "Ꞩemio": "𓐥",
        "semm": "ſem",
        "ẜemm": "ſem",
        "sem": "ſem",
        "ẜem": "ſem",
            "𓐮": "kẜembu",
            "𓐭": "kẜembu",
            "𓐬": "kẜemp",
            "𓐫": "kẜemp",
            "𓐪": "ẜemin",
            "𓐩": "ẜemin",
            "𓐨": "Ꞩemin",
            "𓐧": "ẜemio",
            "𓐦": "ẜemio",
            "𓐥": "Ꞩemio",

            "ſemeen": "𓐤",
            "Semeen": "𓐣",
            "aņehmeen": "𓐢",
        "meen": "ween",
        "Meen": "Ween",
            "𓐤": "ſemeen",
            "𓐣": "Semeen",
            "𓐢": "aņehmeen",

            "kreeme": "𓐡", #skriemelis
            "ikreem": "𓐠",
            "Ikreem": "𓐐𓐫",
        "kreem": "kreew",
        "Kreem": "Kreew",
            "𓐡": "kreeme",
            "𓐠": "ikreem",
            "𓐐𓐫": "Ikreem",
        "cet": "eet",
        "ssmezz": "ẜẜwezz",   #saulessveces, vissvecākais
        "alstsmezza": "alstswezza",        #valstsvecākais
        "cho gadd": "chogadd",
        "midd": "widd",
        "Midd": "Widd",
        "mid": "wid",
        "Mid": "Wid",
        "tecs": "teeẜ",
        "Tecs": "Teeẜ",
        "preck": "preek",
        "Preck": "Preek",
        "decn": "deen",
        "Decn": "Deen",
        'starp': 'ẜtarp',
        'stahm': 'ẜtahw',
        'ẜtahm': 'ẜtahw',
        'Ꞩtahm': 'Ꞩtahw',
        'skol': 'ẜkol',
        'ļaik': 'laik',
        'Ļaik': 'Laik',
        'teesa': 'teeẜa',
        'Teesa': 'Teeẜa',
        'stipr': 'ẜtipr',    

	"cheijen": "chejeen",
	"chejen": "chejeen",
        'selt': 'ſelt',
        'ẜelt': 'ſelt',
        'Ꞩelt': 'Selt',
        
	    'sird': 'ẜird',
	    'reds': 'redſ',
	    'Reds': 'Redſ',
        'sahl': 'ẜahl',
        'sahk': 'ẜahk',
        'reis': 'reiſ',
        'Reis': 'Reiſ',
        'pilseht': 'pilẜeht',
        'Pilseht': 'Pilẜeht',
        'pagast': 'pagaẜt',
        'Pagast': 'Pagaẜt',
        'makar': 'wakar',
        'Makar': 'Wakar',
        'malẜ': 'walẜ',
        'mals': 'walẜ',
        'Malẜ': 'Walẜ',
        'Mals': 'Walẜ',
        'maigẜn': 'waigſn',
        'maigsn': 'waigſn', #zvaigznes
        'laikā': 'laikâ',
        'Laikā': 'Laikâ',
        'raudẜe': 'raudſe',
        'raudse': 'raudſe', #draudze
        'daẜch': 'daſch',
        'Daẜch': 'Daſch',
        "smezz": "ẜmezz",
        "smez": "ẜmez",
	"maldih": "waldih",
	"Maldih": "Waldih",
	"maldiẜ": "waldihẜ",
	"Maldiẜ": "Waldihẜ",
	"maldihẜ": "waldihẜ",
	"Maldihẜ": "Waldihẜ",
    "dſihm": "dſihw",
    "Dſihm": "Dſihw",
    "maijag": "waijag",
    "Maijag": "Waijag",
    "maijad": "waijad",
    "Maijad": "Waijad",
    "miẜch": "wiſch",
    "miſch": "wiſch",
    "wiẜch": "wiſch",
    "meegl": "weegl",
    "Meegl": "Weegl",
    "maise": "maiſe",
    "Maise": "Maiſe",
    "leſu": "Jeſu",
    "lesu": "Jeſu",
    "leẜu": "Jeſu",
    "Leſu": "Jeſu",
    "Lesu": "Jeſu",
    "Leẜu": "Jeſu",
        "pagalm": "𓐑",
        "Pagalm": "𓐒",
    "galm": "galw",
    "Galm": "Galw",
        "𓐑": "pagalm",
        "𓐒": "Pagalm",
    "allaẜch": "allaſch",
    "Allaẜch": "Allaſch",
    "vck": "vek",
    "kugg": "kuģ",
    "roiņņ": "wiņņ",
    "rviņņ": "wiņņ",
    }
    exc_list = [
        "gods",    #godsirdīgs
        "Gods",    #godsirdīgs
        "sirds",   #sirdsapziņa
        "ẜirds",   #sirdsapziņa
        "Ꞩirds",   #sirdsapziņa
        "andsa",   #Sandsaka, Falklandsallas
        "rundsa",   #Brundsat
        "dsen",    # jo liela daļa ir vācu vai pilsētu vārdi
        "Raudsep",
        "indsel",  #Grindsel, Rindsele,
        "gadsimt",
        "Gadsimt",
        "dson",     #Davidsons
        "ẜmezz",   #Smecīgs
        "ẜmez",
        "Ꞩmezz",
        "Ꞩmez",
        "imitamezz",    # Zimitamezzias
        "imitamez",
        "ntermezzo",    # Intermezzo
        "ntermezo",
        "Mezza",
        "Meza",
        "ezzenah",      # mecanāts
        "ezenah",
        "meẜchan",
    ]

    exceptions(exc_list, vd_x_with, 0)
    add_letters("meẜch", "meſch", vd_x_with)
    add_letters("Meẜch", "Meſch", vd_x_with)
    add_letters("ds", "dſ", vd_x_with, vowels)
    add_letters("mezz", "wezz", vd_x_with)
    add_letters("Mezz", "Wezz", vd_x_with)
    add_letters("mez", "wez", vd_x_with)
    add_letters("Mez", "Wez", vd_x_with)
    exceptions(exc_list, vd_x_with, 1)

    for key, val in vd0.items():
        text = text.replace(key, val)
    for key, val in {"S": "s"}.items():
        text = starts_ends_with(key, val, text, 2)

    for key, val in vd_s_e_with.items():
        text = starts_ends_with(key, val, text, 0)
    for key, val in vd_s_with.items():
        text = starts_ends_with(key, val, text, 1)
    for key, val in {"wiẜẜ": "wiẜs", "wiẜ": "wis"}.items():
        text = starts_ends_with(key, val, text, 0)
    for key, val in vd_e_with.items():
        text = starts_ends_with(key, val, text, 2)
    for key, val in vd_x_with.items():
        text = text.replace(key, val)

    return text