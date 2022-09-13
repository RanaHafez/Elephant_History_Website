import requests
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory


app = Flask(__name__)


response_all_elephants = requests.get(url="https://elephant-api.herokuapp.com/elephants")
response_all_elephants.raise_for_status()
elephants = response_all_elephants.json()
print(len(elephants))


elephant = {
    '_id': '5cf1d0dbcd5e98f2540c4d1c',
    'index': 3,
    'name': 'Balarama',
    'affiliation': 'Dasara',
    'species': 'Asian',
    'sex': 'Male',
    'fictional': 'false',
    'dob': '1958',
    'dod': '-',
    'wikilink': 'https://en.wikipedia.org/wiki/Balarama_(elephant)',
    'image': 'https://elephant-api.herokuapp.com/pictures/missing.jpg',
    'note': 'A lead elephant of the world-famous Mysore Dasara procession.'}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def random_elephant():
    isDone = False
    while not isDone:
        response_random = requests.get(url="https://elephant-api.herokuapp.com/elephants/random")
        response_random.raise_for_status()
        random_elephant = response_random.json()
        print(random_elephant)
        print(random_elephant[0].keys())
        #
        if all(k in random_elephant[0] for k in ('name', 'image', 'sex', 'note')):
            isDone = True
    return render_template("rand_elephant.html", elephant=random_elephant[0])


@app.route("/get-elephant", methods=["GET", "POST"])
def get_elephant():
    name = request.form.get("name")
    response = requests.get(url=f"https://elephant-api.herokuapp.com/elephants/name/{name}")
    if response.content:
        elephant = response.json()
        return render_template("rand_elephant.html", elephant=elephant)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
