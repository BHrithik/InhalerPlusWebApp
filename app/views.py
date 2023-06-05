# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .models import *
import requests
import pyrebase
from geopy.geocoders import Nominatim
import geocoder


def getLocation():
    geolocator = Nominatim(user_agent="InhalerPlus")
    g = geocoder.ip('me')
    # print(g.latlng)
    location = geolocator.reverse(str(g.latlng[0])+" "+str(g.latlng[1]))
    return location.address

uri = "https://inhalerplus-f6754-default-rtdb.firebaseio.com/findme.json"

def loadData():
    firebaseConfig = {
        'apiKey': "AIzaSyDZXYGYPbF4NKviCsvu8eRdBE3BwYDku0A",
        'authDomain': "inhalerplus-f6754.firebaseapp.com",
        'databaseURL': "https://inhalerplus-f6754-default-rtdb.firebaseio.com",
        'projectId': "inhalerplus-f6754",
        'storageBucket': "inhalerplus-f6754.appspot.com",
        'messagingSenderId': "149422619781",
        'appId': "1:149422619781:web:6658e43fd0db0fbb887dec",
        'measurementId': "G-SLN9YNX1BK"
    }
    app = pyrebase.initialize_app(firebaseConfig);
    db = app.database()
    dblist = list(db.child('records').get().val().values())
    records = Reccords.objects.all()
    for i in dblist:
        newrecFlag = True
        for j in records:
            if i['time'] == j.time: 
                newrecFlag = False
        if newrecFlag:
            newrec = Reccords(time=i['time'],user=i['user'],location=getLocation(),count = i['count'])
            newrec.save()
            records = Reccords.objects.all()

@login_required(login_url="/login/")
def index(request):
    loadData()
    records = Reccords.objects.all()
    context = {'segment': 'index', 'records':records}
    html_template = loader.get_template('dashboard.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def findme(request):
    loadData()
    records = Reccords.objects.all()
    context = {'segment': 'index', 'records':records}
    response = requests.put(uri, data ="1")
    print(response)
    html_template = loader.get_template('findMeDashboard.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
