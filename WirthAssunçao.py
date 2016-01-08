__author__ = 'jeremy.wirth & jeshon.assuncao'

def ga_solve(file=None, gui=True, maxtime=0):
	if file == None :
		showGame()
	else:
		openFile = open(file, "r")
		parseCities(openFile.read())
    

def parseCities(f):
	lines = f.split("\n")
	for line in lines:
		word = line.split(" ")
		city = []
		city.append(int(word[1]))
		city.append(int(word[2]))
		cities.append(city)
	draw(cities)

def showGame():
    draw(cities)

    running = True
    while running:
        event = pygame.event.poll()

        if event.type == pygame.QUIT: # Quit the game
            running = 0

        elif event.type == pygame.MOUSEBUTTONDOWN : # Click
            print "Click at (%d, %d)" % event.pos
            cities.append(event.pos)
            draw(cities)

        elif event.type == KEYDOWN and event.key == K_RETURN: # Key Return press
            running = False

        pygame.display.flip() # Repaint

def draw(cities):
    screen.fill(0) # Erase all the screen

    i = 0
    for pos in cities:
        pygame.draw.circle(screen, cityColor, pos, cityWidth) # Show cities

        # Show labels of cities
        x, y = pos
        font = pygame.font.Font(None, 12)
        text = font.render("%i (%i;%i)" %(i, x, y), True, fontColor)
        screen.blit(text, (x+2, y-10))

        i += 1

    # Show the number of city
    font = pygame.font.Font(None, 30)
    text = font.render("Nombre : %i" % len(cities), True, fontColor)
    textRect = text.get_rect()
    screen.blit(text, textRect)

    pygame.display.flip() # Repaint


if __name__ == "__main__":
    import sys, pygame
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN

    pygame.init()
    screenSize = 500
    screen = pygame.display.set_mode((screenSize, screenSize))

    cities = []
    cityColor = 255, 0, 0 # Red
    fontColor = 255, 255, 255 # White
    cityWidth = 2 # Width of one point
    try:
		ga_solve(str(sys.argv[1]))
    except:
		ga_solve()
