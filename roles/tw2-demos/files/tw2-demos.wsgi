import sys
sys.stdout = sys.stderr

activate_this = '/var/lib/tw2-demos-venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import logging
logging.basicConfig()

import tw2.core
import tw2.devtools
import tw2.devtools.browser
application = tw2.core.make_middleware(None, controller_prefix='/')
