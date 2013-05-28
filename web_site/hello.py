import sys
from flask import Flask, render_template
from werkzeug import SharedDataMiddleware

#sys.path.append("/home/simo/my_diary")

#from my_diary.extractor import Extractor
from my_diary import extractor

import prova

app = Flask(__name__)
#app.wsgi_app = SharedDataMiddleware(app.wsgi_app,{ '/static': '/statics/' } )

@app.route('/')
def hello_world():
    return render_template("skeleton.html", data=[])


@app.route("/<key>/")
def show(key):
    q = extractor.Extractor(key)
    #status = q.status()
    #photo = q.photos()
    #albums = q.albums(since=1356962300)
    #link = q.links()
    
    #post = q.posts()
    #print prova.i
    thread = q.threads()
    
    #try:
    #    thread = q.threads()
    #except:
    #    pass
    #finally:
    #    print prova.i
    #    thread = []

    #all = post + thread #status + photo + link +post #+albums

    all = thread
    s = set(all)
    all = list(s)
    all.sort(reverse=True)
    for x in all:
        """
        try:
            x.analyze()
        except:
            pass
        finally:
            print "\n"*5, prova.i"""
        x.analyze()
    return render_template("skeleton.html", data=all)

    
t = """
{% for x in data %}
  <p>{{x}} {{loop.index0}}</p>
{% endfor %}

"""

@app.route("/template")
def show_template():
    from jinja2 import Environment
    env = Environment()
    temp = env.from_string(t) 
    return temp.render(data = [1, 2, 3])

    

if __name__ == '__main__':
    app.run(debug=True)
