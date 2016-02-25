import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep

from jinja2 import Environment, PackageLoader

from database_setup import DBSession, Restaurant

jinja2_env = Environment(loader=PackageLoader('jinja2_templates', 'templates'))


class WebServerHandler(BaseHTTPRequestHandler):
    def get_template(self, template_name):
        t = jinja2_env.get_template(template_name)
        return t

    def render_str(self, template_name, **kwargs):
        t = self.get_template(template_name)
        return t.render(**kwargs)

    def render_page(self, template, **kwargs):
        page_str = self.render_str(template, **kwargs)
        self.wfile.write(page_str)

    def get_form(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        return form

    def send_301_html(self):
        self.send_response(301)
        self.end_headers()

    def get_css(self):
        f = open(curdir + sep + self.path)
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        self.wfile.write(f.read())

    def get_restaurants(self):
        self.send_200_html()
        session = DBSession()
        restaurants = session.query(Restaurant).order_by(Restaurant.id.desc()).all()
        self.render_page('restaurants.html', restaurants=restaurants)

    def get_restaurants_new(self):
        self.send_200_html()
        self.render_page('new_restaurant.html')

    def send_200_html(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def post_restaurants_new(self):
        form = self.get_form()
        new_name = form.getvalue('name')
        if new_name:
            session = DBSession()
            r = Restaurant(name=new_name)
            session.add(r)
            session.commit()
        self.send_response(301)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()

    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                self.get_restaurants()
            elif self.path.endswith('/restaurants/new'):
                self.get_restaurants_new()
            elif self.path.endswith('.css'):
                self.get_css()
        except IOError:
            self.send_error(404, 'File not found: {}'.format(self.path))

    def do_POST(self):
        if self.path.endswith('restaurants/new'):
            self.post_restaurants_new()


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print('Web server running on port {}'.format(port))
        server.serve_forever()

    except KeyboardInterrupt:
        print('^C entered, stopping web server...')
        server.socket.close()


if __name__ == '__main__':
    main()
