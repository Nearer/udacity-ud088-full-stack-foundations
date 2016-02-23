import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        output = ''
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>Hello!'
                output += '<form method="POST" enctype="mutipart/form-data" action="/hello"' \
                          '><h2>What would you like me to say?</h2><input name="message" type="text"' \
                          '><input type="submit" value="Submit"></form>'
                output += '</body></html>'
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>&#161Hola!' \
                          '<a href="hello"> Back to Hello </a>'
                output += '<form method="POST" enctype="mutipart/form-data" action="/hello"' \
                          '><h2>What would you like me to say?</h2><input name="message" type="text"' \
                          '><input type="submit" value="Submit"></form>'
                output += '</body></html>'
            self.wfile.write(output)
            print(output)
            return

        except IOError:
            self.send_error(404, 'File not found: {}'.self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()
            form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                             'CONTENT_TYPE': self.headers['Content-Type'],
                             })
            print(form)
            message_content = form.getvalue('message')

            output = ''
            output += '<html><body>'
            output += '<h1>{}</h1>'.format(message_content)
            output += '<form method="POST" action="/hello"' \
                      '><h2>What would you like me to say?</h2><input name="message" type="text"' \
                      '><input type="submit" value="Submit"></form>'
            output += '</body></html>'
            self.wfile.write(output)
            print(output)
        except Exception as e:
            print('An error occurred: {}'.format(e))


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
