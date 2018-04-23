import requests
from selenium import webdriver
import json
import time
import random
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
import subprocess
import textwrap

# driver = webdriver.Chrome()

def getMovieFromKeywords(keyword):
    url = "https://api.themoviedb.org/3/search/movie/?api_key=1c8c076f2090a2952b05c32efdef0e4c&query="+keyword
    data = requests.get(url).text

    jsonformat = json.loads(data)

    with open("movieResult.json", "w") as infile:
        json.dump(jsonformat, infile, sort_keys=True, indent=4)

    return jsonformat

# getMovieFromKeywords("Avengers")

def getMovieTranslation(movie_id):
    url = "https://api.themoviedb.org/3/movie/" + movie_id + "/alternative_titles?api_key=1c8c076f2090a2952b05c32efdef0e4c"
    data = requests.get(url).text

    jsonformat = json.loads(data)

    with open("movieTranslation.json", "w") as infile:
        json.dump(jsonformat, infile, sort_keys=True, indent=4)
    
    return jsonformat

# getMovieTranslation(10528)

def translateString(title):
    # with open("movieTranslation.json", "r") as infile:
    #     translate_data = json.load(infile)
    
    # print(translate_data)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://translate.google.com")
    time.sleep(1)
    # print(translate_data["titles"][2]["title"])
    driver.find_element_by_id("source").send_keys(title)
    time.sleep(2)
    to_english = driver.find_element_by_id("gt-res-dir-ctr").text
    print(to_english)
    
    driver.quit()

    return to_english

# translateString()

def getImage(movie_id):
    url = "https://api.themoviedb.org/3/movie/" + movie_id + "/images?api_key=1c8c076f2090a2952b05c32efdef0e4c"

    data = requests.get(url).text
    
    jsonformat = json.loads(data)
    with open("images.json", "w") as infile:
        json.dump(jsonformat, infile, sort_keys=True, indent=4)

    prefix = "https://image.tmdb.org/t/p/original"
    imagepath = prefix + random.choice(jsonformat["backdrops"])["file_path"]
    # print(imagepath)
    
    imagename = download_file(imagepath, local_filename="posterRaw.jpg")
    # print(imagename)

    return imagename



def download_file(url, local_filename=None):
    if local_filename is None:
        local_filename = url.split('/')[-1]
        local_filename = local_filename.replace(":small", "")

    # if os.path.exists(local_filename):
    #     return local_filename

    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    
    
    # print(local_filename)
    return local_filename


def edit_image(imagename, words, i):
    image = Image.open(imagename)
    canvas = ImageDraw.Draw(image, 'RGBA')
    workingpath = os.getcwd() + "/fonts/"
    randomfont = [font for font in os.listdir(workingpath)]
    
    print(workingpath + random.choice(randomfont))
    useFont = workingpath + random.choice(randomfont)
    
    font = ImageFont.truetype(useFont, 120)

    lines = textwrap.wrap(words, width=15)
    y_height = 0
    for line in lines:
        w, h = canvas.textsize(line, font=font)
        canvas.rectangle([0, (image.size[1]-h)/2-20 + y_height, image.size[0], (image.size[1]+h)/2+20 + y_height], fill=(0, 0, 0, 20))
        canvas.text(((image.size[0]-w)/2, (image.size[1]-h)/2 + y_height) , line, font=font, fill=(255,255,255))
        y_height += h
   
    out_image_name = "mod_" + str(i) + "_" + imagename
    image.save(out_image_name)
    subprocess.call(["mv", out_image_name, "./static"])


# imagename = getImage("299536")
# edit_image("posterRaw.jpg", "LOLLLLLLLLLLLLLLLLLL KKKKKKKKKKKKKKKKKKKKKKKK", 1)
