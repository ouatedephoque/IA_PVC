__author__ = 'jeremy.wirth & jeshon.assuncao'

def ga_solve(file=None, gui=True, maxtime=0):
    print("ok")

if __name__ == "__main__":
    import sys, pygame

    pygame.init()

    bgcolor = 0, 0, 0
    linecolor = 255, 0, 0
    x = y = 0
    running = 1
    screen = pygame.display.set_mode((640, 400))
    LEFT = 1;

    while running:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            running = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            print "Click at (%d, %d)" % event.pos
            x, y = event.pos

        pygame.draw.circle(screen, linecolor, (x,y), 4)
        pygame.display.flip()

    ga_solve()
