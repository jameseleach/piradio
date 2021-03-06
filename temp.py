#this is test.py

import os
import csv
import time
import random
from signal import pause
from gpiozero import Button
from mpd import MPDClient
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1327
from PIL import Image


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def myround(x, base=5):
    return base * round(x/base)


def mpd_connect(client):
    try:
        client.ping()
    except:
        client.connect("localhost", 6600)


def mpd_status(client):
    mpd_connect(client)
    return client.status()


# Initialize screen
serial = i2c(port=1, address=0x3D)
device = ssd1327(serial)

# Initialize MPD interface
client = MPDClient()
status = mpd_status(client)

# Set / get defaults
#default_channel = 4
#default_volume = 50
current_volume = myround(int(status['volume']))
current_song = 

selected_display = 'volume'
display_timeout = 5
mute_info = {'state': False, 'volume': status['volume']}


# Setup volume graphics
# volume_graphic_mute = Image.open('gfx/vdt-mute.jpg')
volume_graphic_pause = Image.open('gfx/image-pause.jpg')
volume_graphic = {}
keys = range(21)
for i in keys:
    volume_graphic[i] = Image.open('gfx/image-volume-' + str(i) + '.jpg')


# Setup playlist and graphics
img_standby = Image.open('gfx/image-standby.jpg')
streams = {}
client.clear()
with open('streams.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for index, row in enumerate(reader):
        streams[index] = {
            'Name': row['Name'],
            'StreamURL': 'http://ice' + str(random.randint(1, 6)) + '.somafm.com/' + row['Stream'] + '-128-aac',
            'Graphic': Image.open('gfx/image-stream-' + row['Stream'] + ".jpg")
        }
        client.add(streams[index]['StreamURL'])
        print(
            f"stream: {streams[index]['Name']} URL: {streams[index]['StreamURL']}")


# Setup volume buttons
button_vol_select = Button(4, pull_up=True)
button_vol_up = Button(5, pull_up=True)
button_vol_dn = Button(6, pull_up=True)


def update_volume_graphic():
    global selected_display
    global_display = 'volume'
    status = mpd_status(client)
    device.display(volume_graphic[myround(int(status['volume']))/5])


def mute():
    global mute_info
    status = mpd_status(client)
    if mute_info['state'] == True:
        client.setvol(mute_info['volume'])
        mute_info['state'] = False
    else:
        mute_info['state'] = True
        mute_info['volume'] = status['volume']
        client.setvol(0)
    print(f"Mute status: {mute_info['state']}")
    update_volume_graphic()


def vol_rotate():
    status = mpd_status(client)
    cv = status['volume']
    if not button_vol_dn.is_pressed:
        client.volume(5)
    else:
        client.volume(-5)
    status = mpd_status(client)
    print(f"Current volume: {status['volume']}")
    if not cv == status['volume']:
        update_volume_graphic()


button_vol_select.when_pressed = mute
button_vol_up.when_activated = vol_rotate

# Setup stream buttons
button_ch_select = Button(22, pull_up=True)
button_ch_up = Button(23, pull_up=True)
button_ch_dn = Button(24, pull_up=True)


def update_stream_graphic():
    global selected_display
    global_display = 'stream'
    status = mpd_status(client)
    device.display(streams[int(status['song'])]['Graphic'])


def play_pause():
    status = mpd_status(client)
    cs = status['state']
    client.pause()
    status = mpd_status(client)
    if status['state'] == 'pause':
        device.display(volume_graphic_pause)
    else:
        update_stream_graphic()
    print(f"Status: {status['state']}")


def change_stream(current_stream):
    # unused for now
    device.display(img_standby)
    print(f"Switching to {streams[current_stream]['Name']}")
    os.system("mpc clear")
    os.system("mpc add static.mp3")
    os.system("mpc play")
    time.sleep(5)
    os.system("mpc clear")
    os.system("mpc add " + streams[current_stream]['StreamURL'])
    device.display(streams[current_stream]['Graphic'])
    os.system("mpc play")


def ch_rotate():
    status = mpd_status(client)
    if not button_ch_dn.is_pressed:
        new_stream = clamp(int(status['song']) + 1, 0, len(streams) - 1)
    else:
        new_stream = clamp(int(status['song']) - 1, 0, len(streams) - 1)
    if not new_stream == int(status['song']):
        print(
            f"Switching from {streams[int(status['song'])]['Name']} to {streams[new_stream]['Name']}")
        client.play(new_stream)
        update_stream_graphic()
        # change_stream(current_stream)


button_ch_select.when_pressed = play_pause
button_ch_up.when_activated = ch_rotate

# Show and play default stream
device.display(streams[default_channel]['Graphic'])
client.play(default_channel)

pause()
#while True:
#    ct = time.time()
#    if selected_display == 'volume':
#        update_volume_graphic()
#        if time.time() >= ct + display_timeout:
#            global_display = 'stream'
#    else:
#        update_stream_graphic()

