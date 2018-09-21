#import evdev
import evdev
from evdev import InputDevice, categorize, ecodes

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
	if device.name == 'PLAYSTATION(R)3 Controller':
		ps3dev = device.fn

gamepad = InputDevice(ps3dev)

print(gamepad)

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    #filters by event type
    if event.type == ecodes.EV_KEY:
        print(event)