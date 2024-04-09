from django.conf import settings


class RemovePoweredByMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
       
        if request.path.endswith('.css'):
            # Set the Content-Type header to "text/css" for CSS files
             response['Content-Type'] = 'text/css'
    
        response['Server'] = settings.X_POWERED_BY_HEADER
        
        return response