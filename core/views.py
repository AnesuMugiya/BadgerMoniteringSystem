from django.http import HttpResponse


def dashboard(request):
    return HttpResponse("Hello, world. You're at the core index.")