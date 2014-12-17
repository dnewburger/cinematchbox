from flask import Flask
app = Flask(__name__, instance_relative_config=True)
#app.config.from_object(__name__)
app.config.from_pyfile('default_settings.cfg', silent=True)

import cinematchbox.views
