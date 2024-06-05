import os

class InstanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.instance_number = os.getenv('INSTANCE', 'unknown')

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Instance-Number'] = self.instance_number
        return response