from django.shortcuts import render, redirect
from django.views import View
import requests
from django.conf import settings
from dotenv import load_dotenv
import os

class SignupPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html')

    def post(self, request, *args, **kwargs):

        load_dotenv()

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        delivery_location = request.POST.get('delivery_location')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # If latitude and longitude are empty, use Geocoding API to get them
        if not latitude or not longitude:
            google_maps_api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={delivery_location}&key={google_maps_api_key}"
            
            response = requests.get(geocode_url)
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    latitude = data['results'][0]['geometry']['location']['lat']
                    longitude = data['results'][0]['geometry']['location']['lng']
                else:
                    return render(request, 'signup.html', {
                        'error_message': 'Invalid address. Please try again.'
                    })
            else:
                return render(request, 'signup.html', {
                    'error_message': 'Unable to get location. Please try again later.'
                })

        # Send data to the Signup API endpoint
        api_url = request.build_absolute_uri('/api/user/signup/')
        payload = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'delivery_location': delivery_location,
            'latitude': latitude,
            'longitude': longitude
        }

        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 201:
                # Success - Redirect to the login page
                return redirect('login')
            else:
                # Error from API - Show error message
                error_message = response.json().get('error', 'Something went wrong.')
                return render(request, 'signup.html', {
                    'error_message': error_message
                })

        except requests.exceptions.RequestException:
            # Network error
            return render(request, 'signup.html', {
                'error_message': 'Network error. Please try again later.'
            })
