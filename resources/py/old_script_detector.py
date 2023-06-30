# v3
def is_old_script(text):
    text = text.lower()
    if any(["ş" in text, " ee" in text, "ģch" in text]):
        return True

    repl_dict = {"arihu": "", "iholo": "", "iha": "", " ne": "", "ne": "", "ieej": "", "Ieej": "", "elp": "", "stab": "", "iso": "", "ISO": "", "slām": "", "sland": "", " uh ": "", " uh,": "", " uh.": "", " uh!": "", " eh ": "", " eh,": "", " eh.": "", " eh!": "", " ah ": "", " ah,": "", " ah.": "", " ah!": "", " oh ": "", " oh,": "", " oh.": "", " oh!": ""}
    for i, j in repl_dict.items():
        text = text.replace(i,j)
    v = 0
    if len(text)<80: # Title
        if any(["š" in text, "ž" in text, "č" in text]):
            v-=1
        if any([text.count("ā") + text.count("ē") + text.count("ī") + text.count("ū")]):
            v-=1
        if text.count("f")>2:
            v+=1
        if any(["ih" in text, " is" in text, "eh" in text, "uh" in text, "ah" in text, "oh" in text]):
            v+=1
        if any(["ee" in text, "fch" in text]):
            v+=2
        if any(["à" in text, "â" in text, "ê" in text, "è" in text, "î" in text, "ì" in text, "ô" in text, "û" in text]):
            v+=1
        if any(["ş" in text, "ſ" in text, "ẜ" in text]):
            v+=1

    else: # Not title
        if (text.count("š") + text.count("ž") + text.count("č"))>4:
            v-=1
        if (text.count("ā") + text.count("ē") + text.count("ī") + text.count("ū"))>4:
            v-=1
        if (text.count("w"))>3:
            v+=1
        if any(["ih" in text, "eh" in text, "uh" in text, "ah" in text, "oh" in text]):
            v+=1
        if (text.count("ee")+text.count("fch"))>3:
            v+=1
        if any(["à" in text, "â" in text, "ê" in text, "è" in text, "î" in text, "ì" in text, "ô" in text, "û" in text]):
            v+=1
        if any(["ş" in text, "ſ" in text, "ẜ" in text]):
            v+=1
    
    if v>0:
        return True
    else:
        return False