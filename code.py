import os
import csv
import time
import random
from signal import pause

from gpiozero import Button

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1327

from PIL import Image, ImageFont, ImageDraw

# Set default volume
current_volume = 10
current_channel = 4
mute_status = False


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


# Initialize screen
serial = i2c(port=1, address=0x3D)
device = ssd1327(serial)

# Setup volume graphics
volume_graphic_mute = Image.open('gfx/vdt-mute.jpg')
volume_graphic = {}
keys = range(21)
for i in keys:
    volume_graphic[i] = Image.open('gfx/vdt-' + str(i) + '.jpg')


# Setup channel graphics
c_standby = Image.open('gfx/c-standby.jpg')
channels = {}
with open('channels.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for index, row in enumerate(reader):
        channels[index] = {
            'Name': row['Name'],
            'StreamURL': 'http://ice' + str(random.randint(1, 6)) + '.somafm.com/' + row['Channel'] + '-128-aac',
            'Graphic': Image.open('gfx/c-' + row['Channel'] + ".jpg")
        }
        print(
            f"Channel: {channels[index]['Name']} URL: {channels[index]['StreamURL']}")


# Setup volume buttons
def mute():
    global mute_status
    if mute_status == True:
        device.display(volume_graphic[current_volume])
        os.system("mpc volume " + str(current_volume * 5))
        mute_status = False
    else:
        device.display(volume_graphic_mute)
        mute_status = True
        os.system("mpc volume 0")
    print(f"Mute status: {mute_status}")


def vol_rotate():
    global current_volume
    if not button_vol_dn.is_pressed:
        new_volume = clamp(current_volume + 1, 0, len(volume_graphic) - 1)
    else:
        new_volume = clamp(current_volume - 1, 0, len(volume_graphic) - 1)
    print(f"Current volume: {current_volume}")
    if not new_volume == current_volume:
        current_volume = new_volume
        os.system("mpc volume " + str(current_volume * 5))
        device.display(volume_graphic[current_volume])


button_vol_select = Button(4, pull_up=True)
button_vol_select.when_pressed = mute

button_vol_up = Button(5, pull_up=True)
button_vol_dn = Button(6, pull_up=True)
button_vol_up.when_activated = vol_rotate

# Setup channel buttons
def change_channel(current_channel):
    device.display(c_standby)
    print(f"Switching to {channels[current_channel]['Name']}")
    os.system("mpc clear")
    os.system("mpc add static.mp3")
    os.system("mpc play")
    time.sleep(5)
    os.system("mpc clear")
    os.system("mpc add " + channels[current_channel]['StreamURL'])
    device.display(channels[current_channel]['Graphic'])
    os.system("mpc play")


def ch_rotate():
    global current_channel
    if not button_ch_dn.is_pressed:
        new_channel = clamp(current_channel + 1, 0, len(channels) - 1)
    else:
        new_channel = clamp(current_channel - 1, 0, len(channels) - 1)
    print(f"Current channel: {channels[current_channel]['Name']}")
    if not new_channel == current_channel:
        current_channel = new_channel
        change_channel(current_channel)


button_ch_select = Button(22, pull_up=True)
button_ch_select.when_pressed = mute

button_ch_up = Button(23, pull_up=True)
button_ch_dn = Button(24, pull_up=True)
button_ch_up.when_activated = ch_rotate

# Show default volume
# device.display(volume_graphic[current_volume])

# Show default channel
device.display(channels[current_channel]['Graphic'])

pause()
