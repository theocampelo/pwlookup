class bcolors:
    HEA = '\033[95m'
    BLU = '\033[94m'
    GRE = '\033[92m'
    YEL = '\033[93m'
    RED = '\033[91m'
    CLR = '\033[0m'
    BOL = '\033[1m'
    UND = '\033[4m'

def green(string):
    return bcolors.GRE + string + bcolors.CLR

def blue(string):
    return bcolors.BLU + string + bcolors.CLR

def yellow(string):
    return bcolors.YEL + string + bcolors.CLR

def red(string):
    return bcolors.RED + string + bcolors.CLR