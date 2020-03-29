from application import create_app
from livereload import Server

if __name__ == '__main__':
    app = create_app()
    server = Server(app.wsgi_app)
    server.serve()