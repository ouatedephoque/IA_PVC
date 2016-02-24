# -*- coding: utf-8 -*-
__author__ = 'jeremy.wirth & jeshon.assuncao'

import itertools
from random import randint
from individu import Individu
from city import City

def ga_solve(file=None, gui=True, maxtime=0):
    if file == None:
        showGame()
    else:
        openFile = open(file, "r")
        parseCities(openFile.read())

    populationInit()
    selection()
    


def parseCities(f):
    lines = f.split("\n")
    for line in lines:
        word = line.split(" ")

        name = word[0]
        posX = int(word[1])
        posY = int(word[2])
        city = City(name, posX, posY)
        #city.append(int(word[1]))
        #city.append(int(word[2]))
        cities.append(city)
    draw(cities)


def showGame():
    draw(cities)

    running = True
    while running:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:  # Quit the game
            running = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Click
            print "Click at (%d, %d)" % event.pos

            name = "v%i" % len(cities)
            posX, posY = event.pos
            city = City(name, posX, posY)

            cities.append(city)
            draw(cities)

        elif event.type == KEYDOWN and event.key == K_RETURN:  # Key Return press
            running = False

        pygame.display.flip()  # Repaint

def drawPath():
    draw(cities)
    listCities = population[0].city
    
    #dessine tout les chemins
    cityStart = listCities[0]
    for i in range(1, len(listCities)):
        cityEnd = listCities[i]
        pygame.draw.line(screen, pathColor, (cityStart.posX, cityStart.posY), (cityEnd.posX, cityEnd.posY))  # Show path
        cityStart = cityEnd
    
    #ferme la boucle
    cityStart = listCities[len(listCities)-1]
    cityEnd = listCities[0]
    pygame.draw.line(screen, pathColor, (cityStart.posX, cityStart.posY), (cityEnd.posX, cityEnd.posY))  # Show path    
    
    pygame.display.flip() #refresh
    
    #pause après avoir dessiné un chemin, enter pour quitter
    running = True
    while running:
        event = pygame.event.poll()
        if event.type == KEYDOWN and event.key == K_RETURN:
            running = False
    
def draw(cities):
    screen.fill(0)  # Erase all the screen

    i = 0
    for city in cities:
        pygame.draw.circle(screen, cityColor, (city.posX, city.posY), cityWidth)  # Show cities

        # Show labels of cities
        font = pygame.font.Font(None, 12)
        text = font.render("%s (%i;%i)" % (city.name, city.posX, city.posY), True, fontColor)
        screen.blit(text, (city.posX + 2, city.posY - 10))

        i += 1

    # Show the number of city
    font = pygame.font.Font(None, 30)
    text = font.render("Nombre : %i" % len(cities), True, fontColor)
    textRect = text.get_rect()
    screen.blit(text, textRect)

    pygame.display.flip()  # Repaint


def populationInit():
    listIndividus = list(itertools.islice(itertools.permutations(cities), 50))

    for solution in listIndividus:
        individu = Individu(solution)
        population.append(individu)
	
    #tri des individus en fonction de leur distance de parcours
	population.sort(key=lambda individu: individu.totalDistance)

#site reference : http://labo.algo.free.fr/pvc/algorithme_genetique.html
def selection():
    #selection simple : on prend le meilleur individu et un individu au hasard
    #individuA = population[0]
    #individuB = population[randint(1,len(population)-1)]
    
    #selection par roulette
    somme = 0
    for individu in population :
        somme += individu.totalDistance
    individuA = selectIndividu(somme)
    individuB = selectIndividu(somme)    
        
    crossing(individuA, individuB)

#fonction pour la selection des parents
def selectIndividu(s):
    tirage = randint(0, int(s))
    somme = 0
    for individu in population :
        somme += individu.totalDistance
        if somme >= tirage:
            return individu
    
def crossing(A, B):
    #A et B sont deux individu sélectionnés pour créer un nouvel individu
    citiesA = A.city
    citiesB = B.city
    
    #cassure : a gauche de la cassure on met les ville de A, a droite de la cassure les villes de B
    cassure = int(len(citiesA)/2)
    
    listCities = []
        
    #insère les villes de A
    for i in range(0, cassure):
        listCities.append(citiesA[i])
    
    #insère les villes de B, on vérifie que la ville n'existe pas deja dans la liste sinon on cherche la ville suivante
    for i in range(cassure, len(citiesB)):
        city = citiesB[i]
        indice = int(city.name[1])
        while checkCityExist(listCities, city):
            indice += 1
            if(indice >= len(cities)):
                indice = 0
            city = cities[indice]
        listCities.append(city)
        
    individuC = Individu(listCities)
    mutation(individuC)

def mutation(C):
    #permutation de deux villes:
    rand1 = randint(0, len(C.city)-1)
    rand2 = randint(0, len(C.city)-1)
    
    tmp = C.city[rand1]
    C.city[rand1] = C.city[rand2]
    C.city[rand2] = tmp
    
    insertAndResort(C)

def insertAndResort(C):
    #on remplace le pire individu par celui que l on vient de créer et on retrie la liste
    population[len(population)-1] = C
    population.sort(key=lambda individu: individu.totalDistance)
    drawPath()
    
    
def checkCityExist(listCities, city):
    #vérifie si la ville existe déjà dans la liste en comparant leur nom
    for c in listCities:
        if(c.name == city.name):
            return True
    return False
    
if __name__ == "__main__":
    import sys, pygame
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN

    pygame.init()
    screenSize = 500
    screen = pygame.display.set_mode((screenSize, screenSize))

    cities = []
    population = []

    pathColor = 0, 0, 255  # Blue
    cityColor = 255, 0, 0  # Red
    fontColor = 255, 255, 255  # White
    cityWidth = 2  # Width of one point

    try:
        ga_solve(str(sys.argv[1]))
    except:
        ga_solve()
