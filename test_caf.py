import unittest
import filterengine

from geomutils  import *
from filterengine import FilterEngine


class TestChunks(unittest.TestCase):
    '''
    Unit Tests
    Tests chunk mechanism
    run with : python3 -m unittest test_caf.py 
    '''

    @staticmethod
    def computeSumOfAreas(chunks):
        area = 0
        for c in chunks:
            area += c.sizeX * c.sizeY
        return area

    def test_chunkClipIsAllDataset1(self):
        N = 10
        M = 5
        width  = filterengine.CHUNK_SIZE_X * N
        height = filterengine.CHUNK_SIZE_Y * M 
        clip   = Rectangle(0,0,width,height)
        chunks = FilterEngine.computeChunks(clip, width, height)
        self.assertEqual(len(chunks), N*M)
        self.assertEqual(TestChunks.computeSumOfAreas(chunks), width*height)


    def test_chunkClipIsAllDataset2(self):
        N = 10
        M = 5
        width  = filterengine.CHUNK_SIZE_X * N + 1
        height = filterengine.CHUNK_SIZE_Y * M + 1
        clip = Rectangle(0,0,width,height)
        chunks = FilterEngine.computeChunks(clip, width, height)
        self.assertEqual(len(chunks), (N+1)*(M+1))
        self.assertEqual(TestChunks.computeSumOfAreas(chunks), width*height)


    def test_chunkClipSmallerThanChunk(self):
        N = 10
        M = 5
        width  = filterengine.CHUNK_SIZE_X * N 
        height = filterengine.CHUNK_SIZE_Y * M 
        clip = Rectangle(100,100,300,200)
        chunks = FilterEngine.computeChunks(clip, width, height)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(TestChunks.computeSumOfAreas(chunks), 300*200)

    def test_chunkClipBiggerThanChunk(self):
        N = 10
        M = 5
        width  = filterengine.CHUNK_SIZE_X * N 
        height = filterengine.CHUNK_SIZE_Y * M 
        clip = Rectangle(100,100,filterengine.CHUNK_SIZE_X + 1,filterengine.CHUNK_SIZE_Y + 1)
        chunks = FilterEngine.computeChunks(clip, width, height)
        self.assertEqual(len(chunks), 4)
        self.assertEqual(TestChunks.computeSumOfAreas(chunks), (filterengine.CHUNK_SIZE_X + 1)*(filterengine.CHUNK_SIZE_Y + 1))

if __name__ == '__main__':
    unittest.main()
