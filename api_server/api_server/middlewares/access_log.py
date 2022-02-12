import logging

logger = logging.getLogger(__name__)


class RequestDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # logger.info(f'Cookies: {request.COOKIES}')
        # logger.info(f'Headers: {request.headers}')
        # logger.info(f'META: {request.META}')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
