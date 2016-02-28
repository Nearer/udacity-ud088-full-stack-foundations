import flask
from flask import Flask, render_template, url_for, redirect, request
import re
from database_setup import DBSession, Restaurant, MenuItem

session = DBSession()

app = Flask(__name__)


@app.route('/restaurants/<int:r_id>/new', methods=['GET', 'POST'])
def new_menu_item(r_id):
    r = session.query(Restaurant).get(r_id)
    if not (r):
        flask.abort(404)
    if request.method == 'POST':
        if request.form.get('cancel', None):
            return redirect(url_for('restaurant_menu', r_id=r.id))
        else:
            name = request.form.get('name', None)
            price = process_price(request.form.get('price', None))
            description = request.form.get('description', None)
            if not name:
                error = 'Please enter a valid name'
                return render_template('new_menu_item.html', price=price, description=description, error=error)
            else:
                item = MenuItem(name=name, price=price, description=description, restaurant_id=r.id)
                session.add(item)
                session.commit()
            return redirect(url_for('restaurant_menu', r_id=r.id))
    else:
        return render_template('new_menu_item.html', price=None, description=None)


def process_price(raw_price):
    us_regex = re.compile(r'^\$?(\d*\.?\d+)$')
    if us_regex.match(raw_price):
        price_string = us_regex.match(raw_price).group(1)
        try:
            return float(price_string)
        except:
            return None


@app.route('/restaurants/<int:r_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(r_id, item_id):
    r = session.query(Restaurant).get(r_id)
    item = session.query(MenuItem).get(item_id)
    if not (r and item):
        flask.abort(404)
    if request.method == 'POST':
        if request.form.get('cancel', None):
            return redirect(url_for('restaurant_menu', r_id=r.id))
        else:
            name = request.form.get('name', None)
            price = process_price(request.form.get('price', None))
            description = request.form.get('description', None)
            if not name:
                error = 'Please enter a valid name'
                return render_template('edit_menu_item.html', item=item, error=error)
            else:
                item.name = name
                item.price = price
                item.description = description
                session.add(item)
                session.commit()
            return redirect(url_for('restaurant_menu', r_id=r.id))
    else:
        return render_template('edit_menu_item.html', item=item)


@app.route('/restaurants/<int:r_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def delete_menu_item(r_id, item_id):
    r = session.query(Restaurant).get(r_id)
    item = session.query(MenuItem).get(item_id)
    if not (r and item):
        flask.abort(404)
    if request.method == 'POST':
        if request.form.get('cancel', None):
            return redirect(url_for('restaurants'))
        else:
            session.delete(item)
            session.commit()
            return redirect(url_for('restaurant_menu', r_id=r.id))
    else:
        return render_template('delete_menu_item.html', item=item)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':
        if request.form.get('cancel', None):
            return redirect(url_for('restaurants'))
        name = request.form.get('name', None, type=str)
        if not name:
            error = 'Please enter a name.'
            return render_template('new_restaurant.html', error=error)
        else:
            r = Restaurant(name=name)
            session.add(r)
            session.commit()
            return redirect(url_for('restaurant_menu'), r_id=r.id)
    else:
        return render_template('new_restaurant.html', error=None)


@app.route('/restaurants/<int:r_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(r_id):
    if request.method == 'POST':
        name = request.form.get('name', None, type=str)
        if not name or request.form.get('cancel', None):
            return redirect(url_for('restaurants'))
        else:
            r = session.query(Restaurant).get(r_id)
            if r:
                r.name = name
                session.add(r)
                session.commit()
                return redirect(url_for('restaurants'))
            else:
                flask.abort(404)
    else:
        r = session.query(Restaurant).get(r_id)
        if r:
            return render_template('edit_restaurant.html', r=r)
        else:
            flask.abort(404)


@app.route('/restaurants/<int:r_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(r_id):
    if request.method == 'POST':
        r = session.query(Restaurant).get(r_id)
        session.delete(r)
        session.commit()
        return redirect(url_for('restaurants'))
    else:
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


@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/')
def redirect_to_home():
    return redirect(url_for('restaurants'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
