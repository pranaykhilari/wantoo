import json
from django.http import HttpResponse, HttpResponseRedirect

def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request:
                # a jsonp response!
                data = '%s(%s);' % (request['callback'], data)
                return HttpResponse(data, "text/javascript")
        except:
            data = json.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator    


# def company_required(orig_func):
#     def decorator(request, *args, **kwargs):
#         if request.user.is_authenticated() and request.user.user_detail.company is None:
#             return HttpResponseRedirect('/dashboard/company/new/')
#         else:
#             return orig_func(request, *args, **kwargs)
            
#     decorator.__name__ = orig_func.__name__
#     return decorator
