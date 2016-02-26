import flask
from flask import Flask, render_template

from database_setup import MenuItem, DBSession, Restaurant

session = DBSession()

app = Flask(__name__)


@app.route('/restaurants/<int:restaurant_id>/new')
def new_menu_item(restaurant_id):
    return 'Create a new menu item here'


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/edit')
def edit_menu_item(restaurant_id, item_id):
    return 'Edit a menu item here'


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/delete')
def delete_menu_item(restaurant_id, item_id):
    return 'Delete a menu item here'


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    r = session.query(Restaurant).get(restaurant_id)
    if r:
        return render_template('menu.html', r=r)
    else:
        flask.abort(404)


@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/')
def main_menu():
    string = ''
    for m in session.query(MenuItem).all():
        string += m.name + '<br>'
        string += '${}'.format(m.price) + '<br>'
        string += m.description + '<br><br>'
    return string


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
