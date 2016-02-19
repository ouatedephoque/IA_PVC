__author__ = 'jeshon.assuncao'

from city import City
import math

class Individu:
    def __init__(self, listCity):
        self.city = listCity
        self.totalDistance = self.evaluation()

    def __repr__(self):
        return '(%s)' % (', '.join(str(x) for x in self.city))

    def evaluation(self):
        distTot = 0.0

        for index in range(len(self.city)):
            if(index+1 < len(self.city)):
                distTot += self.distBetweenTwoCities(self.city[index], self.city[index+1])
            else:
                distTot += self.distBetweenTwoCities(self.city[index], self.city[0])
                break

        return distTot

    def distBetweenTwoCities(self, cityA, cityB):
        return math.sqrt(pow(cityB.posX - cityA.posX, 2) + pow(cityB.posY - cityA.posY, 2))
