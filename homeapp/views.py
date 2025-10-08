from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello ICC — Django 5 OK")
