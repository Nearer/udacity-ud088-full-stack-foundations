import flask
from flask import Flask, render_template, url_for

from database_setup import DBSession, Restaurant

session = DBSession()

app = Flask(__name__)


@app.route('/restaurants/<int:r_id>/new')
def new_menu_item(r_id):
    return 'Create a new menu item here'


@app.route('/restaurants/<int:r_id>/<int:item_id>/edit')
def edit_menu_item(r_id, item_id):
    return 'Edit a menu item here'


@app.route('/restaurants/<int:r_id>/<int:item_id>/delete')
def delete_menu_item(r_id, item_id):
    return 'Delete a menu item here'


@app.route('/restaurants/new')
def new_restaurant():
    return render_template('new_restaurant.html')


@app.route('/restaurants/<int:r_id>/edit')
def edit_restaurant(r_id):
    r = session.query(Restaurant).get(r_id)
    if r:
        return render_template('edit_restaurant.html', r=r)
    else:
        flask.abort(404)


@app.route('/restaurants/<int:r_id>/delete')
def delete_restaurant(r_id):
    r = session.query(Restaurant).get(r_id)
    if r:
        return render_template('delete_restaurant.html', r=r)
    else:
        flask.abort(404)


@app.route('/restaurants/<int:r_id>/')
def restaurant_menu(r_id):
    r = session.query(Restaurant).get(r_id)
    if r:
        return render_template('menu.html', r=r)
    else:
        flask.abort(404)


@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
