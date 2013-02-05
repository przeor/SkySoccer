from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPFound


def not_found(request):
    msg = "Keep looking on site!"
    return HTTPNotFound(msg)


def redirect_page(request):
    return HTTPFound(location="/")
