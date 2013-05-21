import sys
from flask import Flask, render_template
from werkzeug import SharedDataMiddleware

#sys.path.append("/home/simo/my_diary")

#from my_diary.extractor import Extractor
from my_diary import extractor

app = Flask(__name__)
#app.wsgi_app = SharedDataMiddleware(app.wsgi_app,{ '/static': '/statics/' } )

@app.route('/')
def hello_world():
    return render_template("skeleton.html", data=[])

@app.route("/<key>/")
def show(key):
    q = extractor.Extractor(key)
    status = q.status()
    photo = q.photos()
    #albums = q.albums(since=1356962300)
    link = q.links()
    all = status + photo + link #+albums
    all.sort(reverse=True)
    for x in all:
        x.analyze()
    return render_template("skeleton.html", data=all)
    

if __name__ == '__main__':
    app.run(debug=True)
