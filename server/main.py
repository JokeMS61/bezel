import sys
import pygame
from settings import *
from networkcontroller import NetworkController
from keyboardcontroller import keyboardController
from eventpublisher import EventPublisher
from dashmain import dashmain
from processdata import *

def main():
    #logger.debug('------- entry main --------')
    dash = dashmain()
    networkcontroller = NetworkController(dash)
    keyboardcontroller = keyboardController()
    eventpublisher = EventPublisher()
    eventpublisher.register(dash)
    keyboardcontroller.register(eventpublisher)
    networkcontroller.register(eventpublisher)

    clock = pygame.time.Clock()
    processdata = ProcessDataController()

    eventpublisher.deliverValues()
    dash.display()
    pygame.display.flip()


    logger.debug("-> run .............................................................")

    while True:

        clock.tick()

        if pygame.key.get_focused():

            if pygame.key.get_pressed()[pygame.K_q]:
                processdata.setValue(ID_QUIT,0)
                break

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:

                    logger.debug("event.key: %s", pygame.key.name(event.key))
                    keyboardcontroller.validatevalue(event)


        pygame.event.clear()

        fps = int(clock.get_fps())
        dash.setfps(fps)
        dash.update()
        rectangles = dash.getDrawArea()
        pygame.display.update(rectangles)


    networkcontroller.destroy()
    pygame.quit()

if __name__ == "__main__":

    main()
    sys.exit()
