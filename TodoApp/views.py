from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .models import Item

@csrf_exempt
@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def update_and_delete_todo(request, id):
    item_exists = Item.objects.filter(id=id).exists()
    if item_exists:
        item = Item.objects.get(id=id)

        if request.method == "PATCH":
            description = request.POST.get("description")
            item.description = description
            item.save()
            return JsonResponse(
                {
                    "id": id,
                    "title": item.title,
                    "description": item.description
                }
            )
        elif request.method == "DELETE":
            item.delete()
            return JsonResponse({'204': 'item deleted'})
    return JsonResponse({"invalid id": "item doesn't exist"})

@csrf_exempt
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_paginate_todo(request):
    if request.method == 'POST':
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
    elif request.method == 'GET':
        page = request.GET.get("page")
        paginated_objects = Paginator(list(Item.objects.values()), 2)

        if page:
            page = int(page)
            if page <= paginated_objects.num_pages:
                data = paginated_objects.get_page(page).object_list
                return JsonResponse({
                    "data": data,
                    "page": page,
                    "total": 2
                })
            return JsonResponse({'404': 'page range not valid'})
        return JsonResponse({'bozo': 'no page parameter provided'})
    
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
