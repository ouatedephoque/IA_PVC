__author__ = 'jeremy.wirth & jeshon.assuncao'

import itertools
from individu import Individu
from city import City

def ga_solve(file=None, gui=True, maxtime=0):
    if file == None:
        showGame()
    else:
        openFile = open(file, "r")
        parseCities(openFile.read())

    populationInit()
    print(population)


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


def crossing():
    print("crossing...")

def selection():
    print("selection...")

def mutation():
    print("mutation...")


if __name__ == "__main__":
    import sys, pygame
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN

    pygame.init()
    screenSize = 500
    screen = pygame.display.set_mode((screenSize, screenSize))

    cities = []
    population = []

    cityColor = 255, 0, 0  # Red
    fontColor = 255, 255, 255  # White
    cityWidth = 2  # Width of one point

    try:
        ga_solve(str(sys.argv[1]))
    except:
        ga_solve()
