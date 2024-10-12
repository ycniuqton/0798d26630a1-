# myapp/middleware.py

from django.http import HttpResponseRedirect
from core.authentication import RedirectToLoginException


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except RedirectToLoginException as e:
            return e.args[0]  # This is the HttpResponseRedirect

        return response


import logging
import uuid

# Create a logger instance
logger = logging.getLogger(__name__)


class ContextIDMiddleware:
    """
    Middleware that generates a unique CONTEXT_ID for each request
    and attaches it to the logging context to ensure that all logs
    for a single request share the same CONTEXT_ID.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # BEFORE request processing: generate CONTEXT_ID and log it
        context_id = str(uuid.uuid4())
        request.context_id = context_id  # Attach to the request

        # Add CONTEXT_ID to logging context
        logger = logging.getLogger('django.server')
        logging_context = {'CONTEXT_ID': context_id}
        old_factory = logger.manager.loggerDict['django.server'].makeRecord

        def record_factory(*args, **kwargs):
            record = old_factory(*args, **kwargs)
            for key, value in logging_context.items():
                setattr(record, key, value)
            return record

        logger.manager.loggerDict['django.server'].makeRecord = record_factory

        logger.info(request.body)
        # Call the next middleware or view
        try:
            response = self.get_response(request)
        except Exception as e:
            # Log exception details
            logger.error(f"Request {request.context_id} failed with exception: {e}")
            raise

        # AFTER request processing (after the view is called): process the response
        return self.process_response(request, response)

    def process_response(self, request, response):
        # AFTER response is processed: log response-related details
        return response
