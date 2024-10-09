from collections import defaultdict
from datetime import datetime, timedelta

from django.http import HttpRequest, HttpResponse



def set_useragent_on_request_middleware(get_response):
    print('Initial call')
    def middleware(request: HttpRequest):
        print('Before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('After get response')
        return response

    return middleware

class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('requsets count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('responses count', self.responses_count)
        return response
    
    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions so far')


class LimitRequests:
    def __init__(self, get_response):
        self.get_response = get_response
        self.time_between_requests = 0.0001
        self.requests_by_ips = defaultdict(self._get_default_time)
    
    def _get_default_time(self) -> datetime:
        return datetime.now() - timedelta(seconds=self.time_between_requests + 1)

    def __call__(self, request: HttpRequest):
        ip = request.META.get('REMOTE_ADDR')
        print('IP:', ip)
        now: datetime = datetime.now()
        if (now - self.requests_by_ips[ip]).total_seconds() > self.time_between_requests:
            self.requests_by_ips[ip] = now
            response = self.get_response(request)
            print('Request is success.')
            return response
        else:
            return HttpResponse('<b>Request is failed. Too little time between requests!</b>')

