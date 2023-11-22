from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    print("index tournament")
    return HttpResponse("Hello, world. You're at the trans index.")
