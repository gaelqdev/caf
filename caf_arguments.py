import sys

DEFAULT_INPUT  = 'ilatlon_float.tif'

def extractInputName():
    '''
    Extracts file input name from argv
    '''
    if ((len(sys.argv) > 1) and not (sys.argv[1].startswith('-'))):
        return sys.argv[1]
    else:
        return None

def extractOutputName():
    '''
    Extracts file output name from argv
    '''
    option = False
    name = None
    for arg in sys.argv:
        if option:
            name = arg
            break
        if arg == '-o':
            option = True
    return name

def extractClipCoords():
    '''
    Extracts clip coordinate from argv
    '''
    counter = -1
    coords = []
    for arg in sys.argv:
        if (counter > 3):
            break;
        if counter >= 0:
            coords.append(int(arg))
            counter += 1
        if arg == '-c':
            counter += 1
    return coords


def displayHelp():
    for arg in sys.argv:
        if arg == '-h' or arg == '--help':
            return True

