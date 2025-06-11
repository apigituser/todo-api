from django.contrib.auth.models import User
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def register(request: HttpRequest):
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
