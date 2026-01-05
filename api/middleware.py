# api/middleware.py
import logging, traceback, sys
logger = logging.getLogger("exception_logger")

class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as e:
            tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
            logger.error("UNCAUGHT EXCEPTION:\n%s", tb)
            print("UNCAUGHT EXCEPTION:\n", tb, file=sys.stderr)
            raise