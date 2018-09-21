
#------------------------------------------------ MODULES
import evdev, os, time, threading
from evdev import InputDevice, categorize, ecodes
from force_feedback import *

#------------------------------------------------ SETUP CONTROLLER

#Find Playstation 3 Controller Device Location
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    if device.name == 'PLAYSTATION(R)3 Controller':
        ps3dev = device.fn

#Connect to Playstation 3 Controller
gamepad = InputDevice(ps3dev)

#------------------------------------------------ CONTROLLER DICTIONARY AND FUNCTIONS
cross = lambda: print('Kryds')
square = lambda: print('Firkant')
triangle = lambda: print('Trekant')
circle = lambda: print('Cirkel')
up = lambda: print('Op')
down = lambda: print('Ned')
left = lambda: print('Venstre')
right = lambda: print('Højre')
start = lambda: print('Start')
select = lambda: print('Select')
r1Press = lambda: print('R1')
r2Press = lambda: print('R2')
r3 = lambda: print('R3')
l1Press = lambda: print('L1')
l2Press = lambda: print('L2')
l3 = lambda: print('L3')
ps3 = lambda: print('PS3')

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

#------------------------------------------------ LAMBDA FUNCTIONS

clear = lambda: os.system('clear')
scale = lambda val, src, dst: (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

#------------------------------------------------ FUNCTIONS

f = Vibrate(ps3dev)
p = f.new_effect(1.0, 1.0, TIME_DELTA )

def rumble():
    f.play_efect((p))
    time.sleep(TIME_DELTA / 1000.0)
    f.stop_effect((p))

print(gamepad)



#loop and filter by event code and print the mapped label
for event in gamepad.read_loop():
    if event.type == 1 and event.value == 1:
            keypress[event.code]()

    elif event.type == 3:

        keyanalog[event.code] = event.value


        wall = 0.1

        if not (128*(1-wall) <= keyanalog[0] <= 128*(1+wall)) or not (128*(1-wall) <= keyanalog[1] <= 128*(1+wall)):
            print("Left X-axis: %.1f" % keyanalog[0])
            print("Left Y-axis: %.1f" % keyanalog[1])
            print()

        if not (128*(1-wall) <= keyanalog[2] <= 128*(1+wall)) or not (128*(1-wall) <= keyanalog[5] <= 128*(1+wall)):
            print("Right X-axis: %.1f" % keyanalog[2])
            print("Right Y-axis: %.1f" % keyanalog[5])
            print()

        if not (500*(1-wall) <= keyanalog[59] <= 500*(1+wall)) or not (500*(1-wall) <= keyanalog[60] <= 500*(1+wall)):
            print("Accelertometer (Left/Right): %.1f" % keyanalog[59])
            print("Accelertometer (Forward/Backward): %.1f" % keyanalog[60])
            print()

        if keyanalog[48]: print("L2:", keyanalog[48])
        if keyanalog[49]: print("R2:", keyanalog[49])
        if keyanalog[50]: print("L1:", keyanalog[50])
        if keyanalog[51]: print("R1:", keyanalog[51])





