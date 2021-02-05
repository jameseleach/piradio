# This is temp.py
import time
from signal import pause
from gpiozero import Button

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1327

from PIL import Image, ImageFont, ImageDraw

import csv

# Set default volume
current_volume = 10
current_channel = 4
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

# Show default volume
device.display(volume_graphic[current_volume])

channels = {}
with open('channels.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        i = reader.line_num -1
        channels[i] = {'Name': row['Name'], 'Description': row['Description'], 'StreamURL': row['StreamURL'], 'Graphic': Image.open('gfx/' + row['Graphic'])}
        print(row['Channel'], row['Name'],row['Description'], row['StreamURL'])

# Setup volume buttons
def mute():
    global mute_status
    if mute_status == True:
        device.display(volume_graphic[current_volume])
        mute_status = False
    else:
        device.display(volume_graphic_mute)
        mute_status = True
    print(f"Mute status: {mute_status}")

def vol_rotate():
    global current_volume
    if not button_vol_dn.is_pressed:
        current_volume = clamp(current_volume + 1, 0, len(volume_graphic)-1)
        print(f"Current volume: {current_volume}")
        device.display(volume_graphic[current_volume])
    else:
        current_volume = clamp(current_volume - 1, 0, len(volume_graphic))
        print(f"Current volume: {current_volume}")
        device.display(volume_graphic[current_volume])

button_vol_select = Button(4, pull_up=True)
button_vol_select.when_pressed = mute

button_vol_up = Button(5, pull_up=True, bounce_time=0.1)
button_vol_dn = Button(6, pull_up=True, bounce_time=0.1)
button_vol_up.when_activated = vol_rotate

# Setup channel buttons
def ch_rotate():
    global current_channel
    if not button_ch_dn.is_pressed:
        current_channel = clamp(current_channel + 1, 1, len(channels)-1)
    else:
        current_channel = clamp(current_channel - 1, 1, len(channels)-1)
    print(f"Current channel: {current_channel}")
    device.display(channels[current_channel]['Graphic'])

button_ch_select = Button(22, pull_up=True)
button_ch_select.when_pressed = mute

button_ch_up = Button(23, pull_up=True, bounce_time=0.1)
button_ch_dn = Button(24, pull_up=True, bounce_time=0.1)
button_ch_up.when_activated = ch_rotate

pause()