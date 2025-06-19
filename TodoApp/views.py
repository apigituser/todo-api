from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Item

@csrf_exempt
def create_paginate_handle(request):
    if request.method == "GET":
        return get_todo(request)
    elif request.method == "POST":
        return create_todo(request)
    else:
        return JsonResponse({"Bad Request": "Invalid HTTP Method"}, status=400)

@csrf_exempt
def update_delete_handle(request, id):
    if request.method == "PATCH":
        return update_todo(request, id)
    elif request.method == "DELETE":
        return delete_todo(request, id)
    else:
        return JsonResponse({"Bad Request": "Invalid HTTP Method"}, status=400)

@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def get_todo(request):
    page = int(request.GET.get("page") or 1)
    limit = request.GET.get("limit") or 2

    paginated_objects = Paginator(list(Item.objects.values()), limit)

    if page <= paginated_objects.num_pages:
        data = paginated_objects.get_page(page).object_list
        return JsonResponse({
            "data": data,
            "page": page,
            "limit": int(limit),
            "total": paginated_objects.count
        })
    return JsonResponse({"Bad Request": "Page does not exist"}, status=404)

@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def create_todo(request):
    title = request.POST.get("title")
    description = request.POST.get("description")

    if title and description:
        item = Item(title=title, description=description)
        item.save()
        return JsonResponse({
            "id": item.id,
            "title": item.title,
            "description": item.description
        })
    return JsonResponse({"Bad Request": "Title and Description required"}, status=400)

@api_view(['DELETE'])
@throttle_classes([UserRateThrottle])
def delete_todo(request, id):
    item = get_object_or_404(Item, id=id)
    item.delete()
    return JsonResponse({"OK": f"Item (id:{id}) deleted successfully"})

@api_view(['PATCH'])
@throttle_classes([UserRateThrottle])
def update_todo(request, id):
    item = get_object_or_404(Item, id=id)
    description = request.POST.get("description")
    
    if description:
        item.description = description
        item.save()
        return JsonResponse({
            "id": id,
            "title": item.title,
            "description": item.description
        })
    return JsonResponse({"Bad Request": "Item Description required"}, status=400)
    
@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
@permission_classes([])
def loginUser(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    if username and password:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token = Token.objects.get(user=user)
            return JsonResponse({'token': token.key})
        return JsonResponse({'Unauthorized': 'Invalid Credentials'}, status=401)
    return JsonResponse({'Bad Request': 'Username and Password required'}, status=400)

@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
@permission_classes([])
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')

    if username and password and email:
        if User.objects.filter(username=username).exists():
            return JsonResponse({'Conflict': 'Username already exists'}, status=409)
        user = User.objects.create_user(username, email, password)
        if user:
            token = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token[0].key})
    return JsonResponse({'Bad Request': 'Username Password and Email required'}, status=400)
