from math  import ceil

from geomutils  import *
from geodataset import GeoDataset
from filter     import Filter2D

CHUNK_SIZE_X = 1024
CHUNK_SIZE_Y = 1024

class FilterEngine:
    '''
    The FilterEngine class represents the engine which will perform the filter on a GeoDataset and writes the result 

    Args:

        input  : a GeoDataset object containing the input of the process

        output : a GeoDataset object containing the output of the process

        filter : a Filter2D object containing the filter to apply

    Examples:

            input           = GeoDataset(inputName)

            output          = GeoDataset(outputName)

            highPassFilter  = Filter2D(Filter2D.initHighPassFilter(FILTER_SIZE))

            filterEngine    = FilterEngine(input,output,highPassFilter)

            filterEngine.processOnClip(x=500, y=1000, width=2000, height=2000)

            filterEngine.processOnClip()
    '''
    def __init__(self, input, output, filter):
        self.input  = input
        self.output = output
        self.filter = filter


    def processOnClip(self, **kwargs):
        '''
        Processes the Filtering on a clip zone and writes the result in the output file

        First writes the input into the output

        Then applies the filter on the clip and writes the filtered clip in the output

       Args:

               x=...      : X origin of the clip (optional)

               y=...      : Y origin of the clip (optional)

               width=...  : width of the clip (optional)

               height=... : height of the clip (optional)


        Example:

                filterEngine.processOnClip()  # filters the all input

                filterEngine.processOnClip(x=400, y=400, width=1000, height=1000)  #filters one clip

        Returns:
       '''
        self.input.openReadMode()
        outputProfile = self.input.driver.profile
        outputProfile.update(count=1)
        self.output.openWriteMode(outputProfile)
        
        # copy the original data in output
        dataSetRectangle = Rectangle(0,0,self.input.getWidth(),self.input.getHeight())
        self.filterAndWrite(dataSetRectangle, None)

        # extract clip rectangle from arguments
        # if not specified set the clip to the all dataset
        x = kwargs.get('x', -1)
        y = kwargs.get('y', -1)
        w = kwargs.get('width', -1)
        h = kwargs.get('height', -1)

        if (x < 0) or (y < 0) or (w < 0) or (h < 0):
            clipRectangle = dataSetRectangle
        else:
            clipRectangle = Rectangle(x, y, w, h)

        # apply the filter on the clip and write the result in output
        self.filterAndWrite(clipRectangle, self.filter)

        self.input.close()
        self.output.close()
        return

    def filterAndWrite(self, clip, filter):
        '''

         Compute the number of chunks needed to process the filtering on the clip zone

         Loops on chunks

         For each chunk: 

               add a margin depending on the size of the filter window

               read the input chunk

               apply the filter, if the filter is not None

               remove the previous margin from the result

               write the result in the output


        Args:
                clip     : a Rectangle Object defining the zone in the dataset


                filter   : a Filter object. If None, no filter is applied, input is just copied in output 



        Returns:
        '''

        chunks = FilterEngine.computeChunks(clip, self.input.driver.width, self.input.driver.height)

        for chunk in chunks:
            if filter is None :
                margin  = Margin(0,0,0,0)
            else :
                margin  = FilterEngine.computeMarginForRectangle(chunk, self.filter.windowSizeX, self.filter.windowSizeY, self.input.driver.width, self.input.driver.height)

            augmentedChunkRect = chunk.addMargin(margin)

            inputChunkData     = self.input.readRectangle(1, augmentedChunkRect)

            if filter is None :
                result  = inputChunkData
            else :
                result  = filter.apply(inputChunkData)
                       
            resultNoMargin     = result[margin.left:margin.left+chunk.sizeX][margin.top:margin.top+chunk.sizeY]

            self.output.writeRectangle(1, chunk, resultNoMargin)

        return


    @staticmethod
    def computeChunks(clip, datasetWidth, dataSetHeight):
        '''
         Splits the clip into chunks

        Args:

                clip          : a Rectangle object defining the clipping zone 

                datasetWidth  : dataset Width

                datasetHeight : dataset Height

        Returns:

                array of Rectangle objects defining the chunks that cover the clipping zone

        '''

        result = []

        inputWidth    = min(datasetWidth - clip.originX,clip.sizeX)
        inputHeight   = min(dataSetHeight - clip.originY,clip.sizeY)
        inputWidth    = max(0, inputWidth)
        inputHeight   = max(0, inputHeight)
        
        chunksDimX    = ceil(inputWidth/CHUNK_SIZE_X)
        chunksDimY    = ceil(inputHeight/CHUNK_SIZE_Y)
        
        for i in range(chunksDimX):
           for j in range(chunksDimY):
            chunkRectangle     = FilterEngine.computeChunk(i, j, CHUNK_SIZE_X, CHUNK_SIZE_Y, inputWidth, inputHeight, clip.originX, clip.originY)
            result.append(chunkRectangle)       
                   
        return result


    @staticmethod
    def computeChunk(indexX, indexY, chunkWidth, chunkHeight, datasetWidth, datasetHeight, offsetX, offsetY):
        '''
        Computes the Rectangle containing one chunk given its indices, taking in account dataset dimensions
        

        Args:
            
                indexX        : the X index of the chunk in the dataset

                indexY        : the Y index of the chunk in the dataset

                chunkWidth    : the width of the chunk

                chunkHeight   : the height of the chunk

                datasetWidth  : the width of the dataset

                datasetHeight : the height of the dataset


        Returns:

                a Rectangle defining the coordinates of the chunk in the 2D dataset
        '''
        
        chunkOriginX = indexX*CHUNK_SIZE_X + offsetX
        chunkOriginY = indexY*CHUNK_SIZE_Y + offsetY

        chunkSizeX   = CHUNK_SIZE_X
        if (chunkOriginX + chunkSizeX > datasetWidth + offsetX):
            chunkSizeX = datasetWidth - indexX*CHUNK_SIZE_X
        chunkSizeY   = CHUNK_SIZE_Y
        if (chunkOriginY + chunkSizeY > datasetHeight + offsetY):
            chunkSizeY = datasetHeight - indexY*CHUNK_SIZE_Y
        
        return Rectangle(chunkOriginX,chunkOriginY,chunkSizeX,chunkSizeY)



    @staticmethod
    def computeMarginForRectangle(rectangle, filterWindowWidth, filterWindowHeight, datasetWidth, datasetHeight):
        '''
        Computes the Margin needed to filter one chunk given its index, taking in account the window of a filter and the dataset dimensions
        
        Args:

                rectangle           : a Rectangle Object defining the zone in the dataset
            
                filterWindowWidth   : the width of the filter window
            
                filterWindowHeight  : the height of the filter window
            
                datasetWidth        : the width of the dataset
            
                datasetHeight       : the height of the dataset

        Returns:
            
                a Margin object
        '''

        marginUp    = int(filterWindowWidth/2)
        marginRight = int(filterWindowWidth/2)
        marginDown  = int(filterWindowHeight/2)
        marginLeft  = int(filterWindowHeight/2)

        if (rectangle.originY - marginUp < 0):
            marginUp = rectangle.originY
        if (rectangle.originY + rectangle.sizeY + marginDown >= datasetHeight):
            marginDown = datasetHeight - 1 - rectangle.originY - rectangle.sizeY

        if (rectangle.originX - marginLeft < 0):
            marginLeft = rectangle.originX
        if (rectangle.originX + rectangle.sizeX + marginRight >= datasetWidth):
            marginRight = datasetWidth - 1 - rectangle.originX - rectangle.sizeX

        return Margin(marginUp,marginRight,marginDown,marginLeft)



