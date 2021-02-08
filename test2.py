#this is test2.py

# namedtuple 
# https://www.geeksforgeeks.org/namedtuple-in-python/


import csv
import random
from PIL import Image
from collections import namedtuple

stream = namedtuple('stream',['name', 'url', 'description', 'graphic'])
streams = {}
with open('streams.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for index, row in enumerate(reader):
        streams[index] = stream(
            row['Name'],
            'http://ice' + str(random.randint(1, 6)) + '.somafm.com/' + row['Stream'] + '-128-aac',
            'Generic description',
            Image.open('gfx/image-stream-' + row['Stream'] + ".jpg"),
            
        )