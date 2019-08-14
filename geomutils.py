
class Rectangle:
    def __init__(self, originX, originY, sizeX, sizeY):
        self.originX  = originX
        self.originY  = originY
        self.sizeX    = sizeX
        self.sizeY    = sizeY

    def __str__(self):
        return '['+str(self.originX)+','+str(self.originY)+','+str(self.sizeX)+','+str(self.sizeY)+']'

    def addMargin(self, margin):
        '''
        Adds a Margin to the Rectangle 

        Args:
            
                margin    : a margin object

        Returns:

                a new instance of a Rectangle augmented with the margin
        '''
        return Rectangle(self.originX-margin.left, self.originY-margin.top, self.sizeX+margin.left+margin.right, self.sizeY+margin.top+margin.down)

class Margin:
    def __init__(self, top, right, down, left):
        self.top   = top
        self.right = right
        self.down  = down
        self.left  = left