from flask import Flask, request, render_template, Markup, redirect, url_for, session
import grabMovieInfo
from iso3166 import countries
import random

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
prefix = "https://image.tmdb.org/t/p/original"

# set a root directory
@app.route('/', methods=["GET", "POST"])  
def home(): # the home page will be on localhost:5000/
    if request.method == "GET":
        return render_template("home.html")
    else:
        keyword = request.form.get("moviename", "")
        if keyword != "":
            session["keyword"] = keyword
            return redirect(url_for('search'))
        else:
            return render_template("home.html", posters="No Result Found")
        

@app.route('/search')
def search():
    keyword = session.get("keyword", None)
    if keyword != "":
        search_results = grabMovieInfo.getMovieFromKeywords(keyword)
        posters = ""
        for result in search_results["results"]:
            if result["poster_path"] is not None:
                url = Markup('<a href="/language?id='+ str(result["id"]) + "&title=" + result["original_title"] + '"><img src="' + prefix + result["poster_path"] + '" width="300"></a>')
                
            else:
                url = Markup('<img src="/static/noimage.svg">')
            posters += url
        # print(posters)
        
        return render_template("search.html", posters=posters, keyword=keyword)
    else:
        return render_template("home.html")


@app.route('/language', methods=["GET", "POST"])
def language():
    if request.method == "GET":
        movieid = request.args.get("id","")
        keyword = request.args.get("title","")
        language_results = grabMovieInfo.getMovieTranslation(movieid)
        raw_img_path = grabMovieInfo.getImage(movieid)
        print(raw_img_path)
        posters = ""
                
        for i, title in enumerate(language_results["titles"]):
            # title = random.choice(language_results["titles"])
            if title["iso_3166_1"] != "US" and title["iso_3166_1"]!="GB" and title["iso_3166_1"]!="AU" and title["iso_3166_1"]!="CA":       
                if title["iso_3166_1"] == "TW":
                    country = "Taiwan"
                else:
                    country = countries.get(title["iso_3166_1"]).name
                translated_title = grabMovieInfo.translateString(title["title"])
                print(country)
                print(translated_title)
                grabMovieInfo.edit_image(raw_img_path, translated_title, i)
                url = Markup('<h3>' + country + '</h3>' + '<img src="/static/mod_' + str(i) + '_posterRaw.jpg" width="900">')
                posters += url
        

        return render_template("result.html", posters=posters, keyword=keyword)
        