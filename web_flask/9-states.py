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


@app.route('/states', strict_slashes=False)
def render_state():
    """render html list"""
    list_of_states = storage.all(State)
    return render_template('9-states.html', states=list_of_states)


@app.route('/states/<id>', strict_slashes=False)
def render_state_id(id=None):
    """render html list"""
    s = storage.all(State)
    c = storage.all(City)
    is_it = False
    state_name = None
    for v in s.values():
        if id == v.id:
            is_it = True
            state_name = v.name
    return render_template('9-states.html',
                           states=s,
                           cities=c,
                           is_it=is_it,
                           state_name=state_name,
                           id=id)


@app.teardown_appcontext
def teardown_db(self):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
