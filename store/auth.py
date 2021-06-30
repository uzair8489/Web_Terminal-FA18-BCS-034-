from django.shortcuts import redirect

def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # returnUrl = request.META['PATH_INFO']
        # print(request.META['PATH_INFO'])
        if not request.session.get('user'):
            return redirect('login')
            
        # print('middleware')
        response = get_response(request)
        return response

    return middleware