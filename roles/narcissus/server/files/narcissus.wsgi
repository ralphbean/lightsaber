#-*- coding: UTF-8 -*-

import logging, sys, os
logging.basicConfig(stream=sys.stderr)

from moksha.wsgi.middleware import make_moksha_middleware
from moksha.common.lib.helpers import get_moksha_appconfig

from tw2.core.middleware import make_middleware

from narcissus.app.routes import app as application
from narcissus.app.routes import load_production_config

production_filename = "/etc/narcissus.ini"
if os.path.exists(production_filename):
    config = load_production_config(production_filename)
else:
    # Load development.ini
    config = get_moksha_appconfig()

# Wrap the inner wsgi app with our middlewares
application.wsgi_app = make_moksha_middleware(application.wsgi_app, config)
application.wsgi_app = make_middleware(application.wsgi_app)
