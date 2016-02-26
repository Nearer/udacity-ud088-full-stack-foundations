import flask
from flask import Flask

from database_setup import MenuItem, DBSession, Restaurant

session = DBSession()

app = Flask(__name__)


@app.route('/')
def main_menu():
    string = ''
    for m in session.query(MenuItem).all():
        string += m.name + '<br>'
        string += '${}'.format(m.price) + '<br>'
        string += m.description + '<br><br>'
    return string


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    r = session.query(Restaurant).get(restaurant_id)
    if r:
        string = ''
        for m in r.menu_items:
            string += m.name + '<br>'
            string += m.description + '<br><br>'
        return string
    else:
        flask.abort(404)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
