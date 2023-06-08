from flask import Flask, render_template, jsonify, Response
import random
import loginapi
import wikiscraper
import uggscraper
import webbrowser

#
# Main program, hosts the webserver and webpage
#
webbrowser.open('http://127.0.0.1:5000')


app = Flask(__name__)
app.static_folder = "./static"
app.template_folder = "./templates"
lc = loginapi.LeagueClient.initalizeClient()
#dd = loginapi.DragonDeez.getChampNumberList()
#ugg = uggscraper.getUGGdata()
#wiki = wikiscraper.WikiClass.getwikitable()

@app.route("/")
def rendertemplate():
    return render_template("index.html")

@app.route("/LC")
def initialize():
    global lc
    data = lc.doEverythingLive()
    return jsonify(data)

@app.route("/getsession")
def get_session():
    pass

@app.route("/offlinedatatest")
def test():
    global lc
    data = lc.offlinetheory()
    return jsonify(data)

@app.route("/updatenumber")
def jsonNumber():
    return jsonify(number=random.randint(0, 100))

@app.route("/something")
def newnumber():
    return random.randint(0, 100)

if __name__ == "__main__":

    app.run(debug=True)