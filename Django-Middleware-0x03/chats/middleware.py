# chats/middleware.py
import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.http import JsonResponse

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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_logs = {}  # {ip: [(timestamp1), (timestamp2), ...]}

    def __call__(self, request):
        if request.method == 'POST' and '/messages/' in request.path:
            ip = self.get_client_ip(request)
            now = time.time()
            window = 60  # 1 minute
            limit = 5    # max 5 messages per minute

            # Initialize or clean up logs
            if ip not in self.message_logs:
                self.message_logs[ip] = []
            self.message_logs[ip] = [t for t in self.message_logs[ip] if now - t < window]

            if len(self.message_logs[ip]) >= limit:
                return JsonResponse({
                    'error': 'Rate limit exceeded. You can only send 5 messages per minute.'
                }, status=429)

            self.message_logs[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Handle proxied requests
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    

    # Django-Middleware-0x03/chats/middleware.py
from django.http import JsonResponse

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            allowed_roles = ['admin', 'moderator']
            user_role = getattr(user, 'role', None)

            if user_role not in allowed_roles:
                return JsonResponse(
                    {'error': 'Access denied: You must be an admin or moderator to perform this action.'},
                    status=403
                )
        else:
            # Optionally handle anonymous users here if needed, e.g., block or allow
            pass

        response = self.get_response(request)
        return response
