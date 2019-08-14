import rasterio
from rasterio.windows import Window


class GeoDataset:
    '''
    The GeoDataset class represents a geo data file (e.g. geotiff) 

    Args:

            name : the name of the file

    Attributes:

            driver : the rasterio reader or writer

            width  : the width of the dataset

            height : the height of the dataset
    '''
    def __init__(self, name):
        self.name   = name
        self.driver = None
        self.width  = -1
        self.height = -1

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def openReadMode(self):
        '''
        Opens the file in read mode

        Args:

        Returns:

        '''
        self.driver = rasterio.open(self.name, mode = 'r')
        self.width = self.driver.width
        self.height = self.driver.height
        return
        
    def openWriteMode(self, profile):
        '''
        Opens the file in write mode

        Args:

                profile containing driver, height, width, count, dtype, crs, transform


        Returns:

        '''
        self.driver = rasterio.open(self.name, 'w', **profile)
        return


    def readRectangle(self, band, rectangle):
        '''
        Reads a Subset of the dataset defined by a rectangle

        Args:

                band:   band number

                rectangle: a Rectangle object defining the zone to read

        Returns:

            A 2D array of data
        '''
        return self.driver.read(band, window=Window(rectangle.originX,rectangle.originY, rectangle.sizeX, rectangle.sizeY))

    def writeRectangle(self, band, rectangle, data):
        '''
        Writes a Subset of data in the dataset

        Args:

                band:   band number

                rectangle: a Rectangle object defining the zone where to write

                data:   a 2d array containing the data to write

        Returns:

        '''
        self.driver.write(data, window=Window(rectangle.originX,rectangle.originY, rectangle.sizeX, rectangle.sizeY), indexes=band)
        return


    def close(self):
        '''
            Closes the file
        '''
        if self.driver is not None:
            self.driver.close()
        return

