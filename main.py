import os.path
import time
import sys

import caf_arguments

from geodataset   import GeoDataset
from filter       import Filter2D
from filterengine import FilterEngine

FILTER_SIZE    = 7

HELP_TEXT      = ('usage: python3 main.py input [-c x y width height] [-o output]\n'
                    'Options and arguments (and corresponding environment variables):\n'
                    'input     : name of the input file\n'
                    '-c        : coordinates of the clip origin and size of the clip. Ex: -c 400 400 1000 1000\n'
                    '-h        : print this help message and exit (also --help)\n'
                    '-o        : name of the output file\n\n'
                    'Examples:\n python3 main.py ilatlon_float.tif\n python3 main.py ilatlon_float.tif -c 200 500 1000 800 -o out.tif')

def buildDefaultOutputName(inputName):
    '''
    Builds default output file name  'blabla.tif'  -> 'blabla-out-hpf-<windowSize>.tif'
    
    Args:

            inputName : a string containing the input name

    Returns:

            a string containing the output name
    '''
    splits = os.path.splitext(inputName)
    return (splits[0] + '-out-hpf-' + str(FILTER_SIZE) + splits[1])



def displayHelp():
    '''
    Tests if display help is asked (option --help or -h)
    '''
    if ((len(sys.argv) > 1) and  (sys.argv[1] == '--help')):
        return True


if __name__ == "__main__":

    if displayHelp():
        print (HELP_TEXT)
        sys.exit()

    startTime       = time.time()

    inputName       = caf_arguments.extractInputName()
    if inputName is None:
        print (HELP_TEXT)
        sys.exit()

    outputName      = caf_arguments.extractOutputName()
    if outputName is None:
        outputName = buildDefaultOutputName(inputName)

    clipsCoords     = caf_arguments.extractClipCoords();

    input           = GeoDataset(inputName)
    output          = GeoDataset(outputName)
    highPassFilter  = Filter2D(Filter2D.initHighPassFilter(FILTER_SIZE))
    filterEngine    = FilterEngine(input,output,highPassFilter)

    if (len(clipsCoords) < 3):
        filterEngine.processOnClip()
    else:
        filterEngine.processOnClip(x=clipsCoords[0], y=clipsCoords[1], width=clipsCoords[2], height=clipsCoords[3])

    print('Finished '+str(float("{0:.2f}".format(time.time() - startTime))) + ' seconds')
    print('Wrote '+outputName)

   



