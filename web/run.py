import sys
sys.path.extend(['/root/ljquant'])

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from web.hsi_intraday_app import app as hsi
from web.app import app as flask_app
from werkzeug.serving import run_simple

application = DispatcherMiddleware(flask_app, {
    '/hsiIntraday': hsi.server,
})

