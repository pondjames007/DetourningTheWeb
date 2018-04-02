import requests
from bs4 import BeautifulSoup
from PIL import Image
from envelopes import Envelope
import re
import os
import json

def hashtagTweets(q):
    html = requests.get("https://mobile.twitter.com/hashtag/" + q).text
    soup = BeautifulSoup(html, "html.parser")
    tweets = soup.select(".dir-ltr")
    images = soup.select(".media img")
    print("No. of tweets: " + str(len(tweets)))
    print("No. of images: " + str(len(images)))
    imgname = []
    
    for image in images:
        img_url = image.get("src")
        #print(img_url)
        imgname.append(download_file(img_url))
    
    count = 0
    for tweet in tweets:
        text = tweet.text
        image = ""
        # dir-ltr will come up with: whole text, hashtag only, pic url only
        # try to only keep the whole text
        if len(text.split()) is not 1:
            result = re.search(r"pic.twitter.com",text.split()[-1])
            #print(result)
            if result is not None:
                image = imgname[count]
                # print(image)
                text = " ".join(text.split()[:-1])
                # print(str(count)+"   IMAGE: "+ text)
                count += 1
            text.replace(q, "")
            sendMail(q, tweet.text, image)
            
            
    print(count)

def download_file(url, local_filename=None):
    if local_filename is None:
        local_filename = url.split('/')[-1]
        local_filename = local_filename.replace(":small", "")

    if os.path.exists(local_filename):
        return local_filename

    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    
    
    print(local_filename)
    return local_filename


def sendMail(title, text, image):
    with open("creds.json", "r") as infile:
        creds = json.load(infile)
    
    textbody = text.upper()
    html = '<b style="font-size: 50px; color: white; background-color: red">'+ text +'</b>'

    message = Envelope(
        from_addr = ("detourning2018.gmail.com", "Lol"), 
        to_addr = ("pondjames007@gmail.com", "James"),
        subject = title, 
        text_body = textbody,
        html_body = html
    )
    if image is not "":
        message.add_attachment(image)

    message.send("smtp.googlemail.com", login = creds['email_username'], password = creds['email_password'], tls = True)


q = "TeachMeSomethingIn5Words"
hashtagTweets(q)