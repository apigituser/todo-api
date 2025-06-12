from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def loginUser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    if username and password:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': f'{username} logged in'})
        return JsonResponse({'401': 'invalid credentials'})
    return JsonResponse({'you idiot': 'provide a username and password'})

@csrf_exempt
def logoutUser(request):
    if request.user.is_authenticated:
        authenticated_user = str(request.user)
        logout(request)
        return JsonResponse({'200': f'{authenticated_user} logged out'})
    return JsonResponse({'bish': 'you\'re anonymous'})

@csrf_exempt
def register(request):
    body = request.body
    user = None
    try:
        payload = json.loads(body)
        user = User.objects.create_user(
            payload['username'],
            payload['email'],
            payload['password']
        )
    except json.JSONDecodeError:
        payload = "Invalid Json"
    except Exception:
        payload = "Internal Error"
    if user:
        return JsonResponse({'success': 'User created'})
    return JsonResponse({'error': 'Failed to create user'})
