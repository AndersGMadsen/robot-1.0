from os import listdir
from os.path import isfile, join
import pygame

album = "Mix Volume 2/"
songs = [f for f in listdir(album) if isfile(join(album, f))]
number = 0

pygame.init()

pygame.mixer.music.load(album + songs[number])






"""import pygame
pygame.init()

pygame.mixer.music.load('brandy.mp3')
pygame.mixer.music.play(0)
input()
pygame.mixer.music.pause()
input()
pygame.mixer.music.unpause()
input()
"""