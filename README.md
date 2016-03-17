rdb-fullstack
=============

Common code for the Relational Databases and Full Stack Fundamentals courses

Notes from Jeremiah Richter:

This form contains the local web application that I developed in the Udacity course [Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088) and is designed to be run under the `vagrant` virtualization environment to satisfy dependencies. I ran it successfully under Arch Linux kernel 4.4.1-2-ARCH.

To run:
1. install `vagrant`.
2. cd to the directory of the **Vagrantfile**, `vagrant/`
3. run:
```
vagrant up
vagrant ssh
```
Note: to populate the SQLite database with some example restaurants/menu items, run:
```
python /vagrant/restaurantmenu/populate_restaurants.py
python /vagrant/restaurantmenu/populate_menu_items.py
```
in that order.

4. then, to start the web server, run:
```
python /vagrant/restaurantmenu/finalproject.py
```
5. navigate, using a browser, to http://localhost:5050/ to see the webpage.

Note: the CSS/Javascript are partially loaded from an online CDN, and internet connectivity may be required for optimal display/functionality
