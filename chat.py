from psidash.psidash import load_conf, load_dash, load_components
from psidash.psidash import get_callbacks, assign_callbacks
import flask

conf = load_conf('chat.yaml')

server = flask.Flask(__name__)

conf['app']['server'] = server

imports = conf.get('import')

app = load_dash(__name__, conf['app'], imports)

app.layout = load_components(conf['layout'], imports)

application = app.server

if 'callbacks' in conf:
    callbacks = get_callbacks(app, conf['callbacks'])
    assign_callbacks(callbacks, conf['callbacks'])

run_server_opts = conf['app.run_server']

if __name__ == '__main__':
    app.run_server(**run_server_opts)



