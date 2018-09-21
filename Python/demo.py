
#------------------------------------------------ MODULES
import evdev, os, time, threading, fcntl, struct, array, time, sys
from evdev import InputDevice, categorize, ecodes
from os import listdir
from os.path import isfile, join

#Supress PyGame Welcome
sys.stdout = open(os.devnull, 'w')
import pygame
sys.stdout = sys.__stdout__

#------------------------------------------------ VARIABLES

EVIOCRMFF = 0x40044581
EVIOCSFF = 0x40304580
TIME_DELTA = 250    #VIBRATION LENGTH

album = "Mix Volume 2/"
wall = 0.1

#------------------------------------------------ CLASSES

class Vibrate:

    def __init__(self, file):
        self.ff_joy = open(file, "r+b", buffering=0)

    def close(self):
        self.ff_joy.close()

    def new_effect(self, strong, weak, length):
        effect = struct.pack('HhHHHHHxHH', 0x50, -1, 0, 0, 0, length, 0, int(strong * 0xFFFF), int(weak * 0xFFFF))
        a = array.array('h', effect)
        fcntl.ioctl(self.ff_joy, EVIOCSFF, a, True)
        return a[1]
        id = a[1]
        return (ev_play, ev_stop)

    def play_efect(self, id):
        if type(id) == tuple or type(id) == list:
            ev_play = ''
            for i in id:
                ev_play = ev_play + struct.pack('LLHHi', 0, 0, 0x15, i, 1)
        else:
            ev_play = struct.pack('LLHHi', 0, 0, 0x15, id, 1)
        self.ff_joy.write(ev_play)
        self.ff_joy.flush()

    def stop_effect(self, id):
        if type(id) == tuple or type(id) == list:
            ev_stop = ''
            for i in id:
                ev_stop = ev_stop + struct.pack('LLHHi', 0, 0, 0x15, i, 0)
        else:
            ev_stop = struct.pack('LLHHi', 0, 0, 0x15, id, 0)
        self.ff_joy.write(ev_stop)
        self.ff_joy.flush()

    def forget_effect(self, id):
        if type(id) == tuple or type(id) == list:
            for i in id:
                fcntl.ioctl(self.ff_joy, EVIOCRMFF, i)
        else:
            fcntl.ioctl(self.ff_joy, EVIOCRMFF, id)

#------------------------------------------------ SETUP CONTROLLER

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    if device.name == 'PLAYSTATION(R)3 Controller':
        ps3dev = device.fn

gamepad = InputDevice(ps3dev)
print(gamepad)

#------------------------------------------------ MUSIC
songs = sorted([f for f in listdir(album) if isfile(join(album, f))])
number = len(album) - 1

pygame.init()

#------------------------------------------------ LAMBDA FUNCTIONS

clear = lambda: os.system('clear')
scale = lambda val, src, dst: (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

#------------------------------------------------ FUNCTIONS

ff = Vibrate(ps3dev)
effect = ff.new_effect(1.0, 1.0, TIME_DELTA)

def rumble():
    ff.play_efect((effect))
    time.sleep(TIME_DELTA / 1000.0)
    ff.stop_effect((effect))

#------------------------------------------------ CONTROLLER FUNCTIONS

def cross():
    print("Kryds")
    threading.Thread(target=rumble).start()


square = lambda: print('Firkant')
triangle = lambda: print('Trekant')
circle = lambda: print('Cirkel')


up = lambda: pygame.mixer.music.unpause()
down = lambda: pygame.mixer.music.pause()

def left():
    global number
    number = (number - 1) % len(album)
    pygame.mixer.music.load(album + songs[number])
    pygame.mixer.music.play(0)

def right():
    global number
    number = (number + 1) % len(album)
    pygame.mixer.music.load(album + songs[number])
    pygame.mixer.music.play(0)

start = lambda: print('Start')
select = lambda: print('Select')
r1Press = lambda: print('R1')
r2Press = lambda: print('R2')
r3 = lambda: print('R3')
l1Press = lambda: print('L1')
l2Press = lambda: print('L2')
l3 = lambda: print('L3')
ps3 = lambda: print('PS3')

#------------------------------------------------ CONTROLLER DICTIONARY

keypress = {
    302: cross,
    303: square,
    300: triangle,
    301: circle,
    292: up,
    294: down,
    295: left,
    293: right,
    291: start,
    288: select,
    299: r1Press,
    297: r2Press,
    290: r3,
    298: l1Press,
    296: l2Press,
    289: l3,
    704: ps3
}

keyanalog = {
    0: 128,     #Left Joystick X-Position
    1: 128,     #Left Joystick Y-Position
    2: 128,     #Right Joystick X-Position
    5: 128,     #Right Joystick Y-Position
    48: 0,      #L2 Analog
    49: 0,      #R2 Analog
    50: 0,      #L1 Analog
    51: 0,      #R1 Analog
    59: 500,    #Accelerometer (Left/Right) Position
    60: 500     #Accelerometer (Forward/Backward) Position
}

#------------------------------------------------ EVENT LOOP

for event in gamepad.read_loop():

    #Key presses
    if event.type == 1:
        #Key down
        if event.value == 1:
            keypress[event.code]()

    #Analog presses
    elif event.type == 3:

        keyanalog[event.code] = event.value

        if not keyanalog[0] in range(120, 136) or not keyanalog[1] in range(120, 136):
            print("Left X-axis: %.1f" % keyanalog[0])
            print("Left Y-axis: %.1f" % keyanalog[1])
            print()

        if not keyanalog[2] in range(120, 136) or not keyanalog[5] in range(120, 136):
            print("Right X-axis: %.1f" % keyanalog[2])
            print("Right Y-axis: %.1f" % keyanalog[5])
            print()

        if not keyanalog[59] in range(450, 550) or not keyanalog[60] in range(450, 550):
            print("Accelertometer (Left/Right): %.1f" % keyanalog[59])
            print("Accelertometer (Forward/Backward): %.1f" % keyanalog[60])
            print()

        if keyanalog[48] and event.code == 48: print("L2:", keyanalog[48])
        if keyanalog[49] and event.code == 49: print("R2:", keyanalog[49])
        if keyanalog[50] and event.code == 50: print("L1:", keyanalog[50])
        if keyanalog[51] and event.code == 51: print("R1:", keyanalog[51])
