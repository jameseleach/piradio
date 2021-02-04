# This is temp.py
import time
from signal import pause
from gpiozero import Button

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1327

from PIL import Image, ImageFont, ImageDraw

# Set default volume
current_volume = 10
mute_status = False

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

# Initialize screen
serial = i2c(port=1, address=0x3D)
device = ssd1327(serial)

# Setup volume graphic dict
volume_graphic = {}
keys = range(21)
for i in keys:
    volume_graphic[i] = Image.open('gfx/vdt-' + str(i) + '.jpg')
volume_graphic_mute = Image.open('gfx/vdt-mute.jpg')

device.display(volume_graphic[current_volume])

# Setup volume buttons
def volume_up():
    global current_volume
    current_volume = clamp(current_volume + 1, 0, 20)
    print(f"Current volume: {current_volume}")
    device.display(volume_graphic[current_volume])

def volume_down():
    global current_volume
    current_volume = clamp(current_volume - 1, 0, 20)
    print(f"Current volume: {current_volume}")
    device.display(volume_graphic[current_volume])

def mute():
    global mute_status
    if mute_status == True:
        device.display(volume_graphic[current_volume])
        mute_status = False
    else:
        device.display(volume_graphic_mute)
        mute_status = True
    print(f"Mute status: {mute_status}")

button_select = Button(4, pull_up=True)
button_select.when_pressed = mute

button_vol_up = Button(5, pull_up=True)
button_vol_up.when_pressed = volume_up

button_vol_dn = Button(6, pull_up=True)
button_vol_dn.when_pressed = volume_down

pause()