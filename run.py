from application import create_app
from livereload import Server

if __name__ == '__main__':
    app = create_app()
    app.debug = True
    server = Server(app.wsgi_app)
    server.serve()