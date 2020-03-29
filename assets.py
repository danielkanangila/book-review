from flask_assets import Environment, Bundle


def setup_assets(app):
    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle('scss/main.scss', filters='pyscss', output='css/main.css')
    assets.register('scss', scss)