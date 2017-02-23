# CMSC 122 Winter 2017 Arif-Chuang-Hori-Teehan
# UChicago Yelp Recommender Project
#
#

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")