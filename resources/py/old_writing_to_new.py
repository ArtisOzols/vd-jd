import re
from LatvianStemmer import stem
from resources.py.lang_resources.vcc_wordlist import st_vcc
from resources.py.lang_resources.vcc_wordlist import nost_vcc
from resources.py.lang_resources.vcc_wordlist import st_adj_adv_with_s
from resources.py.lang_resources import w_prefixs_endings as w_p_e
from resources.py.lang_resources import letter_conversion_dict as dict
from resources.py.lang_resources import old_w_dictionary
from resources.py.lang_resources import verbs

all_verbs = verbs.i | verbs.ii_iii
consonants = {"b", "c", "č", "d", "f", "g", "ģ", "h", "j", "k", "ķ", "l", "ļ", "m", "n", "ņ", "p", "r", "s", "š", "t", "v", "z", "ž"}
a_e_i_u = {"a", "e", "i", "u"}
vowels = {"a", "e", "i", "o", "u", "ā", "ē", "ī", "ū"}
s_to_l_vowels = {"a": "ā", "e": "ē", "i": "ī", "u": "ū"}
diacritic_char = {"ā", "č", "ē", "ģ", "ī", "ķ", "ļ", "ņ", "š", "ū", "ž"}    

# Changes prefixes – "s" to "z" in "is", "us", "ais", "bes", "līds", "lids"; "z" to "s" in prefixes that ends with "s" followed by "t", "d" or "p"; short to long vowel ("lidz" to "līdz"; "pec" to "pēc"; "ja"+vowel (exc. "u") to "jā"+vowel)
def change_prefix(w):
    # Converting prefixes that ends with "s" (but should end with 'z')

    # Changes short to long vowel in pefixes  
    # If first 4 letters in word are "lidz" and this word stemmed is not in exeption list, "lidz" is replaced with "līdz" 
    if w[:4] == "lidz":
        if not w in w_p_e.lidz and not stem(w) in w_p_e.lidz_st:
            w = "līdz"+w[4:]
    if w[:4] == "lids":
        if not w in w_p_e.lids and not stem(w) in w_p_e.lids_st:
            w = "līdz"+w[4:]

    # If word starts with "is", "us", "ais" or "bes" and word is not in exception list, "s" in prefix is replaced with "z"
    if w[:2] == "is":
        if not w in w_p_e.iz and not stem(w) in w_p_e.iz_st:
            w = "iz"+w[2:]
    if w[:2] == "us":
        if not w in w_p_e.uz and not stem(w) in w_p_e.uz_st:
            w = "uz"+w[2:]
    if w[:3] == "ais":
        if not w in w_p_e.aiz and not stem(w) in w_p_e.aiz_st:
            w = "aiz"+w[3:]
    if w[:3] == "bes":
        if not w in w_p_e.bez and not stem(w) in w_p_e.bez_st:
            w = "bez"+w[3:]

    # converting prefixes that ends with "z" (but should end with "s") with following letter  "t", "d" or "p"
    for p in w_p_e.pref_with_st_sd_sp:
        if w[:len(p)] == p:
            w = w.replace(p, p[:-2]+"s"+p[-1])

    # Converting prefixes "ja"+vowel (but should contain long vowel)
    if len(w) > 2:
        # If first 3 letters in word are "pec" and this word non-stemmed is not present in exeption list, "pec" is replaced with "pēc". There is no stemed exception list, because it consists of only 1 word – "pec" 
        # if w[:3] == "pec":
        #     if not w in w_p_e.pec:
        #         w = "pēc"+w[3:]

        # If first 2 letters in word are "ja" followed by a vowel (except "u" since there are too many words that start with "jau") and this word neither stemmed nor non-stemmed is not present in exeption list, "ja" is replaced with "jā" 
        if w[:3] in {"jaa", "jae", "jai", "jao", "jaā", "jaē", "jaī", "jaū"}:
            if not w in w_p_e.ja_v or not stem(w) in w_p_e.ja_v_st:
                w = "jā"+w[2:]                    
    return w

# Removes prefix
def remove_prefix(w, rm_all=True):
    for p in w_p_e.pref:
        # Takes each prefix from "w_p_e.pref" list and checks if word starts with it. Measures prefix length (taken from the list) and checks that many first letters in the word; if they match, prefix is removed
        if w[:len(p)] == p:
            nopref_w = w[len(p):]

            # the minimal length of word without prefix is 2, because the input words can be stemmed. e.g., "neas" from word "neass"
            if len(nopref_w)<=1:
                return (w, "")

            #  if property rm_all is set to False, word without a prefix and removed prefix is returned. If not, the rest of the prefixes will be removed from word and returned
            if not rm_all:
                return (nopref_w, p)
            
            # To remove the remaining prefixes, remove_prefix() function is called. Both its values are returned, but before the second value returned prefix is added
            new_w, new_p = remove_prefix(nopref_w)
            return (new_w, p + new_p)
    # If word dont have any prefix, word with nothing is returned
    return (w, "")

def change_ee(w):
    pref = ""
    if w[:3] == "nee":
        if not stem(w) in dict.nie_st and not w in dict.nie_nost:
            if not stem(w) in dict.nee_st and not w in dict.nee_nost:
                w, pref = w[2:], "ne"
        if not pref:    
            return w
    return pref + w.replace("ee", "ie")

# TZCH→Č, TSCH→Č
def change_tzch_tsch(w):
    w, pref = remove_prefix(w, rm_all=True)
    zs_ch_frakt = {"ž": "zch","š": "sch"}
    for zs_ch in ["ž", "š"]:
        # For cases when last letter of prefix is "t" and first letter of word (without prefix) is "ž" or "š"
        if pref[-1:] == "t" and w[0] == zs_ch:
            # These lists contains words after prefix removal whose prefix's last letter is t and word 1st letter is "ž" or "š" (e.g., "tšūt" from word "atšūt") 
            if not stem("t"+w) in dict.tzch_tsch_ext[f"t{zs_ch_frakt[zs_ch]}_st_pref"] and not "t"+w in dict.tzch_tsch_ext[f"t{zs_ch_frakt[zs_ch]}_nost_pref"]:
                w = pref[:-1] + "č" + w[1:]
                w, pref = remove_prefix(w, rm_all=True)
        # For cases when "tž" or "tš" is in the middle or end of the word
        if "t"+zs_ch in w:
            if not stem(w) in dict.tzch_tsch_ext[f"t{zs_ch_frakt[zs_ch]}_st"] and not w in dict.tzch_tsch_ext[f"t{zs_ch_frakt[zs_ch]}_nost"]:
                w = w.replace("t"+zs_ch, "č")
    return pref + w

# ZT→ST, ZD→SD, ZP→SP
def change_st_zt_sp(w):
    nopref_w, pref = remove_prefix(w, rm_all=True)
    mod_nopref_w = nopref_w
    for z_tdp in ["zt", "zd", "zp"]:
        if z_tdp in mod_nopref_w:
            if not stem(mod_nopref_w) in dict.z_tdp_exc[z_tdp+"_st"] and not mod_nopref_w in dict.z_tdp_exc[z_tdp+"_nost"]:
                mod_nopref_w = mod_nopref_w.replace(z_tdp, "s"+z_tdp[-1])

    if nopref_w != mod_nopref_w:
        return w.replace(nopref_w, mod_nopref_w)
    return w

# CH→H
def change_ch(w):
    # If "ch" is in the word and word is not in exception list, "ch" is replaced with "h"
    if "ch" in w:
        if not w in w_p_e.ch and stem(w) not in w_p_e.ch_st:
            return w.replace("ch", "h")
    return w

# Checks word for vowel followed by 2 consonants
def check_vcc(w):
    nnext_ch, next_ch = None, "" # None, because during 1st iteration they both must not be the same
    for ch in w[::-1]: # This is done backwards to avoid finding vcc in prefixes
        if ch in ["a", "e", "i", "o", "u"] and nnext_ch == next_ch and not nnext_ch in vowels:
            return ch + next_ch + nnext_ch
        nnext_ch = next_ch
        next_ch = ch
def check_vcc_exc(w):
    # Checks if word neather stemmed nor non-stemmed is in exception lists. If it is, unmodified word is returned, else – one prefix is removed from the word and added to "pref" variable.
    # This process continues until the word has no more prefixes
    while True:
        st_w = stem(w)
        if st_w[-4:] == "ošāk":
            st_w = st_w[:-4]
        elif st_w[-2:] in ["āk", "oš"]:
            st_w = st_w[:-2]

        if st_w in st_vcc or w in nost_vcc:
            return True

        w, pref = remove_prefix(w, False)
        if not pref:
            return False

# Replaces vowel + doubled consonants (hereinafter VCC) with vowel and one consonant (e.g., "patti"->"pati", "sattikt"->"satikt", "attiekksme"->"attieksme")
def change_vcc(w):
    ## MUST REWRITE COMMENTS
    # Next word without prefix will be processed to avoid vowel + doubled consonants in prefix (e.g. "ieeja")
    # If word still have 3 or more characters, multiple combinations of vowel + doubled consonants are generated and checked if they are present in the word. If they are and if word neather stemmed nor non-stemmed are present in exception list, doubled consonant is removed.
    # This process continues either until the word is in exception list or until there are no vowel with doubled consonant in the word. In both cases word is returned with its prefix

    # Words with 3 or more letters are verified
    if len(w) > 2:
        pref = ""
        while True:
            vcc = check_vcc(w)
            if not vcc or check_vcc_exc(w):
                return pref + w
            
            # Checking if w is not in superlative degree.
            # If it is, 1st 4 letters should be "viss", then we check if stemmed word without "vis" and "āk" is not in adjectiveor adverb words that start with "s"
            if "vissas" == w[:6] and stem(w)[5:-2] in st_adj_adv_with_s:
                pref, w = "vissa", w[5:]
                continue
            if "viss" == w[:4] and stem(w)[3:-2] in st_adj_adv_with_s:
                pref, w = "vis", w[3:]
                continue
            w = vcc[:2].join(w.rsplit(vcc,1)) # Replaces 1 occurrence starting from the end 
    else:
        return w

# Replaces short to long vowel if before vowel is consonant but after – "šan"
def change_c_v_san(w, st_w):
    # Checks if last 3 letters of stemmed word is "šan" and before it – a short vowel
    if st_w[-3:] == "šan" and st_w[-4] in a_e_i_u:
        # If stemmed word is in exception list, non-stemmed word is returned
        # Checks if the 5th character from the end is consonant. If it is – following vowel in nonstemmed word is changed to long vowel
        if not st_w in w_p_e.c_v_san and not st_w[-5] in vowels:
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
            # Checks if the vowel (4th character from the end) is a short vowel. If it is – non-stemmed word is returned with long vowel followed by "tāj" (instead of "taj"); if it is not – only "taj" is replaced with "tāj"
            if v in a_e_i_u:
                return w.replace(v+"taj", s_to_l_vowels[v]+"tāj")
            else:
                return w.replace(v+"taj", v+"tāj")

    # Checks if stemmed word ends with "tāj" and before is a short vowel  
    elif st_w[-4] in a_e_i_u and st_w[-3:] == "tāj":
        if not "jautāj" in st_w and not "maitāj" in st_w:
            # Checks if stemmed word is not in exception list. "sv_taj_long_a" consists of stemmed words that ends with short vowel + "tāj"
            if not st_w in w_p_e.sv_taj_long_a:
                # Returns non-stemmed word with long vowel before "tāj"
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
                original_mod_w = w
                while True:
                    if w in verb_list:
                        # If verb exists, it is returned modified with end
                        return original_mod_w + end
                    w, pref = remove_prefix(w, rm_all=False)
                    if not pref:
                        break

# Change short to long vowel in verb suffix and ending
def change_verb_ending(w):
    # Infinitive, past, future and II conj. present. This will not work for I conj. verbs, except for some words in infinitive form
    # Checks if word is in one of these categories. If it is, word is modified, else – passed unmodified to the next for loop to check if it is a verb of III conj. 1st group
    # 3rd pers. future (-s) is excluded, because this would change nouns in plural (e.g., "būves" should not be converted to verb "būvēs" since "būves" is also noun in plural)
    for end in ["sieties", "jāmies", "jamies", "jāties", "jaties", "simies", "amies", "aties", "ties", "jies", "siet", "sies", "jām", "jam", "jāt", "jat", "jos", "jās", "jas", "sim", "šos", "am", "ju", "ji", "ja", "šu", "si", "t"]:
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

            # Checks if any – with and without prefix word can be found in iii_first_g list – list of stemmed III conj. 1st group verbs
            original_mod_w = mod_w
            while True:
                if mod_w in verbs.iii_first_g:
                    end = end.replace("a", "ā")
                    return original_mod_w+end
                mod_w, pref = remove_prefix(mod_w, rm_all=False)
                if not pref:
                    break
    return w

def change_c_ib(w, st_w):
    if not w in w_p_e.ib_nost:
        if not st_w in w_p_e.ib_st:
            if len(st_w) > 2:
                if st_w[-3] in consonants and st_w[-2:] == "ib":
                    return w.replace(st_w, st_w[:-2]+"īb")
    return w

def edit_w(w):
    # Endings
    if w[-2:] == "ak":
        if not w in w_p_e.ak:
            w = w[:-2] + "āk"
    # if w[-3:] == "ges":
    #     w = w[:-3] + "gas"
    # if w[-4:] == "dait":
    #     w = w[:-4] + "diet"

    w = change_prefix(w)
    w = change_ee(w)
    w = change_tzch_tsch(w)
    w = change_st_zt_sp(w)
    w = change_ch(w)
    w = change_vcc(w)
    w = change_verb_ending(w)
    
    st_w = stem(w)
    w = change_c_ib(w, st_w)
    if len(st_w) > 4:
        w = change_c_v_san(w, st_w)
        w = change_v_taj(w, st_w)

    if w in old_w_dictionary.o_w_dict:
        w = old_w_dictionary.o_w_dict[w]

    return w

def split_and_edit_words(text):
    """Splits text into words (Words can contain "'" and can be number word ending, like "arr'", "15ajjā")"""
    words = re.findall(r"\w+(?:['-]\w+)?", text)
    for w in set(words):
        w = w.replace("S", "Z")
        mod_w = edit_w(w.lower())
        if w.lower():
            text = text.replace(w, mod_w)
        elif w.istitle():
            text = text.replace(w, mod_w.title())
        elif w.isupper():
            text = text.replace(w, mod_w.upper())
        else:
            # Replaces word with modified in text. Word is returned in lowcase. This may not be original case
            text = text.replace(w, mod_w)
    return text


def change_key_val(text, d):
    for key, value in d.items():
        text = text.replace(key.upper(), value.upper())
        if len(key) > 1:
            text = text.replace(key.title(), value.title())
        text = text.replace(key, value)
    return text

def change_long_vowels_v_c_z_s_sch_zch(text, change_S_to_Z=True):
    text = " " + text + " "
    # \n, \t
    text = text.replace("\n", " 🤯 ")
    text = text.replace("\t", " 📏 ")

    # Ā, Ē, Ī, Ō, Ū, V, C
    text = change_key_val(text, dict.lengthmarks_w_z)

    # Z, Ž, S, Š
    text = text.replace("S", "Z")
    text = text.replace("ſ", "z")
    text = text.replace("Ꞩ", "S")
    text = text.replace("ẜ", "s")
    text = change_key_val(text, dict.s_ž_š)

    # \n, \t
    text = text.replace(" 🤯 ", "\n")
    text = text.replace(" 📏 ", "\t")
    return text[1:-1]

def change_ee_only(text):
    ee_words = set(re.findall(r"\b\w*ee\w*\b", text, flags=re.IGNORECASE))
    for w in ee_words:
        mod_ee_w = change_prefix(w.lower())
        mod_ee_w = change_ee(mod_ee_w)
        if w.islower():
            text = text.replace(w, mod_ee_w)
        if w.istitle():
            text = text.replace(w, mod_ee_w.title())
        if w.isupper():
            text = text.replace(w, mod_ee_w.upper())
        else:
            text = text.replace(w, mod_ee_w)
    return text

def convert(text, r=True, ee_only=False, change_S_to_Z=True):
    """ Converts old fraktur latvian text to modern latvian text
        Inpustring: text - text to convert;
        Boolean: x - if True converts "x" to "ks"; r - if True converts "ŗ" to "r"; ee_only - if True converts only "ee" to "ie" in text; change_S_to_Z - if True converts "S" to "Z"
    """
    if r:
        text = text.replace("Ŗ", "R").replace("ŗ", "r")
    if ee_only:
        return change_ee_only(text)
        
    # Converts old letters and prefixes in text to those used in modern Latvian
    text = change_long_vowels_v_c_z_s_sch_zch(text, change_S_to_Z)
    # Text modernization – splits text into words, converts them and returns modernized text 
    text = split_and_edit_words(text)
    return text