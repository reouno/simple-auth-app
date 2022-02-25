"""Access log middleware"""
import logging

from django.http import HttpRequest

logger = logging.getLogger(__name__)


class RequestDebugMiddleware:
    """Debug log of access"""
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # logger.info(f'Request path: {request.path}, Method: {request.method}')
        # logger.info(f'Cookies: {request.COOKIES}\n')
        # logger.info(f'Headers: {request.headers}\n')
        # logger.info(f'META: {request.META} \n')
        # logger.info(f'Body: {request.body.decode("utf-8")}')
        # logger.info(f'properties: {dir(request)} \n')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
