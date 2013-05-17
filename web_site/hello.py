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
    return 'Hello World!'

@app.route("/<key>/")
def show(key):
    q = extractor.Extractor(key)
    status = q.links()
    status = [s.analyze() for s in status]
    return render_template("skeleton.html", data=status) 
    

if __name__ == '__main__':
    app.run(debug=True)