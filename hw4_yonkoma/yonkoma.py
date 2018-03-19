import subprocess
import requests
from bs4 import BeautifulSoup
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import glob

#url = sys.argv[1]
url = "https://www.youtube.com/watch?v=7s71D2kQrFE"
fileName = "whoissmarter.mp4"

# download video
subprocess.call(['youtube-dl', url, '-o', fileName, '--write-sub'])

# make supercut
subprocess.call(['videogrep', '-i', fileName, '--search', 'WHO|WHO\'S|WHY|KIDS IN|WELL'])

# turn the supercut into images
subprocess.call(['ffmpeg', '-i', 'supercut.mp4', '-vf', 'fps=1','frame-%03d.jpg'])

# load the subtitles that you want (the subtitle file is modified manually)
subtitle = [line.split("\t")[-1] for line in open('cut_subtitle_mod.txt', 'r')]
print(subtitle)

# put images and subtitles together
blank_image = Image.new('RGB', (1280, 2880), (0, 0, 0))

# load image files (images are selected manually)
jpegs = sorted(glob.glob('kids/*.jpg'))

x = 0
y = 0
i = 0
c = 1

for jpg in jpegs:
    im = Image.open(jpg)
    canvas = ImageDraw.Draw(im)

    font = ImageFont.truetype('/Library/Fonts/Verdana.ttf', 40)
    canvas.text((300, 550), subtitle[i], font=font, fill=(255, 255, 255))
    print(jpg)
    blank_image.paste(im, (x, y))

    width = im.size[0]
    height = im.size[1]
    i += 1
    y += height
    if y >= 2880:
        y = 0
        # x += width+40
        name = 'yonkoma%d.jpg' % (c)
        print(name)
        blank_image.save(name)
        c += 1


