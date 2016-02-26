# -*- coding: utf-8 -*-
__author__ = 'jeremy.wirth & jeshon.assuncao'

import itertools
from math import *
from random import randint
from individu import Individu
from city import City

population = []
cities = []

def ga_solve(file=None, gui=True, maxtime=0):
    if file == None:
        showGame()
    else:
        openFile = open(file, "r")
        parseCities(openFile.read())

    populationInit()

    while(len(population) > 1):
        print "Population size : ", len(population)
        selection()
        crossing()
        mutation()
        drawPath()

    print "\nChemin trouvé ! : ", population[0]

def parseCities(f):
    lines = f.split("\n")
    for line in lines:
        word = line.split(" ")

        name = word[0]
        posX = int(word[1])
        posY = int(word[2])
        city = City(name, posX, posY)

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

    for individu in population:
        for i in range(0, len(individu.city)):
            listCities = individu.city

            # Dessine tout les chemins
            cityStart = listCities[0]
            for i in range(1, len(listCities)):
                cityEnd = listCities[i]
                pygame.draw.line(screen, pathColor, (cityStart.posX, cityStart.posY), (cityEnd.posX, cityEnd.posY))  # Show path
                cityStart = cityEnd

        # Relie le dernier avec le premier
        cityStart = individu.city[len(individu.city)-1]
        cityEnd = individu.city[0]
        pygame.draw.line(screen, pathColor, (cityStart.posX, cityStart.posY), (cityEnd.posX, cityEnd.posY))  # Show path

    pygame.display.flip() #refresh
    
    # pause après avoir dessiné un chemin, enter pour quitter
    #running = True
    #while running:
    #    event = pygame.event.poll()
    #    if event.type == KEYDOWN and event.key == K_RETURN:
    #        running = False
    
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
    listIndividus = list(itertools.islice(itertools.permutations(cities), 1000))

    for solution in listIndividus:
        individu = Individu(solution)
        population.append(individu)
	
    # Tri des individus en fonction de leur distance de parcours
	population.sort(key=lambda individu: individu.totalDistance)

# Site reference : http://labo.algo.free.fr/pvc/algorithme_genetique.html
def selection():
    populationSelected = list()

    # Selection Elitisme
    #NB_INDIVIDUS_TO_KEEP = int(ceil(len(population) * 0.5)) # = 50% de la population

    #for i in range(0, NB_INDIVIDUS_TO_KEEP): # Garde les meilleurs 50% d'individus
    #    populationSelected.append(population[i])
    
    # Selection par roulette
    NB_INDIVIDUS_SELECT = int(ceil(len(population)/2));
    somme = 0
    for individu in population :
        somme += individu.totalDistance

    for i in range(0, NB_INDIVIDUS_SELECT):
        populationSelected.append(selectIndividu(somme))

    replacePopulation(populationSelected)
# Fonction pour la selection des parents
def selectIndividu(s):
    tirage = randint(0, int(s))
    somme = 0
    for individu in population :
        somme += individu.totalDistance
        if somme > tirage:
            return individu
    
def crossing():
    populationCrossed = list()

    # Si la taille de la liste est impaire on pop le dernier individu
    # car il n'aura pas d'autre parent pour faire un enfant
    if(len(population)%2 != 0):
        indexLast = len(population)-1
        lastIndividu = population.pop(indexLast)
        populationCrossed.append(lastIndividu)

    # Parcours la liste des parents à croiser
    for i in range(0, len(population)/2):
        # Selectionne les individus 2 par 2 (0 et 1, 2 et 3, etc.)
        A = population[i*2]
        B = population[(i*2)+1]

        #  A et B sont deux individu sélectionnés pour créer un nouvel individu
        citiesA = A.city
        citiesB = B.city
    
        # Cassure : a gauche de la cassure on met les ville de A, a droite de la cassure les villes de B
        cassure = int(len(citiesA)/2)
    
        listCities = []
        
        # Insère les villes de A
        for i in range(0, cassure):
            listCities.append(citiesA[i])
    
        # Insère les villes de B, on vérifie que la ville n'existe pas deja dans la liste sinon on cherche la ville suivante
        for i in range(cassure, len(citiesB)):
            city = citiesB[i]
            indice = int(city.name[1])
            while checkCityExist(listCities, city):
                indice += 1
                if(indice >= len(cities)):
                    indice = 0
                city = cities[indice]
            listCities.append(city)

        individuEnfant = Individu(listCities)
        populationCrossed.append(individuEnfant)

    replacePopulation(populationCrossed)

def checkCityExist(listCities, city):
    # Vérifie si la ville existe déjà dans la liste en comparant leur nom
    for c in listCities:
        if(c.name == city.name):
            return True
    return False

def mutation():
    populationMutated = list(population)

    for i in range(0, len(population)):
        mutateOrNo = randint(0, 1) # Nb aléatoire, 1 ou 0

        # Permet de ne pas muter tous les individus mais seulement certains (aléatoire)
        if(mutateOrNo == 1):
            C = population[i]
            CToMutate = C

            # Permutation de deux villes:
            rand1 = randint(0, len(CToMutate.city)-1)
            rand2 = randint(0, len(CToMutate.city)-1)

            tmp = CToMutate.city[rand1]
            CToMutate.city[rand1] = CToMutate.city[rand2]
            CToMutate.city[rand2] = tmp

            populationMutated.remove(C)
            populationMutated.append(CToMutate)

    # Tri des individus en fonction de leur distance de parcours
	populationMutated.sort(key=lambda individu: individu.totalDistance);

    replacePopulation(populationMutated)

def replacePopulation(newPopulation):
    global population
    population = []
    population = list(newPopulation)

if __name__ == "__main__":
    import sys, pygame
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN

    pygame.init()
    screenSize = 500
    screen = pygame.display.set_mode((screenSize, screenSize))

    pathColor = 0, 0, 255  # Blue
    cityColor = 255, 0, 0  # Red
    fontColor = 255, 255, 255  # White
    cityWidth = 2  # Width of one point

    try:
        ga_solve(str(sys.argv[1]))
    except:
        ga_solve()
