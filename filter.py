import numpy as np
from scipy import ndimage

class Filter2D:
        '''
        The Filter2D class represents a 2D linear filter

        Args :
                        
                array :  an array representing the filter window, e.g:

                [[-1, -1, -1]]

                [-1,  8, -1]

                [-1, -1, -1]]

        Attributes:

                windowSizeX  : width of the window

                windowSizeY  : height of the window

                window       : 2D array

        '''

    
        def __init__(self, array):
                self.windowSizeX = len(array[0])
                self.windowSizeY = len(array)
                self.window      = np.array(array)

        def apply(self,inputMatrix):
                '''
                Applies the filter to the input 2D matrix (matrix convolved with filter window)

                Args:

                        inputMatrix :  2D array of data


                Returns:

                        an 2D array of data, result of the filtering, same size as the argument inputMatrix
                '''
                result = ndimage.convolve(np.array(inputMatrix), self.window, mode='reflect')
                return result

        @staticmethod
        def initHighPassFilter(size):
                '''
                Initializes the window of a High Pass Filter, e.g. for size 3 :

                                [[-1, -1, -1]]

                                [-1,  8, -1]

                                [-1, -1, -1]]

                Args:

                                size :  size of the window (should be an odd integer)

                Returns:

                                an 2D array of size [size, size]

                '''
                
                window = [[-1 for x in range(size)] for y in range(size)]
                window[int(size/2)][int(size/2)] = size * size - 1
                return window