# Standard libary imports
# Third-party imports
# Django imports
from django.shortcuts import render
# Local imports


def handler404(request, exception):
    """ Error Handler 404 - Page Not Found """
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """ Error Handler 500 - Interal Server Error """
    return render(request, "errors/500.html", status=500)


def handler403(request, exception):
    """ Error Handler 404 - Permissions denied """
    return render(request, "errors/403.html", status=403)
