import os
import sys
import traceback
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

# create the real Django WSGI app once
_django_app = get_wsgi_application()

def application(environ, start_response):
    try:
        path = environ.get("PATH_INFO", "")
        if path == "/api/ping":
            start_response("200 OK", [("Content-Type", "text/plain")])
            return [b"pong"]
        # otherwise delegate to Django
        return _django_app(environ, start_response)
    except Exception:
        # log full traceback to stderr so Render/Gunicorn captures it
        tb = traceback.format_exc()
        print("WSGI EXCEPTION:\n", tb, file=sys.stderr)
        start_response("500 Internal Server Error", [("Content-Type", "text/plain")])
        return [b"internal error"]