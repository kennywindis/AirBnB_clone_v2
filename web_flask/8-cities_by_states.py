#!/usr/bin/python3
"""getting and rendering data from storage
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
import os
from flask import g


app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def render_state_obj():
    """render html list"""
    s = storage.all(State)
    c = storage.all(City)
    return render_template('8-cities_by_states.html', states=s, cities=c)


@app.teardown_appcontext
def teardown_db(self):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
