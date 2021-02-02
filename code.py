# This is code.py
import time
from encoder import Encoder

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1327

from PIL import Image, ImageFont, ImageDraw

# Initialize screen
serial = i2c(port=1, address=0x3D)
device = ssd1327(serial)

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

volume_encoder = Encoder(4, 5, 6)
channel_encoder = Encoder(22, 23, 24)

# Setup volume graphic dict
volume_graphic = {}
keys = range(21)
for i in keys:
    volume_graphic[i] = Image.open('gfx/vdt-' + str(i) + '.jpg')

# Set default volume
current_volume = 10
device.display(volume_graphic[current_volume])

while True:
    if volume_encoder.rotate_up:
        current_volume = clamp(current_volume + 1, 0, 20)
        print(f"Current volume: {current_volume}")
        device.display(volume_graphic[current_volume])

    if volume_encoder.rotate_down:
        current_volume = clamp(current_volume - 1, 0, 20)
        print(f"Current volume: {current_volume}")
        device.display(volume_graphic[current_volume])

    if volume_encoder.button_selected:
        print("Volume button pressed")
    if channel_encoder.rotate_up:
        print("Channel up")
    if channel_encoder.rotate_down:
        print("Channel down")
    if channel_encoder.button_selected:
        print("Channel button pressed")

    time.sleep(0.1)