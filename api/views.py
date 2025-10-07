from django.shortcuts import render
from django.http import JsonResponse
import json
import time
from api import models

def homePage(request):
    solar, _ = models.Solar.objects.get_or_create(solarId=1)
    if solar.gridStatus == True:
        grid_text = "On grid"
        color = "#6dd07f"
        grid_output = "20"
        grid_animation = "flex"
    else:
        grid_text = "Off grid"
        color = "red"
        grid_output = "0"
        grid_animation = "none"

    if solar.load == 0:
        load_animation= "none"
    else:
        load_animation = "flex"
        
    return render(request, "project1/index.html", {
        'name': request.user,
        'load': solar.load,
        'grid_text': grid_text,
        'color': color,
        'grid_output': grid_output,
        'grid_animation': grid_animation,
        'load_animation': load_animation,
        'solar_value':solar.solarValue,
    })


def saveLoadValue(request):
        if request.method == "POST":
            data = json.loads(request.body)
            valoare = data.get("value")
            print("Valoarea slider-ului:", valoare)

            # Update instead of creating new each time
            obj, created = models.Solar.objects.get_or_create(solarId=1)
            obj.load = valoare
            obj.save()

            return JsonResponse({"value": valoare})


def loadUpdate(request):
    lastValue= models.Solar.objects.get(solarId = 1)
    while True:
        time.sleep(1)
        latestValue = models.Solar.objects.get(solarId = 1)
        if lastValue.load != latestValue.load:
            return JsonResponse({"value": latestValue.load})

def saveSolarValue(request):
    if request.method =="POST":
        obj = models.Solar.objects.get(solarId = 1)
        data = json.loads(request.body)
        valoare = data.get("solarValue")
        print("Valoarea slider-ului:", valoare)
        obj.solarValue = valoare
        obj.save()
        return JsonResponse({"solarValue": valoare})


def solarUpdate(request):
    lastValue = models.Solar.objects.get(solarId = 1)
    while True:
        time.sleep(1)
        latestValue= models.Solar.objects.get(solarId = 1)
        if latestValue.solarValue != lastValue.solarValue:
            return JsonResponse({"solar": latestValue.solarValue})


def saveGridValue(request):
    if request.method == "POST":
        obj = models.Solar.objects.get(solarId = 1)
        if obj.gridStatus == True:
            obj.gridStatus = False
            obj.save()
        else:
            obj.gridStatus = True
            obj.save()

        return JsonResponse({"status": "ok"})


def gridUpdate(request):
    lastValue= models.Solar.objects.get(solarId = 1)
    while True:
        time.sleep(1)
        latestValue = models.Solar.objects.get(solarId = 1)
        if lastValue.gridStatus != latestValue.gridStatus:
            return JsonResponse({"grid": latestValue.gridStatus})