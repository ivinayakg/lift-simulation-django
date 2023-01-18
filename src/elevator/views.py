from rest_framework.decorators import api_view
from elevator.serializers import SessionSerializer
from elevator.models import Elevator, Session
from django.http import JsonResponse
from elevator.utils import env
from elevator.middleware import getCookie
# Create your views here.


@api_view(["POST"])
def createSession(request):
    try:
        data = {
            "total_elevators": request.data.get("elevators"),
            "total_floors": request.data.get("floors")
        }
        session = SessionSerializer(data=data).create()
        session.save()
        response = JsonResponse({"message": "Hello world"})
        response.set_cookie(env("COOKIE_NAME"), session.id,
                            expires=int(env("COOKIE_AGE")), httponly=True)
        return response
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})


@api_view()
def checkSession(request):
    try:
        session_id = getCookie(request)
        session = Session.objects.get(id=session_id)
        session = SessionSerializer(session)
        return JsonResponse({"message": "success", "session": {"id": session_id, **session.data}})
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})
