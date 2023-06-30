import re
from LatvianStemmer import stem
from resources.py.lang_resources.vcc_wordlist import st_vcc
from resources.py.lang_resources.vcc_wordlist import nost_vcc
from resources.py.lang_resources import w_prefixs_endings as w_p_e
from resources.py.lang_resources import fractur_to_latin_dict as dict
from resources.py.lang_resources import verbs


all_verbs = verbs.i | verbs.ii_iii
consonants = ["b", "c", "č", "d", "f", "g", "ģ", "h", "j", "k", "ķ", "l", "ļ", "m", "n", "ņ", "p", "r", "s", "š", "t", "v", "z", "ž"]
svowels = ["a", "e", "i", "u", "o"]
vowels = ["a", "e", "i", "u", "ā", "ē", "ī", "ū", "o"]
s_to_l_vowels = {"a": "ā", "e": "ē", "i": "ī", "u": "ū"}

change_words = {"ši": "šī", "ta": "tā", "irr": "ir", "ari": "arī", "bij": "bija", "tape": "tapa", "trešu": "trešo", "taī": "tajā", "taīs": "tajās", "tapēc": "tāpēc", "mācit": "mācīt", "voi": "vai", "tadēļ": "tādēļ"}

# Prefixes
def change_prefix(w):
    if w[:2] in ["is", "us"] or w[:3] in ["ais", "bes"]:
        if not w in w_p_e.pref_exc:
            if w[:3] == "ais":
                return "aiz"+w[3:]
            if w[:3] == "bes":
                return "bez"+w[3:]
            if w[:2] == "is":
                return "iz"+w[2:]
            if w[:2] == "us":
                return "uz"+w[2:]
    return w
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
        if w[-len(e):] == e:
            if e[0] == "j":
                e = w[-len(e)-1] + e  # Adding last char befor ending

            mod_w = w[:-len(e)]
            nopref_mod_w = remove_prefix(mod_w)[0]
            if nopref_mod_w in verbs.iii_first_g or mod_w in verbs.iii_first_g:
                e = e.replace("a", "ā")
                return mod_w+e
    return w

def change_c_ib(w, st_w):
    if not w in w_p_e.ib_exc_nost:
        if not st_w in w_p_e.ib_exc_st:
            if len(st_w) > 2:
                if st_w[-3] in consonants and st_w[-1] == "b":
                    return w.replace(st_w, st_w[:-2]+"īb")


def is_changed(new_t, w):
    return new_t if new_t else w   
def edit_w(w):
    w = is_changed(change_prefix(w), w)
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

    return "".join(words)

def change_key_val(w, d):
    for key, value in d.items():
        w = w.replace(key.upper(), value.upper())
        if len(key) > 1:
            w = w.replace(key.title(), value.title())
        w = w.replace(key, value)
    return w
def fraktur_to_latin(text, r=True, ch=True):
    text = " " + text + " "
    # \n, \t
    text = text.replace("\n", " 🤯 ")
    text = text.replace("\t", " 📏 ")

    # if r:
    #     text = text.replace("Ŗ", "R")
    #     text = text.replace("ŗ", "r")

    if ch:
        dict.lengthmarks_w_z["ch"] = "h"

    # Ā, Ē, Ī, Ō, Ū, H, KS, V, C
    text = change_key_val(text, dict.lengthmarks_w_z)

    # Z, Ž, ST
    for key, value in dict.z_ž_st.items():
        text = text.replace(key, value)

    # S, Š, Č
    text = text.replace("ẜ", "s")
    text = change_key_val(text, dict.s_š_č)

    # PREFIXES
    for key, value in dict.prefixes.items():
        text = text.replace(key.upper(), value.upper())
        text = text.replace(key.title(), value.title())
        text = text.replace(key, value)

    # EE
    for key, value in dict.ee.items():
        text = text.replace(key.upper(), value.upper())
    for key, value in dict.ee.items():
        text = text.replace(key.title(), value.title())
    for key, value in dict.ee.items():
        text = text.replace(key, value)

    # \n, \t
    text = text.replace(" 🤯 ", "\n")
    text = text.replace(" 📏 ", "\t")
    return text[1:-1]

def convert(text, r=True, ch=True):
    text = fraktur_to_latin(text, r, ch)
    text = split_and_edit_words(text)
    return text