import numpy as np

def parse_dice(dices_txt:str):
    """You have to write xdy+a-b, a and b are optional"""
    nb = 0
    dice = 0
    modi = 0

    parse = dices_txt.split('d')
    nb = int(parse[0])

    parse = parse[1].split('+') # then parses = ["j","x-y"]
    print(parse)
    if (len(parse)==1): # (j-y)
        parse = parse[0].split('-') # then parses = ["j","y"]
        dice = int(parse[0])
        if (len(parse)==2): # (idj  -x)
            modi -= int(parse[1])
    else: # (idj +x -?)
        dice = int(parse[0])
        parse = parse[1].split('-') # then parses = ["j","x","y"]
        if (len(parse)==2): # (idj +x -y)
            modi -= int(parse[1])
            modi += int(parse[0])
        else:  # (idj +x)
            modi += int(parse[0])

    return [nb, dice, modi]


def roll(dices_txt:str):
    nb, dice, mod = parse_dice(dices_txt)

    #if (nb<0): Error

    rdlist = np.random.randint(low=1,high=dice,size=nb)

    value = np.sum(rdlist)
    return list(rdlist), value+mod
