from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Item

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_todo(request):
    title = request.POST.get("title")
    description = request.POST.get("description")

    if title and description:
        item = Item(title=title, description=description)
        item.save()
        return JsonResponse(
            {
                "id": item.id,
                "title": item.title,
                "description": item.description
            }
        )
    return JsonResponse({'err': 'err'})
    
@csrf_exempt
@api_view(['POST'])
def loginUser(request):
    if request.user.is_authenticated:
        return JsonResponse({'stop it': 'you\'re already logged in'})

    username = request.POST.get('username')
    password = request.POST.get('password')
    
    if username and password:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token = Token.objects.get(user=user)
            return JsonResponse({'token': token.key})
        return JsonResponse({'401': 'invalid credentials'})
    return JsonResponse({'you idiot': 'provide a username and password'})

@csrf_exempt
@api_view(['POST'])
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    

    if username and password and email:
        if User.objects.filter(username=username).exists():
            return JsonResponse({'too bad': 'user already exists'})
        user = User.objects.create_user(username, email, password)
        if user:
            token = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token[0].key})
    return JsonResponse({'not enough arguments': 'provide username password email'})
