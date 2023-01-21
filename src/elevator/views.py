from rest_framework.decorators import api_view
from elevator.serializers import SessionSerializer
from elevator.models import Elevator, Session
from django.http import JsonResponse
from elevator.utils import env
# Create your views here.


@api_view(["POST"])
def createSession(request):
    try:
        session_id = request.COOKIES[env("COOKIE_NAME")]
        session = Session.objects.get(id=session_id)
        session = SessionSerializer(session)
        return JsonResponse({"message": "success created", "session": {"id": session_id, **session.data}})
    except Exception:
        pass
    try:
        data = {
            "total_elevators": request.data.get("elevators"),
            "total_floors": request.data.get("floors")
        }
        sessionSerilized = SessionSerializer(data=data)
        session = sessionSerilized.create()
        if not session:
            raise Exception("Invalid data")

        session.save()
        [Elevator(session=session).save()
         for x in range(int(data["total_elevators"]))]

        response = JsonResponse({"message": "success created", "session": {
                                "id": session.id, **sessionSerilized.data}})
        response.set_cookie(env("COOKIE_NAME"), session.id,
                            expires=int(env("COOKIE_AGE")), httponly=True)
        return response
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})


@api_view()
def checkSession(request, cookie):
    try:
        session_id = cookie
        session = Session.objects.get(id=session_id)
        session = SessionSerializer(session)
        return JsonResponse({"message": "success", "session": {"id": session_id, **session.data}})
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})
