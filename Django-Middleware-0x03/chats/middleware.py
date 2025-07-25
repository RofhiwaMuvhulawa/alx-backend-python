import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from rest_framework.response import Response
from rest_framework import status

# Configure logging for RequestLoggingMiddleware
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler('requests.log'),
    ]
)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if not (10 <= current_hour < 14):  # Temporary for testing (10:00–14:00 UTC)
            return HttpResponseForbidden("Access is restricted outside of 6 PM to 9 PM.")
        response = self.get_response(request)
        return response

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/api/'):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required for this action.")
            if not (request.user.is_staff or request.user.is_superuser or request.user.role == 'moderator'):
                return HttpResponseForbidden("Only admins or moderators can perform this action.")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}  # In-memory store: {ip: [timestamps]}

    def __call__(self, request):
        if request.method == 'POST' and '/api/conversations/' in request.path and '/messages/' in request.path:
            ip_address = request.META.get('REMOTE_ADDR')
            now = datetime.now()
            if ip_address not in self.request_counts:
                self.request_counts[ip_address] = []
            self.request_counts[ip_address] = [
                timestamp for timestamp in self.request_counts[ip_address]
                if now - timestamp < timedelta(minutes=1)
            ]
            if len(self.request_counts[ip_address]) >= 5:
                return Response(
                    {"detail": "Rate limit exceeded: 5 messages per minute."},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
            self.request_counts[ip_address].append(now)
        response = self.get_response(request)
        return response
