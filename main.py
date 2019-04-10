from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)


@app.route("/")
def index():
    time = datetime.now().strftime("%c")
    return render_template("index.html", current_time=time)


@app.route('/name')
def name():
    first_name = request.args.get('first', '')
    last_name = request.args.get('last', '')
    return render_template("name.html", name=f"{first_name} {last_name}")

@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():

    if request.method == 'POST':
        # Handle POST requests & save entries to a file
        name = request.form['guest_name']
        with open("guests.txt", 'a') as f:
            f.write(f"{name}\n")

        # Redirect the user...
        return redirect(url_for("guestbook"))

    # Read all of the guest entries from a file.
    guests = []
    with open("guests.txt") as f:
        guests = f.readlines()

    return render_template("guestbook.html", guests=guests)


@app.route('/api/guestbook')
def guestbook_api():
    guests = []
    with open("guests.txt") as f:
        guests = f.readlines()

    data = json.dumps({
        'count': len(guests),
        'guests': guests,
    })

    return data