from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.validators import URLValidator # for validating URLs
from django.core.exceptions import ValidationError

import json
import string
import random
from shortener.models import GShortURL, ShortURL


# Guest Index
def Gindex(request):
    return render(request, 'Gindex.html' )

characters = string.ascii_letters + string.digits

# if user is logged in , redirect to dashboard , otherwise render home page
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Replace 'dashboard' with your actual dashboard URL name
    return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')

def login_page(request):
    return render(request, 'login.html')

@never_cache # ensure this page is never cached (stored in browser) but accessed from server
@login_required(login_url='/login/') # if user is not logged in, redirect to login page
def main(request):
    return render(request, 'main.html')

## after succesfully logging in or signing up, the user will be redirected to this page
@never_cache # ensure this page is never cached (stored in browser) but accessed from server
@login_required(login_url='/login/') # if user is not logged in, redirect to login page
def dashboard(request):              # otherwise, execute this function
    # fetching data of the logged in user
    user_info= ShortURL.objects.filter(user=request.user) 
    data=[]
    for i in user_info:
        data.append([i.shortcode, i.original_url, i.created_at, i.click_count])

    return render(request, 'dashboard.html', {'user': request.user, 'data': data})


@csrf_exempt  
def logout_user(request):
    if request.method == 'POST':
        logout(request)  # This clears the session
        return JsonResponse({'message': 'Logged out successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)


# FOR authencating user that are logging in
def  auth_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(username=username, password=password)
            user.save()
            print(f"User {username} created successfully.")
            # Automatically log in the user after registration
            login(request, user)
            return JsonResponse({"message": "User created successfully"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)

# Shortening URLs for guests
@csrf_exempt
def Gshorten(request):
    if request.method == "POST":
        data = json.loads(request.body)
        long_url = data.get('original_url')
        print(long_url)
         # Validate URL
        url_validator = URLValidator()
        try:

            url_validator(long_url)
        except ValidationError:
            # If the URL is invalid, return an error response
          return JsonResponse({'error': 'Invalid URL'}, status=400)
        newshortcode=""

        while True:
            # Generate a random shortcode
            shortcode = ''.join(random.choices(characters, k=6))
            # Check if the shortcode is unique (you would typically check against your database here)
            if not GShortURL.objects.filter(shortcode=shortcode).exists():
                newshortcode = shortcode
                # adding to the data
            
                obj=GShortURL.objects.create(shortcode=newshortcode, original_url=long_url)
                obj.save()
                print(obj)
                break

        short_url = "http://127.0.0.1:8000/" + newshortcode
        return JsonResponse({'short_url': short_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def shorten(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            long_url = data.get('original_url')

            # Validate URL
            url_validator = URLValidator()
            try:
               url_validator(long_url)
            except ValidationError:
            # If the URL is invalid, return an error response
               return JsonResponse({'error': 'Invalid URL'}, status=400)
            
            # Generate a unique 7-character shortcode
            while True:
                shortcode = ''.join(random.choices(characters, k=7))
                if not ShortURL.objects.filter(shortcode=shortcode).exists():
                    break

            # Create and save the ShortURL object
            obj = ShortURL.objects.create(
                user=request.user,
                shortcode=shortcode,
                original_url=long_url
            )
            
            obj.save()

            print(f"Short URL created: {obj.shortcode} → {obj.original_url}")
            short_url = f"http://127.0.0.1:8000/{shortcode}"  # Replace with your domain in production
            return JsonResponse({'short_url': short_url})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



@login_required
def delete_link(request, shortcode):
    if request.method == 'DELETE':
        try:
            # Check if the shortcode exists in ShortURL
            link = ShortURL.objects.get(shortcode=shortcode)
            link.delete()
            print("LINK DELETED")
            return JsonResponse({'message': 'Link deleted successfully'})
        except ShortURL.DoesNotExist:
            return JsonResponse({'error': 'Link not found'}, status=404)


# redirect to original for guest AND registered users
def rd(request, shortcode):
    try:
        if len(shortcode) == 6:
           link = GShortURL.objects.get(shortcode=shortcode)
           return redirect(link.original_url)
        
        # elif len(shortcode) == 7:
        else :
           link = ShortURL.objects.get(shortcode=shortcode)
           link.click_count += 1  # Increment click count
           link.save()  # Save the updated click count
           return redirect(link.original_url)
        
        
    except (GShortURL.DoesNotExist, ShortURL.DoesNotExist):
        # If the shortcode does not exist, return a 404 error
        return render(request, '404.html', status=404)  

    #     return JsonResponse({"error": "Short URL not found."}, status=404)