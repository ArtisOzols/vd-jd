import re
from LatvianStemmer import stem
from resources.py.lang_resources.vcc_wordlist import st_vcc
from resources.py.lang_resources.vcc_wordlist import nost_vcc
from resources.py.lang_resources import w_prefixs_endings as w_p_e
from resources.py.lang_resources import fractur_to_latin_dict as dict
from resources.py.lang_resources import verbs
from resources.py import old_script


all_verbs = verbs.i | verbs.ii_iii
consonants = ["b", "c", "č", "d", "f", "g", "ģ", "h", "j", "k", "ķ", "l", "ļ", "m", "n", "ņ", "p", "r", "s", "š", "t", "v", "z", "ž"]
svowels = ["a", "e", "i", "u", "o"]
vowels = ["a", "e", "i", "u", "ā", "ē", "ī", "ū", "o"]
s_to_l_vowels = {"a": "ā", "e": "ē", "i": "ī", "u": "ū"}

change_words = {"ši": "šī", "ta": "tā", "irr": "ir", "ari": "arī", "bij": "bija", "tape": "tapa", "trešu": "trešo", "taī": "tajā", "taīs": "tajās", "tapēc": "tāpēc", "mācit": "mācīt", "voi": "vai", "tadēļ": "tādēļ"}

# Prefixes
# def change_prefix(w):
#     if w[:2] in ["is", "us"] or w[:3] in ["ais", "bes"]:
#         if not w in w_p_e.pref_exc:
#             if w[:4] == "līds":
#                 return "līdz"+w[4:]
#             if w[:3] == "ais":
#                 return "aiz"+w[3:]
#             if w[:3] == "bes":
#                 return "bez"+w[3:]
#             if w[:2] == "is":
#                 return "iz"+w[2:]
#             if w[:2] == "us":
#                 return "uz"+w[2:]
#     return w
def remove_prefix(w):
    for p in w_p_e.pref:
        if w[:len(p)] == p:
            return (w[len(p):], p)
    return (w, "")

def change_vcc(w):
    w, pref = remove_prefix(w)
    if len(w) > 2:
        for v in svowels:
            for c in consonants:
                if v+c+c in w:
                    if not stem(w) in st_vcc and not w in nost_vcc:
                        w = w.replace(v+c+c, v+c)
    return pref + w

# Suffixes
def change_c_v_san(w, st_w):
    if st_w[-3:] == "šan" and st_w[-4] in ["a", "e", "i", "u"]:
        for e in w_p_e.c_v_san:
            if e in st_w:
                return
        if not st_w[-5] in vowels:
            c = st_w[-4]
            return w.replace(c+"šan", s_to_l_vowels[c]+"šan")

def change_v_taj(w, st_w):
    if st_w[-4] in vowels and st_w[-3:] == "taj":
        if not st_w in w_p_e.v_taj:
            c = st_w[-4]
            if c in ["a", "e", "i", "u"]:
                return w.replace(c+"taj", s_to_l_vowels[c]+"tāj")
            else:
                return w.replace(c+"taj", c+"tāj")
    elif st_w[-4] in ["a", "e", "i", "u"] and st_w[-3:] == "tāj":
        if not "jautāj" in st_w and not "maitāj" in st_w:
            if not st_w in w_p_e.sv_taj:
                return w.replace(st_w[-4]+"tāj", s_to_l_vowels[st_w[-4]]+"tāj")

def mod_verb(w, verb_d, end):
    w = w[:-len(end)]
    if len(w) > 1:
        if w[-2] in consonants:
            v = w[-1]
            if v in ["i", "a", "e", "u"]:
                w = w[:-1] + s_to_l_vowels[v]
                nopref_w = remove_prefix(w)[0]

                if nopref_w in verb_d or w in verb_d:
                    return w + end     
def change_verb_tense(w):
# Change short to long vowel in verb suffix and ending
    # Infinitive, Past, future and II conj. present
    for e in ["sieties", "jāmies", "jamies", "jāties", "jaties", "simies", "amies", "aties", "ties", "jies", "siet", "sies", "jām", "jam", "jāt", "jat", "jos", "jās", "jas", "sim", "šos", "am", "at", "ju", "ji", "ja", "šu", "si", "s", "t"]:
        if w[-len(e):] == e:
            # Infinitive form
            if e in ["ties", "t"]:
                return mod_verb(w, all_verbs, e)
            
            # The rest
            else:
                mod_w = mod_verb(w, verbs.ii_iii, e)
                w = mod_w if mod_w else w
                break
    # III conj. 1st group (-īt, -īties, -ināt, -ināties)
    for e in ["jamies", "jaties", "amies", "aties", "jam", "jat", "jas", "am", "at", "as"]:
        el = len(e)
        if w[-el:] == e:
            if e[0] == "j":
                e = w[-el-1:]  # Adding last char befor ending

            mod_w = w[:-el]
            nopref_mod_w = remove_prefix(mod_w)[0]
            if nopref_mod_w in verbs.iii_first_g or mod_w in verbs.iii_first_g:
                e = e.replace("a", "ā")
                return mod_w+e
    return w

def change_c_ib(w, st_w):
    if not w in w_p_e.ib_exc_nost:
        if not st_w in w_p_e.ib_exc_st:
            if len(st_w) > 2:
                if st_w[-3] in consonants and st_w[-2:] == "ib":
                    return w.replace(st_w, st_w[:-2]+"īb")


def is_changed(new_t, w):
    return new_t if new_t else w   
def edit_w(w):
    # w = is_changed(change_prefix(w), w)
    w = is_changed(change_vcc(w), w)
    w = is_changed(change_verb_tense(w), w)

    st_w = stem(w)
    if len(st_w) > 4:
        w = is_changed(change_c_v_san(w, st_w), w)
        w = is_changed(change_v_taj(w, st_w), w)

    w = is_changed(change_c_ib(w, st_w), w)
    
    if w in change_words:
        w = change_words[w]
        
    # Endings
    if w[-3:] == "ges":
        w = w[:-3] + "gas"

    if w[-4:] == "dait":
        w = w[:-4] + "diet"

    if w[-4:] == "dait":
        w = w[:-4] + "diet"

    return w


def split_and_edit_words(text):
    words = re.findall(r"\w+(?:['-]\w+)?|\s+|[^\w\s]", text)  # split the text into words, preserving escape characters
    for w in words:
        # True are only words. Words can contain "'" or numbers (like "arr'", "15ajjā")
        if w.isalnum() or "'" in w or "-" in w:
            if not w.isnumeric():
                if w.islower():
                    new_w = edit_w(w)
                    if new_w != w:
                        words[words.index(w)] = new_w
                else:
                    new_w = edit_w(w.lower())
                    if new_w != w:
                        if w.istitle():
                            words[words.index(w)] = new_w.title()
                        elif w.isupper():
                            words[words.index(w)] = new_w.upper()
                        else:
                            words[words.index(w)] = new_w
    return "".join(words)

def change_key_val(text, d):
    for key, value in d.items():
        text = text.replace(key.upper(), value.upper())
        if len(key) > 1:
            text = text.replace(key.title(), value.title())
        text = text.replace(key, value)
    return text

def change_ee_to_ie(text):
    for key, value in dict.ee_exc_1.items():
        text = text.replace(key.upper(), value+"§")
        text = text.replace(key.title(), value+"╩")
        text = text.replace(key, value+"╔")
    text = change_key_val(text, {"ee": "ie"})
    for key, value in dict.ee_exc_2.items():
        text = text.replace(key+"§", value.upper())
        text = text.replace(key+"╩", value.title())
        text = text.replace(key+"╔", value)
    for key, value in dict.ee_exc_1.items():
        text = text.replace(value+"§", key.upper())
        text = text.replace(value+"╩", key.title())
        text = text.replace(value+"╔", key)
    return text

def fraktur_to_latin(text, x=False, r=True, ch=False, ee_only=False, change_S_to_Z=True):
    text = " " + text + " "
    # \n, \t
    text = text.replace("\n", " 🤯 ")
    text = text.replace("\t", " 📏 ")

    if x:
        text = text.replace("X", "Ks")
        text = text.replace("x", "ks")

    if r:
        text = text.replace("Ŗ", "R")
        text = text.replace("ŗ", "r")

    if ee_only:
        text = change_ee_to_ie(text)
        # \n, \t
        text = text.replace(" 🤯 ", "\n")
        text = text.replace(" 📏 ", "\t")
        return text[1:-1]

    # Ā, Ē, Ī, Ō, Ū, V, C
    text = change_key_val(text, dict.lengthmarks_w_z)

    # Z
    if change_S_to_Z:
        for key, value in dict.z_cap.items():
            text = text.replace(key, value)

    # Z, Ž, Č, ST, SD, SP
    text = text.replace("ſ", "z")

    for key, value in dict.st_tzch_exc.items():
        text = text.replace(key.upper(), value+"▌")
        text = text.replace(key.title(), value+"▐")
        text = text.replace(key, value+"▬")

    text = change_key_val(text, dict.st_tzch_sch_zch)

    for key, value in dict.st_tzch_exc.items():
        text = text.replace(value+"▌", key.upper())
        text = text.replace(value+"▐", key.title())
        text = text.replace(value+"▬", key)

    text = change_key_val(text, dict.tzch)

    # S, Š, Č
    text = text.replace("ẜ", "s")
    text = text.replace("Ꞩ", "S")
    text = change_key_val(text, dict.s_š_č)

    # PREFIXES
    text = change_key_val(text, dict.prefixes)

    # EE
    text = change_ee_to_ie(text)

    if ch:
        dict.lengthmarks_w_z["ch"] = "h"
        dict.lengthmarks_w_z["Ch"] = "H"

    # \n, \t
    text = text.replace(" 🤯 ", "\n")
    text = text.replace(" 📏 ", "\t")
    return text[1:-1]

# patch_dict = {
#     "maldiš": "valdīš",
#     "Maldiš": "Valdīš",
#     "siņ": "ziņ",
#     "Siņ": "Ziņ",
#     "sin": "zin",
#     "Sin": "Zin",
#     "Riga": "Rīga",
#     "ietpilso": "☺𓀠☺",
#     " miet": " viet",
#     "Miet": "Viet",
#     "☺𓀠☺": "ietpilso",
#     "dārs": "dārz",
#     "Dārs": "Dārz",
#     "iepaj": "iepāj",   
#     "uldig": "uldīg",
#     "malde": "valde",
#     "Malde": "Valde",
#     " uo ": " no ",
#     " lūs ": "jūs ",
#     "mien": "vien",
#     "Mien": "Vien",
#     "ilnig": "ilnīg",
#     "ielaka": "ielāka",
#     "šeijen": "šejien",
#     "Šeijen": "Šejien",
#     "melti": "velti",
#     "Melti": "Velti",
#     "vinš": "viņš",
#     "Vinš": "Viņš",
#     "mēds": "mēdz",
#     "Mēds": "Mēdz",
#     " dimas": " divas",
#     "Dimas": "Divas",
#     "dzīm": "dzīv",
#     "Dzīm": "Dzīv",
#     "maijag": "vajag",
#     "Maijag": "Vajag",
    
#     " marrē": " varē",
#     " marra": " vara",
#     " marru": " varu",
#     "Marrē": "Varē",
#     " nemarr": " nevar",
#     "Nemarr": "Nevar",

#     " marē": " varē",
#     " mara": " vara",
#     " maru": " varu",
#     "Marē": "Varē",
#     " nemar": " nevar",
#     "Nemar": "Nevar",



#     "marbūt": "varbūt",
#     "Marbūt": "Varbūt",
#     "marrbūt": "varbūt",
#     "Marrbūt": "Varbūt",
#     " šē ": " še ",
#     "Šē ": "Še ",
#     " ļa": " ka",
#     ",ļa": ",ka",
#     " ue": " ne",
#     " ns": " uz",
#     " uņ": " un",
#     " ro ": " to ",
#     " jam ": " jau ",
#     "Jam": "Jau",
#     " šini ": " šinī ",
#     "Šini ": "Šinī ",
#     "reds": "redz",
#     "Reds": "Redz",
#     " mai ": " vai ",
#     " mai!": " vai!",
#     ",mai": ", vai",
#     "Mai": "Vai",
#     " tē ": " te ",
#     "Tē ": "Te ",
#     " kopa": " kopā",
#     "Kopa": "Kopā",
#     "mieu": "vien",
#     "Mieu": "Vien",
#     "vieu": "vien",
#     "Vieu": "Vien",
#     " tem": " tev",
#     "Tem": "Tev",
#     "tēms": "tēvs",
#     "Tēms": "Tēvs",
#     "istēmu": "☻𓀠☻",
#     "tēmu": "tēvu",
#     "Tēmu": "Tēvu",
#     "tēmi": "tēvi",
#     "Tēmi": "Tēvi",
#     "☻𓀠☻": "istēmu",
#     " mēl": " vēl",
#     "Mēl": "Vēl",
#     " ciņa": " ziņa",
#     "Ciņa": "Ziņa",
#     "emiš": "eviš",
#     "aviš": "avīž",
#     "Aviš": "Avīž",
#     "lielak": "lielāk",
#     "Lielak": "Lielāk",
#     "ķeisar": "ķeizar",
#     "Ķeisar": "Ķeizar",
#     "keisar": "keizar",
#     "Keisar": "Keizar",
#     "miegli": "viegli",
#     "Miegli": "Viegli",
#     "drauds": "draudz",
#     "Drauds": "Draudz",
#     "maise": "maize",
#     "Maise": "Maize",
#     "aznic": "aznīc",
#     "pamisam": "pavisam",
#     "Pamisam": "Pavisam",
#     "pamissam": "pavisam",
#     "Pamissam": "Pavisam",
#     "arvienu vien": "♥𓀠♥",
#     "Arvienu vien": "♥𓀡♥",
#     "arvienu": "arvien",
#     "Arvienu": "Arvien",
#     "♥𓀠♥": "arvienu vien",
#     "♥𓀡♥": "Arvienu vien",
#     "meša": "meža",
#     "Meša": "Meža",
#     " masa ": " maza ",
#     "Masa": "Maza",
#     "nemas": "nemaz",
#     "Nemas": "Nemaz",
#     "masu": "mazu",
#     "Masu": "Mazu",
#     " sa - ": "  sa",
#     "bieši": "bieži",
#     "Bieši": "Bieži",
#     "tadš": "taču",
#     "Tadš": "Taču",
#     "lesus": "Jēzus",
#     "Lesus": "Jēzus",
#     "dzīm": "dzīv",
#     "Dzīm": "Dzīv",
#     "galmas": "galvas",
#     "Galmas": "Galvas",
#     "maijaga": "vaijaga",
#     "Maijaga": "Vaijaga",
#     "zaicinat": "zaicināt",
#     "iztaba": "istaba",
#     "Iztaba": "Istaba",
#     " ša ": " šā ",
#     "Ša": "Šā",
#     "tani": "tanī",
#     "Tani": "Tanī",
#     "pusse": "puse",
#     "Pusse": "Puse",
#     " arr": " ar",
#     "Arr": "Ar",
#     "allaš": "allaž",
#     "Allaš": "Allaž",
#     "zelssceļ": "zelzsceļ",
#     "brīšam": "brīžam",
#     "Brīšam": "Brīžam",
#     " ties ": " tiesa ",
#     "Ties ": "Tiesa ",
#     "pilsat": "pilsēt",
#     "Pilsat": "Pilsēt",
#     "kapēc": "kāpēc",
#     "Kapēc": "Kāpēc",
#     "tadēļ": "tādēļ",
#     "Tadēļ": "Tādēļ",
#     "tapēc": "tāpēc",
#     "Tapēc": "Tāpēc",
#     " ta ": " tā ",
#     ",ta ": ",tā ",
#     "Ta": "Tā ",
#     "citad": "citād",
#     "Citad": "Citād",
    
#     "vienigi": "vienīgi",
#     "Vienigi": "Vienīgi",
#     " jav": " jau",
#     "Jav": "Jau",
#     "tappe": "tapa",
#     "Tappe": "Tapa",
#     "ļaušu": "ļaužu",
#     "Ļaušu": "Ļaužu",
#     " neka ": " nekā ",
#     "Neka ": "Nekā ",
#     "sacci": "sacī",
#     "Sacci": "Sacī",
#     "tiešam": "tiešām",
#     "Tiešam": "Tiešām",
#     " itt ": " it ", 
#     "Itt ": "It ",
#     "tūlit": "tūlīt",
#     "Tūlit": "Tūlīt",
#     "pārradu": "parādu",
#     "Pārradu": "Pārādu",
#     "vēlak": "vēlāk",
#     "Vēlak": "Vēlāk",
#     "pēdej": "pēdēj",
#     "Pēdej": "Pēdēj",
#     "tāļak": "tālāk",
#     "Tāļak": "Tālāk",
#     "tālak": "tālāk",
#     "Tālak": "Tālāk",
#     "cilvek": "cilvēk",
#     "Cilvek": "Cilvēk",
#     "mācitaj": "mācītāj",
#     "Mācitaj": "Mācītāj",
#     "vecak": "vecāk",
#     "Vecak": "Vecāk",
#     "tāļu": "tālu",
#     "Tāļu": "Tālu",
#     "april": "aprīl",
#     "April": "Aprīl",
#     "mierig": "mierīg",
#     "Mierig": "Mierīg",
#     "derr": "der",
# }
def convert(text, x=False, r=True, ch=False, ee_only=False, change_S_to_Z=True):
    # text = old_script.clean_words(text)
    text = fraktur_to_latin(text, x, r, ch, ee_only, change_S_to_Z)
    text = split_and_edit_words(text)
    # for key, val in patch_dict.items():
    #     if key in text:
    #         text = text.replace(key, val)

    return text