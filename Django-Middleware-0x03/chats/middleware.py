# chats/middleware.py
import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden

# Configure logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        response = self.get_response(request)
        return response



class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Current server time
        current_time = datetime.now().time()

        # Access window: from 6 PM (18:00) to 9 PM (21:00)
        start_time = time(18, 0)  # 6 PM
        end_time = time(21, 0)    # 9 PM

        # Allow access only within the time window
        if not (start_time <= current_time <= end_time):
            return HttpResponseForbidden(
                "⛔ Access to chats is only allowed between 6 PM and 9 PM."
            )

        # Continue processing request
        return self.get_response(request)
