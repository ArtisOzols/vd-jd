import re
from LatvianStemmer import stem
from resources.py.lang_resources.vcc_wordlist import st_vcc
from resources.py.lang_resources.vcc_wordlist import nost_vcc
from resources.py.lang_resources import w_prefixs_endings as w_p_e
from resources.py.lang_resources import fractur_to_latin_dict as dict
from resources.py.lang_resources import old_w_dictionary
from resources.py.lang_resources import verbs

all_verbs = verbs.i | verbs.ii_iii
consonants = {"b", "c", "č", "d", "f", "g", "ģ", "h", "j", "k", "ķ", "l", "ļ", "m", "n", "ņ", "p", "r", "s", "š", "t", "v", "z", "ž"}
a_e_i_u = {"a", "e", "i", "u"}
vowels = {"a", "e", "i", "o", "u", "ā", "ē", "ī", "ū"}
s_to_l_vowels = {"a": "ā", "e": "ē", "i": "ī", "u": "ū"}
diacritic_char = {"ā", "č", "ē", "ģ", "ī", "ķ", "ļ", "ņ", "š", "ū", "ž"}

# Changes prefixes – short to long vowel ("lidz" to "līdz"; "pec" to "pēc"; "ja"+vowel (exc. "u") to "jā"+vowel) and "s" to "z" in "is", "us", "ais", "bes"
def change_prefix(w):
    # Counts word characters, then edits those words longer that 4 characters, then those longer than 3
    w_len = len(w)

    # Changes short to long vowel in pefixes  
    if w_len > 3:
        # If first 4 letters in word are "lidz" and this word stemmed is not in exeption list, "lidz" is replaced with "līdz" 
        if w[:4] == "lidz":
            if not stem(w) in w_p_e.lidz_st:
                w = "līdz"+w[4:]
    if w_len > 2:
        # If first 3 letters in word are "pec" and this word neither stemmed nor non stemmed is not present in exeption list, "pec" is replaced with "pēc" 
        if w[:3] == "pec":
            if not w in w_p_e.pec or not stem(w) in w_p_e.pec_st:
                w = "pēc"+w[3:]
        # If first 2 letters in word are "ja" followed by a vowel (except "u" since there are too many words that start with "jau") and this word neither stemmed nor non stemmed is not present in exeption list, "ja" is replaced with "jā" 
        elif w[:3] in {"jaa", "jae", "jai", "jao", "jaā", "jaē", "jaī", "jaū"}:
            if not w in w_p_e.ja_v or not stem(w) in w_p_e.ja_v_st:
                w = "jā"+w[2:]
    
        # Changes "s" to "z" in pefixes
        # If word starts with "is", "us", "ais" or "bes" and word is not in exception list, "s" in prefix is replaced with "z"
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

# Changes "ch" to "h"
def change_ch(w):
    # If "ch" is in the word and word is not in exception list, "ch" is replaced with "h"
    if "ch" in w:
        if not w in w_p_e.ch_exc:
            return w.replace("ch", "h")
    return w

# Removes prefix
def remove_prefix(w, rm_all=True):
    for p in w_p_e.pref:
        # Takes each prefix from "w_p_e.pref" list and checks if word starts with it. Measures prefix length (taken from the list) and checks that many first letters in the word; if they match, prefix is removed
        if w[:len(p)] == p:
            nopref_w = w[len(p):]
            # if property rm_all is set to False, word without a prefix and removed prefix is returned. If not, the rest of the prefixes will be removed from word and returned
            if not rm_all:
                return (nopref_w, p)
            
            # To remove the remaining prefixes, remove_prefix() function is called. Both its values are returned, but before the second value returned prefix is added
            new_w, new_p = remove_prefix(nopref_w)
            return (new_w, p + new_p)
    # If word dont have any prefix, word with nothing is returned
    return (w, "")

# Replaces vowel + doubled consonants with vowel and one consonant (e.g., "patti"->"pati", "sattikt"->"satikt")
def change_vcc(w):
    orig_w, pref = w, ""
    # Checks if word neather stemmed nor non stemmed is in exception lists. If it is, unmodified word is returned, else – one prefix is removed from the word and added to "pref" variable.
    # This process continues until the word has no more prefixes
    while True:
        if stem(w) in st_vcc or w in nost_vcc:
            return orig_w
        w, new_pref = remove_prefix(w, False)
        pref += new_pref
        if not new_pref:
            break
    # Next word without prefix will be processed to avoid vowel + doubled consonants in prefix (e.g. "ieeja")
    # If word still have 3 or more characters, multiple combinations of vowel + doubled consonants are generated and checked if they are present in the word. If they are and if word neather stemmed nor non stemmed are present in exception list, doubled consonant is removed.
    # This process continues either until the word is in exception list or until there are no vowel with doubled consonant in the word. In both cases word is returned with its prefix
    if len(w) > 2:
        for v in a_e_i_u | {"o"}:
            for c in consonants:
                if v+c+c in w:
                    if stem(w) in st_vcc or w in nost_vcc:
                        return pref + w
                    w = w.replace(v+c+c, v+c)
    return pref + w

# Replaces short to long vowel if before vowel is consonant but after – "šan"
def change_c_v_san(w, st_w):
    # Checks if last 3 letters of stemmed word is "šan" and before it – a short vowel
    if st_w[-3:] == "šan" and st_w[-4] in a_e_i_u:
        # If stemmed word is in exception list, non stemmed word is returned
        if st_w in w_p_e.c_v_san_exc:
            return w
        # Checks if the 5th character from the end is consonant. If it is – following vowel in nonstemmed word is changed to long vowel
        if not st_w[-5] in vowels:
            v = st_w[-4]
            return w.replace(v+"šan", s_to_l_vowels[v]+"šan")
    return w

# Replaces short to long vowel if "tāj" or "taj" (which later is replaced with "tāj") follows
def change_v_taj(w, st_w):
    # Checks if stemmed word ends with "taj" and before is a vowel  
    if st_w[-4] in vowels and st_w[-3:] == "taj":
        # Checks if stemmed word is not in exception list. "v_taj_short_a" consists of stemmed words that ends with a vowel + "taj"
        if not st_w in w_p_e.v_taj_short_a:
            v = st_w[-4]
            # Checks if the vowel (4th character from the end) is a short vowel. If it is – non stemmed word is returned with long vowel followed by "tāj" (instead of "taj"); if it is not – only "taj" is replaced with "tāj"
            if v in a_e_i_u:
                return w.replace(v+"taj", s_to_l_vowels[v]+"tāj")
            else:
                return w.replace(v+"taj", v+"tāj")

    # Checks if stemmed word ends with "tāj" and before is a short vowel  
    elif st_w[-4] in a_e_i_u and st_w[-3:] == "tāj":
        if not "jautāj" in st_w and not "maitāj" in st_w:
            # Checks if stemmed word is not in exception list. "sv_taj_long_a" consists of stemmed words that ends with short vowel + "tāj"
            if not st_w in w_p_e.sv_taj_long_a:
                # Returns non stemmed word with long vowel before "tāj"
                return w.replace(st_w[-4]+"tāj", s_to_l_vowels[st_w[-4]]+"tāj")
    return w

# Function for change_verb_ending(). Changes short to long vowel before ending
# input: w - verb to modify; verb_d - list of verbs in Latvian; end - w (verb) ending
def mod_verb(w, verb_list, end):
    # Removes w ending
    w = w[:-len(end)]
    if len(w) > 1:
        # To words with more than 2 characters, checks if 2nd to last character is consonant; and last – short vowel
        if w[-2] in consonants:
            v = w[-1]
            if v in a_e_i_u:
                # Changes last character from short to long vowel;
                w = w[:-1] + s_to_l_vowels[v]

                # Checks if w (without end and long vowel as last character) with and without prefix can be found in verb_list
                nopref_w = remove_prefix(w)[0]
                if nopref_w in verb_list or w in verb_list:
                    # If verb exists, it is returned modified with end
                    return w + end

# Change short to long vowel in verb suffix and ending
def change_verb_ending(w):
    # Infinitive, past, future and II conj. present. This will not work for I conj. verbs, except for some words in infinitive form
    # Checks if word is in one of these categories. If it is, word is modified, else – passed unmodified to the next for loop to check if it is a verb of III conj. 1st group 
    for end in ["sieties", "jāmies", "jamies", "jāties", "jaties", "simies", "amies", "aties", "ties", "jies", "siet", "sies", "jām", "jam", "jāt", "jat", "jos", "jās", "jas", "sim", "šos", "am", "ju", "ji", "ja", "šu", "si", "s", "t"]:
        if w[-len(end):] == end:
            # Infinitive form
            # Change short to long vowel in verb suffix and ending if verb is in all_verbs – list of all verbs without endings "ties"and "t"
            if end in ["ties", "t"]:
                mod_w = mod_verb(w, all_verbs, end)
                if mod_w:
                    return mod_w
            # Past, future and II conj. present
            # Change short to long vowel in verb suffix and ending if verb is in verbs.ii_iii – list of II and III conj. verbs without endings "ties"and "t"
            else:
                mod_w = mod_verb(w, verbs.ii_iii, end)
                w = mod_w if mod_w else w
                break
    # III conj. 1st group (-īt, -īties, -ināt, -ināties)
    # Checks if word is in this category. If it is, word is modified, else returned unmodified
    for end in ["jamies", "jaties", "amies", "aties", "jam", "jat", "jas", "am", "at", "as"]:
        end_l = len(end)
        # Checks if any of these endings are at the end of the word 
        if w[-end_l:] == end:
            # For those words with endings that contains "j", aditional letter from word is added to ending
            if end[0] == "j":
                end = w[-end_l-1:]  # Adding last char befor ending

            # Ending is removed; and then – prefix
            mod_w = w[:-end_l]
            nopref_mod_w = remove_prefix(mod_w)[0]
            # Checks if any – with and without prefix word can be found in iii_first_g list – list of stemmed III conj. 1st group verbs
            if nopref_mod_w in verbs.iii_first_g or mod_w in verbs.iii_first_g:
                end = end.replace("a", "ā")
                return mod_w+end
    return w

def change_c_ib(w, st_w):
    if not w in w_p_e.ib_exc_nost:
        if not st_w in w_p_e.ib_exc_st:
            if len(st_w) > 2:
                if st_w[-3] in consonants and st_w[-2:] == "ib":
                    return w.replace(st_w, st_w[:-2]+"īb")
    return w

def edit_w(w):
    w = change_prefix(w)

    w = change_ch(w)
    w = change_vcc(w)
    w = change_verb_ending(w)

    st_w = stem(w)
    if len(st_w) > 4:
        w = change_c_v_san(w, st_w)
        w = change_v_taj(w, st_w)
    w = change_c_ib(w, st_w)

    if w in old_w_dictionary.o_w_dict:
        w = old_w_dictionary.o_w_dict[w]
        
    # Endings
    if w[-3:] == "ak":
        if not w in w_p_e.ak_exc:
            w = w[:-3] + "ak"
    # if w[-3:] == "ges":
    #     w = w[:-3] + "gas"

    # if w[-4:] == "dait":
    #     w = w[:-4] + "diet"

    return w


def split_and_edit_words(text, r=False):
    # Converts "ŗ", "Ŗ" to "r", "R"
    if r:
        text = text.replace("Ŗ", "R")
        text = text.replace("ŗ", "r")

    # Split text into words (Words can contain "'" and numbers, like "arr'", "15ajjā"), escape characters, punctuations, numbers, spaces, symbols
    words = re.findall(r"\w+(?:['-]\w+)?|\s+|[^\w\s]", text)
    for w in words:
        # True for numbers and words (they can contain "'" and numbers (like "arr'", "15ajjā")
        if w.isalnum() or "'" in w or "-" in w:
            # True if is not number
            if not w.isnumeric():
                # Edits word; if word differs from original, it is replaced in the "words" list retaining original case.
                # Lowcases and edits word; Returns the word in original case
                mod_w = edit_w(w.lower())
                # True if word has changed
                if mod_w != w.lower():
                    if w.istitle():
                        # Replaces word with modified word in "words" list. Word is returned in original title case
                        words[words.index(w)] = mod_w.title()
                    elif w.isupper():
                        # Replaces word with modified word in "words" list. Word is returned in original ipper case
                        words[words.index(w)] = mod_w.upper()
                    else:
                        # Replaces word with modified word in "words" list. Word is returned in lowcase. This may not be original case
                        words[words.index(w)] = mod_w
    # Concatinates split text
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

def fraktur_to_latin(text, x=False, r=True, ee_only=False, change_S_to_Z=True):
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

    # \n, \t
    text = text.replace(" 🤯 ", "\n")
    text = text.replace(" 📏 ", "\t")
    return text[1:-1]

# Converts old fraktur latvian text to modern latvian text
# Input: text - text to convert; x -  
def convert(text, x=False, r=True, ee_only=False, change_S_to_Z=True):
    # Transliteration – converts Fraktur to Latin letters
    text = fraktur_to_latin(text, x, r, ee_only, change_S_to_Z)
    # Text modernization – splits text into words, converts them and returns modernized text 
    text = split_and_edit_words(text, r=False)
    return text