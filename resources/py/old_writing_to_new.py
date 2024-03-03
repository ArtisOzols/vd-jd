import string
import re
from LatvianStemmer import stem
from resources.py.lang_resources.vcc_wordlist import st_vcc, nost_vcc, st_adj_adv_with_s, vcc_in_pref, vcc_in_pref_w_st, vcc_in_pref_w_nost
from resources.py.lang_resources import w_prefixs_endings as w_p_e
from resources.py.lang_resources import letter_conversion as lc
from resources.py.lang_resources import old_w_dictionary
from resources.py.lang_resources import verbs

all_verbs = verbs.i | verbs.ii_iii_verbs
consonants = {"b", "c", "č", "d", "f", "g", "ģ", "h", "j", "k", "ķ", "l", "ļ", "m", "n", "ņ", "p", "r", "s", "š", "t", "v", "z", "ž"}
a_e_i_u = {"a", "e", "i", "u"}
vowels = {"a", "e", "i", "o", "u", "ā", "ē", "ī", "ū"}
s_to_l_vowels = {"a": "ā", "e": "ē", "i": "ī", "u": "ū"}
diacritic_char = {"ā", "č", "ē", "ģ", "ī", "ķ", "ļ", "ņ", "š", "ū", "ž"}    

pref_s_to_z = {
    "is": [w_p_e.is_nost, w_p_e.is_st, w_p_e.pref_is_nost, w_p_e.pref_is_st, "iz"],
    "us": [w_p_e.us_nost, w_p_e.us_st, w_p_e.pref_us_nost, w_p_e.pref_us_st, "uz"],
    "ais": [w_p_e.ais_nost, w_p_e.ais_st, w_p_e.pref_ais_nost, [], "aiz"],
    "bes": [w_p_e.bes_nost, w_p_e.bes_st, w_p_e.pref_bes_nost, [], "bez"],
    "lidz": [w_p_e.lidz_nost, w_p_e.lidz_st, [], [], "līdz"],
    "lids": [w_p_e.lids_nost, w_p_e.lids_st, [], [], "līdz"]
    }
# Changes prefixes – "s" to "z" in "is", "us", "ais", "bes", "līds", "lids"; "z" to "s" in prefixes that ends with "s" followed by "t", "d" or "p"; short to long vowel ("lidz" to "līdz"; "pec" to "pēc"; "ja"+vowel (exc. "u") to "jā"+vowel)
def change_prefix(w):
    # converting prefixes that ends with "z" (but should end with "s") with following letter  "t", "d" or "p" (e.g., "puztumšs"→"pustumšs")
    if len(w) > 3:
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
            if not w in w_p_e.ja_v_nost or not stem(w) in w_p_e.ja_v_st:
                w = "jā"+w[2:] 

    # Converts prefixes "pee" to "pie" and "ee" to "ie"
    w, pref = remove_prefix(w)
    if w[:3] == "pee":
        w = "pie" + w[3:]
    elif w[:2] == "ee":
        w = "ie" + w[2:]
    w = pref + w
    
    # Converting prefixes that ends with "s" (but should end with 'z')
    # If word starts with "is", "us", "ais" or "bes" and word is not in exception list, "s" in prefix is replaced with "z"
    for old_pref in ["is", "us", "ais", "bes", "lidz", "lids"]:
        w, pref = remove_prefix(w)
        if w[:len(old_pref)] == old_pref:
            d = pref_s_to_z[old_pref]
            if w in d[0] or stem(w) in d[1] or pref+w in d[2] or stem(pref+w) in d[3]:
                w = pref + w
                continue
            w = d[-1] + w[len(old_pref):]
        w = pref + w
    
    # if w[:2] == "is":
    #     if not w in w_p_e.iz_nost and not stem(w) in w_p_e.iz_st:
    #         w = "iz"+w[2:]
    # if w[:2] == "us":
    #     if not w in w_p_e.uz_nost and not stem(w) in w_p_e.uz_st:
    #         w = "uz"+w[2:]
    # if w[:3] == "ais":
    #     if not w in w_p_e.aiz_nost and not stem(w) in w_p_e.aiz_st:
    #         w = "aiz"+w[3:]
    # if w[:3] == "bes":
    #     if not w in w_p_e.bez_nost and not stem(w) in w_p_e.bez_st:
    #         w = "bez"+w[3:]

    # # If first 4 letters in word are "lidz" and this word stemmed is not in exeption list, "lidz" is replaced with "līdz" 
    # if w[:4] == "lidz":
    #     if not w in w_p_e.lidz_nost and not stem(w) in w_p_e.lidz_st:
    #         w = "līdz"+w[4:]
    # if w[:4] == "lids":
    #     if not w in w_p_e.lids_nost and not stem(w) in w_p_e.lids_st:
    #         w = "līdz"+w[4:]                  
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

# TŽ→Č, TŠ→Č
def change_tš_tž(w):
    w, pref = remove_prefix(w)
    for š_ž in ["š", "ž"]:
        # For cases when last letter of prefix is "t" and first letter of word (without prefix) is "ž" or "š"
        if pref[-1:] == "t" and w[0] == š_ž:
            # These lists contains words after prefix removal whose prefix's last letter is t and word 1st letter is "ž" or "š" (e.g., "tšūt" from word "atšūt") 
            if not "t"+w in lc.tzch_tsch_ext[f"t{š_ž}_nost_pref"] and not stem("t"+w) in lc.tzch_tsch_ext[f"t{š_ž}_st_pref"]:
                w = pref[:-1] + "č" + w[1:]
                w, pref = remove_prefix(w)
        # For cases when "tž" or "tš" is in the middle or end of the word
        if "t"+š_ž in w:
            if not w in lc.tzch_tsch_ext[f"t{š_ž}_nost"] and not stem(w) in lc.tzch_tsch_ext[f"t{š_ž}_st"]:
                w = w.replace("t"+š_ž, "č")
    return pref + w

# EE→IE
def change_ee(w):
    pref = ""
    w, pref = remove_prefix(w)
    if pref[-2:] == "ne" and w[:1] == "e":
        if "ni"+w in lc.nie_nost or stem("ni"+w) in lc.nie_st :
            pref = pref[:-1] + "i"
    
    return pref + w.replace("ee", "ie")

# ZT→ST, ZD→SD, ZP→SP
def change_zt_zd_zp(w):
    w, pref = remove_prefix(w)
    for z_tdp in ["zt", "zd", "zp"]:
        if z_tdp in w:
            if w in lc.z_tdp_exc[z_tdp+"_nost"] or stem(w) in lc.z_tdp_exc[z_tdp+"_st"]:
                if w in lc.z_tdp_dict_nost:
                    w = lc.z_tdp_dict_nost[w]
                elif stem(w) in lc.z_tdp_dict_st:
                    w = w.replace(stem(w), lc.z_tdp_dict_st[stem(w)])
            else:
                w = w.replace(z_tdp, "s"+z_tdp[-1])
    return pref + w

# CH→H
def change_ch(w):
    # If "ch" is in the word and word is not in exception list, "ch" is replaced with "h"
    if "ch" in w:
        if not w in lc.ch_nost and stem(w) not in lc.ch_st:
            return w.replace("ch", "h")
    return w

# Checks word for vowel followed by 2 consonants
def check_vcc(w):
    pprew, prew = None, "" # None, because during 1st iteration they both must not be the same
    for i in w: # This is done backwards to avoid finding vcc in prefixes
        if i == prew and not prew in vowels and pprew in ["a", "e", "i", "o", "u"]:
            return pprew + prew + i
        pprew = prew
        prew = i

def check_vcc_exc(w):
    st_w = stem(w)
    if st_w[-4:] == "ošāk":
        st_w = st_w[:-4]
    elif st_w[-2:] in ["āk", "oš"]:
        st_w = st_w[:-2]

    if st_w in st_vcc or w in nost_vcc:
        return True

# Replaces vowel + doubled consonants (hereinafter VCC) with vowel and one consonant (e.g., "patti"->"pati", "sattikt"->"satikt", "attiekksme"->"attieksme")
def change_vcc(w):
    ## MUST REWRITE COMMENTS
    # Next word without prefix will be processed to avoid vowel + doubled consonants in prefix (e.g. "ieeja")
    # If word still have 3 or more characters, multiple combinations of vowel + doubled consonants are generated and checked if they are present in the word. If they are and if word neather stemmed nor non-stemmed are present in exception list, doubled consonant is removed.
    # This process continues either until the word is in exception list or until there are no vowel with doubled consonant in the word. In both cases word is returned with its prefix

    # Words with 3 or more letters are verified
    if len(w) > 2:
        w, pref = remove_prefix(w)
        if pref:
            # When vcc is within pref (e.g., vissasodītākais, vissnoderīgākais)
            vcc = check_vcc(pref)
            if vcc and all(not i in pref for i in vcc_in_pref):
                pref = pref.replace(vcc, vcc[:2])

            # # When pref ends with vc and w starts with c (e.g., prettiesiski, prettēji)
            # if pref[-2:-1] in ["a", "e", "i", "o", "u"] and pref[-1:] == w[:1] and not w[:1] in vowels:
            #     # ???

            # When pref ends with v, but w starts with cc (e.g., "sa" and "vvaļa", "pa" and "ccietīgs")
            if w[:1] == w[1:2] and not w[:1] in vowels and pref[-1:] in ["a", "e", "i", "o", "u"]:
                if not w in vcc_in_pref_w_nost and not stem(w) in vcc_in_pref_w_st: # (e.g., "sa" and "vvaļa")
                    w = w[1:]
        while True:
            vcc = check_vcc(w)
            if not vcc or check_vcc_exc(w):
                return pref + w
            w = vcc[:2].join(w.split(vcc,1)) # Replaces 1 occurrence starting 
    else:
        return w

# Function for change_verb_ending(). Changes short to long vowel before ending
# input: w - verb to modify; verb_d - list of verbs in Latvian; end - w (verb) ending
def mod_verb(w, verb_list, end):
    # Removes w ending
    w = w[:-len(end)]
    if len(w) > 1:
        # To words with more than 2 characters, checks if 2nd to last character is consonant; and last – short vowel
        if w[-2] not in vowels:
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
    # Infinitive, past, future and II conj. present.
    # All: infinitive forms with ong vowel before endings -t and -ties
    # I: infinitive forms          This will not work for I conj. verbs, except for some words in infinitive form
    # II:infinitive forms; 
    #  pres - 3rd pers. future
    # III: infinitive forms; pres.  
    # Checks if word is in one of these categories. If it is, word is modified, else – passed unmodified to the next for loop to check if it is a verb of III conj. 1st group
    # 3rd pers. future (-s) is excluded, because this would change nouns in plural (e.g., "būves" should not be converted to verb "būvēs" since "būves" is also noun in plural)
    verb_end = ["sieties", "jāmies", "jamies", "jāties", "jaties", "simies", "amies", "aties", "ties", "jies", "siet", "sies", "jām", "jam", "jāt", "jat", "jos", "jās", "jas", "sim", "šos", "am", "ju", "ji", "ja", "šu", "si", "is", "t"]
    for end in verb_end:
        if w[-len(end):] == end: 
            # Infinitive form
            # Change short to long vowel in verb suffix and ending if verb is in all_verbs – list of all verbs without endings "ties"and "t"
            if end in ["ties", "t"]:
                mod_w = mod_verb(w, all_verbs, end)
                if mod_w:
                    return mod_w
            # Past, future and II conj. present
            # Change short to long vowel in verb suffix and ending if verb is in verbs.ii_iii_verbs – list of II and III conj. verbs without endings "ties"and "t"
            else:
                mod_w = mod_verb(w, verbs.ii_iii_verbs, end)
                w = mod_w if mod_w else w
                break
    # III conj. 1st group (-īt, -īties, -ināt, -ināties)
    # Checks if word is in this category. If it is, word is modified, else returned unmodified
    verb_end_III_first = ["ījamies", "ājamies", "ījaties", "ājaties", "amies", "aties", "ījam", "ājam", "ījat", "ājat", "ījas", "ājas", "am", "at", "as"]
    for end in verb_end_III_first:
        end_l = len(end)
        # Checks if any of these endings are at the end of the word 
        if w[-end_l:] == end:
            if end == "as":
                if any(i in w for i in ["kļūdas", "šaubas", "izbrīnas"]):
                    return w
            # For those words with endings that contains "j", aditional letter from word is added to ending
            # if end[0] == "j":
            #     end = w[-end_l-1:]  # Adding last char befor ending

                
            # Ending is removed; and then – prefix
            mod_w = w[:-end_l]
    
            # Checks if any – with and without prefix word can be found in iii_first_g list – list of stemmed III conj. 1st group verbs
            original_mod_w = mod_w
            # return "ARČA " + mod_w + end

            while True:
                if mod_w in verbs.iii_first_g:
                    end = end.replace("a", "ā")
                    return original_mod_w + end
                mod_w, pref = remove_prefix(mod_w, rm_all=False)
                if not pref:
                    return w
    return w

def change_suffix(w):
    st_w = stem(w)
    if len(st_w) > 2:
        st_w_mod = ""
        if st_w[-2:] == "ib" and st_w[-3] not in vowels:
            st_w_mod = st_w[:-2]+"īb"
            exc_nost, exc_st = w_p_e.ib_nost, w_p_e.ib_st
        elif st_w[-2:] == "ak":
            st_w_mod = st_w[:-2]+"āk"
            exc_nost, exc_st = w_p_e.ak_nost, w_p_e.ak_st

        elif len(st_w) > 4:
            if st_w[-3:] == "šan" and st_w[-4] in a_e_i_u and not st_w[-5] in vowels:
                st_w_mod = st_w[:-4] + s_to_l_vowels[st_w[-4]] + "šan"
                exc_nost, exc_st = w_p_e.c_sv_san_nost, w_p_e.c_sv_san_st
            elif st_w[-3:] == "taj" or st_w[-3:] == "tāj":
                if st_w[-4] in vowels:
                    # returns if w with short vowel + "taj" or "tāj" in wordlists
                    st_w_nopref = remove_prefix(st_w)[0]
                    w_nopref = remove_prefix(w)[0]
                    if st_w_nopref in w_p_e.sv_taj_st | w_p_e.sv_tāj_st or w_nopref in w_p_e.sv_taj_nost | w_p_e.sv_tāj_nost: #e.g., Getaja and vidutājs. For both there are no nostem_wordlists ending with vs and taj or tāj
                        return w
                    # if w with short vowel + converted "taj" to "tāj" is in wordlist, converted w is returned
                    w_mod = w_nopref.replace(st_w_nopref, st_w_nopref[:-3]+"tāj")
                    if st_w_nopref[:-3]+"tāj" in w_p_e.sv_tāj_st or w_mod in w_p_e.sv_tāj_nost:
                        return w.replace(st_w, st_w[:-3]+"tāj")

                    v = s_to_l_vowels[st_w[-4]] if st_w[-4] in s_to_l_vowels else st_w[-4] # changes short to long vowel
                    st_w_mod = st_w[:-4] + v + "tāj"
                    return w.replace(st_w, st_w_mod)
    
        if st_w_mod:
            nopref_w = remove_prefix(w)[0]
            if not nopref_w in exc_nost and not stem(nopref_w) in exc_st:
                return w.replace(st_w, st_w_mod)
    return w

def edit_w(w):
    # if w[-3:] == "ges":
    #     w = w[:-3] + "gas"
    # if w[-4:] == "dait":
    #     w = w[:-4] + "diet"

    w = change_prefix(w)
    w = change_tš_tž(w)
    w = change_ee(w)
    w = change_zt_zd_zp(w)
    w = change_ch(w)
    w = change_vcc(w)
    
    # Suffix and endings
    w = change_verb_ending(w)
    w = change_suffix(w)
    # Only one of following can apply
    # if len(st_w) > 2:
    #     w = change_c_ib(w, st_w)
    #     w = change_ak(w, st_w)
    # if len(st_w) > 4:
    #     w = change_c_v_san(w, st_w)
    #     w = change_v_taj(w, st_w)

    if w in old_w_dictionary.o_w_dict:
        w = old_w_dictionary.o_w_dict[w]

    return w

def split_and_edit_words(text, ee=False):
    """Splits text into words (Words can contain "'" and can be number word ending, like "arr'", "15ajjā")"""
    # words = re.findall(r"\w+(?:['-]\w+)?", text)
    if ee:
        words = set([w.strip(string.punctuation+string.digits) for w in text.split() if "ee" in w.lower()])
        conv_fun = change_ee
    else:
        words = set([w.strip(string.punctuation+string.digits) for w in text.split()])
        conv_fun = edit_w

    for w in words:
        mod_w = conv_fun(w.lower())
        if not w.islower():
            if w.istitle():
                mod_w = mod_w.title()
            elif w.isupper():
                mod_w = mod_w.upper()

        text = re.sub(rf'\b{re.escape(w)}\b', mod_w, text)

    return text

def change_key_val(text, d):
    for key, value in d.items():
        text = text.replace(key.upper(), value.upper())
        if len(key) > 1:
            text = text.replace(key.title(), value.title())
        text = text.replace(key, value)
    return text

# def change_ee_only(text):
#     ee_words = set([w.strip(string.punctuation) for w in text.split() if "ee" in w.lower()])
#     # ee_words = set(re.findall(r"\b\w*ee\w*\b", text, flags=re.IGNORECASE))
#     for w in ee_words:
#         mod_ee_w = change_prefix(w.lower())
#         mod_ee_w = change_ee(mod_ee_w)
#         if w.islower():
#             text = text.replace(w, mod_ee_w)
#         if w.istitle():
#             text = text.replace(w, mod_ee_w.title())
#         if w.isupper():
#             text = text.replace(w, mod_ee_w.upper())
#         else:
#             text = text.replace(w, mod_ee_w)
#     return text

def edit_text(text):
    # Ā, Ē, Ī, Ō, Ū, V, C, Z
    text = change_key_val(text, lc.lengthmarks_w_z_ſ)

    # S, Ž, Š
    text = text.replace("Ꞩ", "S")
    text = text.replace("ẜ", "s")
    text = change_key_val(text, lc.s_ž_š)

    return text

def convert(text, r=True, ee_only=False):
    """ Converts old fraktur latvian text to modern latvian text
        Inpustring: text - text to convert;
        Boolean: r - if True converts "ŗ" to "r"; ee_only - if True converts only "ee" to "ie" in text; change_S_to_Z - if True converts "S" to "Z"
    """
    if r:
        text = text.replace("Ŗ", "R").replace("ŗ", "r")
    if ee_only:
        return split_and_edit_words(text, True)

    # Converts old letters and prefixes in text to those used in modern Latvian
    text = edit_text(text)
    # Text modernization – splits text into words, converts them and returns modernized text 
    text = split_and_edit_words(text)
    return text
import js
js.convert = convert