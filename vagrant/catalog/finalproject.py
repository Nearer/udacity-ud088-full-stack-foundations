import re
from flask import Flask, render_template, url_for, abort, request, flash, get_flashed_messages, redirect
from database_setup import Restaurant, MenuItem, DBSession, COURSES

app = Flask(__name__)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        name = request.form.get('name', None, type=str)
        if not name:
            flash('You must enter a name between 1-80 characters.')
            return render_template('newrestaurant.html', error=True)
        else:
            r = Restaurant(name=name)
            session.add(r)
            session.commit()
            flash('New Restaurant added')
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    r = session.query(Restaurant).get(restaurant_id)
    if not r:
        abort(404)
    elif request.method == 'POST':
        name = request.form.get('name', None, type=str)
        if not name:
            flash('You must enter a new name between 1-80 characters.')
            return render_template('newrestaurant.html', error=True, r=r)
        else:
            r.name = name
            session.add(r)
            session.commit()
            flash('Successfully edited restaurant "{}".'.format(r.name))
            return redirect(url_for('showMenu', restaurant_id=r.id))
    else:
        return render_template('editrestaurant.html', r=r)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    r = session.query(Restaurant).get(restaurant_id)
    if not r:
        abort(404)
    elif request.method == 'POST':
        session.delete(r)
        session.commit()
        flash('Successfully deleted restaurant.')
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleterestaurant.html', r=r)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    r = session.query(Restaurant).get(restaurant_id)
    if r:
        return render_template('menu.html', r=r)
    else:
        abort(404)


def process_price(raw_price):
    us_regex = re.compile(r'^\$?(\d*\.?\d+)$')
    if us_regex.match(raw_price):
        price_string = us_regex.match(raw_price).group(1)
        try:
            return float(price_string)
        except:
            return None


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    r = session.query(Restaurant).get(restaurant_id)
    if not r:
        abort(404)
    elif request.method == 'POST':
        name = request.form.get('name', None, type=str)
        price = process_price(request.form.get('price', None, type=str))
        course = request.form.get('course', None, type=str)
        description = request.form.get('description', None, type=str)
        if not name:
            flash('You must enter a  name between 1-80 characters.')
            return render_template('newmenuitem.html', r=r, COURSES=COURSES, name=name,
                                   price=price, selected=course, description=description,
                                   error=True)
        else:
            item = MenuItem(name=name, price=price, description=description,
                            course=course, restaurant_id=r.id)
            session.add(item)
            session.commit()
            flash('New item added.')
            return redirect(url_for('showMenu', restaurant_id=r.id))
    else:
        return render_template('newmenuitem.html', r=r, COURSES=COURSES)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    r = session.query(Restaurant).get(restaurant_id)
    item = session.query(MenuItem).get(menu_id)
    if not r and item:
        abort(404)
    elif request.method == 'POST':
        name = request.form.get('name', None, type=str)
        price = process_price(request.form.get('price', None, type=str))
        course = request.form.get('course', None, type=str)
        description = request.form.get('description', None, type=str)
        if not name:
            flash('You must enter a  name between 1-80 characters.')
            return render_template('editmenuitem.html', r=r, COURSES=COURSES, name=item.name,
                                   price=price, selected=course, description=description,
                                   error=True)
        else:
            if name != item.name or price != item.price or course != item.course or description != item.description:
                item.name = name
                item.price = price
                item.description = description
                item.course = course
                session.add(item)
                session.commit()
                flash('Edited item "{}".'.format(item.name))
            return redirect(url_for('showMenu', restaurant_id=r.id))
    else:
        return render_template('editmenuitem.html', r=r, item=item, COURSES=COURSES)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    r = session.query(Restaurant).get(restaurant_id)
    item = session.query(MenuItem).get(menu_id)
    if not r and item:
        abort(404)
    elif request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Successfully deleted item.')
        return redirect(url_for('showMenu', restaurant_id=r.id))
    else:
        return render_template('deletemenuitem.html', r=r, item=item)

if __name__ == '__main__':
    app.secret_key = 'ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
