from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
import time
from api import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as login_auth,logout as auth_logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, logout

@login_required(login_url='/login/')
def homePage(request):
    solar, _ = models.Solar.objects.get_or_create(user= request.user)
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
    if solar.solarValue == 0:
        solar_animation = "none"
    else:
        solar_animation = "flex"
    if solar.batteryValue > 0:
        battery_charge = "flex"
        battery_discharge = "none"
    elif solar.batteryValue < 0:
        battery_charge = "none"
        battery_discharge = "flex"
    else:
        battery_charge = "none"
        battery_discharge = "none"

    return render(request, "project1/index.html", {
        'name': request.user,
        'load': solar.load,
        'grid_text': grid_text,
        'color': color,
        'grid_output': grid_output,
        'grid_animation': grid_animation,
        'load_animation': load_animation,
        'solar_value':solar.solarValue,
        'solar_animation':solar_animation,
        'solar_slider': solar.solarValue,
        'battery_value': solar.batteryValue,
        'battery_charge': battery_charge,
        'battery_discharge': battery_discharge,
        'house_invertor': solar.invertorCapacity,
        'solar_power': solar.instaledSolarPower,
        'battery_capacity': solar.batteryCapacity
    })


def saveLoadValue(request):
        if request.method == "POST":
            data = json.loads(request.body)
            valoare = data.get("value")

            obj, created = models.Solar.objects.get_or_create(user= request.user)
            obj.load = valoare
            obj.save()

            return JsonResponse({"value": valoare})


def loadUpdate(request):
    latest_value = models.Solar.objects.get(user=request.user)
    return JsonResponse({"value": latest_value.load})

def saveSolarValue(request):
    if request.method =="POST":
        obj = models.Solar.objects.get(user= request.user)
        data = json.loads(request.body)
        valoare = data.get("solarValue")
        obj.solarValue = valoare
        obj.save()
        return JsonResponse({"solarValue": valoare})


def solarUpdate(request):
    latestValue= models.Solar.objects.get(user= request.user)
    return JsonResponse({"solar": latestValue.solarValue})


def saveGridValue(request):
    if request.method == "POST":
        obj = models.Solar.objects.get(user= request.user)
        if obj.gridStatus == True:
            obj.gridStatus = False
            obj.save()
        else:
            obj.gridStatus = True
            obj.save()

        return JsonResponse({"status": "ok"})


def gridUpdate(request):
    latestValue = models.Solar.objects.get(user= request.user)
    return JsonResponse({"grid": latestValue.gridStatus})
        

def calculateSolarOutput(request):
    obj = models.Solar.objects.get(user= request.user)
    batteryChargeValue = obj.solarValue - obj.load
    obj.batteryValue = batteryChargeValue
    obj.save()
    return JsonResponse({"bateryChargeValue": batteryChargeValue})


def registerPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        all_usernames = User.objects.values_list('username', flat=True)
        
        if username in all_usernames:
            return render(request, "project1/register.html",{"error":"!"})
        else:
            user = User.objects.create_user(username,"user@mail.com",password)
            user.save()
            login(request,user)
            invertorCapacity = request.POST.get("invertor")
            solarInstaledPower = request.POST.get("solar")
            batteryCapacity = request.POST.get("battery")

            obj, created = models.Solar.objects.get_or_create(user=request.user)
            obj.invertorCapacity = invertorCapacity
            obj.instaledSolarPower = solarInstaledPower
            obj.batteryCapacity = batteryCapacity
            obj.save()

            return redirect('/solar/')
        
    return render(request, "project1/register.html")


def loginPage(request):
    if request.method =="POST":
        usena = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request,username= usena, password=pwd)
        if user is not None:
            login(request, user)
            return redirect("/solar/")
        else:
            return render(request, "project1/login.html",{"error":"!"})
           
    return render(request,"project1/login.html")


def logoutUser(request):
    logout(request)
    return redirect('/login/') 


def registerProduct(request):
    invertorCapacity = request.POST.get("invertor")
    solarInstaledPower = request.POST.get("solar")
    batteryCapacity = request.POST.get("battery")

    obj, created = models.Solar.objects.get_or_create(user=request.user)
    obj.invertorCapacity = invertorCapacity
    obj.instaledSolarPower = solarInstaledPower
    obj.batteryCapacity = batteryCapacity
    obj.save()

    return redirect('/solar/')
