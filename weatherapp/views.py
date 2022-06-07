from django.shortcuts import get_object_or_404, redirect, render
from decouple import config
import requests
from pprint import pprint
from .models import City
from django.contrib import messages


def home(request):
    API_key=config('API_KEY')
    u_city = request.GET.get('u_city')
    
    if u_city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={u_city}&appid={API_key}&units=metric"
        r = requests.get(url)
        pprint(r.ok)
        if r.ok:
            content = r.json()
            r_city = content.get('name')
            if City.objects.filter(name=r_city):
                messages.warning(request, message='The city exists!')
            else:
                City.objects.create(name=r_city)
                messages.success(request, message='City created!')
        else:
            messages.error(request, message='City can not found!')
        return redirect('home')
    
    city_data = []
    cities = City.objects.all()
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric"
        r = requests.get(url)
        content = r.json()
        data = {
            'city': city,
            'temp': content['main']['temp'],
            'desc': content['weather'][0]['description'],
            'icon': content['weather'][0]['icon'],
        }
        city_data.append(data)
    context = {
        'city_data': city_data,
    }
    return render(request, "weatherapp/home.html", context)

def delete(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    messages.success(request, message='City deleted!')
    return redirect('home')