__author__ = 'JK'

from settings import *
import time
import httplib
import base64
import StringIO
import pygame
import sys
from pygame.locals import *

class Camtrendnet():
   def __init__(self, ip, username='admin', password='admin'):
       """

       :param ip:
       :param username:
       :param password:
       """
       self.ip = ip
       self.username = username
       self.password = password
       self.base64string = base64.encodestring('%s:%s' % (username, password))[:-1]

   def connect(self):
       h = httplib.HTTP(self.ip)
       h.putrequest('GET','/cgi-bin/image.jpg')
       h.putheader('Authorization', 'Basic %s' % self.base64string)
       h.endheaders()
       errcode, errmsg, headers = h.getreply()
       self.file = h.getfile()

   def update(self, window, size, offset):
       data = self.file.readline()
       if data[0:15] == 'Content-Length:':
           count = int(data[16:])
           s = self.file.read(count)
           while s[0] != chr(0xff):
               s = s[1:]

               p = StringIO.StringIO(s)

               try:
                   campanel = pygame.image.load(p).convert()
                   campanel = pygame.transform.scale(campanel, size)
                   window.blit(campanel, offset)

               except Exception, x:
                   print x

               p.close()

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((660,500), 0, 32)

    pygame.display.set_caption('trendnet.py')

    background = pygame.Surface((660,500))
    background.fill(pygame.Color('#E8E8E8'))
    screen.blit(background, (0,0))

    camera = Camtrendnet('webcam.vhs-ehingen.de', 'admin', 'admin')
    camera.connect()

    while True:

        camera.update(screen, (640,480), (10,10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

        time.sleep(.01)
