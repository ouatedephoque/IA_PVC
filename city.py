__author__ = 'jeshon.assuncao'

class City:
    def __init__(self, name, posX, posY):
        self.name = name
        self.posX = posX;
        self.posY = posY;

    def __repr__(self):
        return "%s(%i,%i)" % (self.name, self.posX, self.posY)