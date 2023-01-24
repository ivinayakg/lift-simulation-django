from rest_framework.decorators import api_view
from elevator.serializers import SessionSerializer, ElevatorRequestSerializer
from elevator.models import Elevator, Session
from django.http import JsonResponse
from elevator.utils import env
# Create your views here.


@api_view(["POST"])
def createSession(request):
    try:
        session_id = request.COOKIES[env("COOKIE_NAME")]
        session = Session.objects.get(id=session_id)
        session_serialized = SessionSerializer(session)
        return JsonResponse({"message": "success created", "session": {"id": session_id, **session_serialized.data}})
    except Exception:
        pass
    try:
        data = {
            "total_elevators": request.data.get("elevators"),
            "total_floors": request.data.get("floors")
        }
        session = SessionSerializer(data=data).create()
        if not session:
            raise Exception("Invalid data")

        [Elevator(session=session['instance']).save()
         for x in range(int(data["total_elevators"]))]

        response = JsonResponse(
            {"message": "success created", "session": session['data']})
        response.set_cookie(env("COOKIE_NAME"), session['instance'].id,
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


@api_view(["POST"])
def createElevatorRequest(request, cookie):
    try:
        session_id = cookie
        data = {
            "destination": request.data.get('destination'),
            "elevator": request.data.get('elevator'),
            "session": session_id
        }
        elevator_request = ElevatorRequestSerializer(
            data=data).create()
        if not elevator_request:
            raise Exception("Invalid data")

        return JsonResponse({"message": "success", "elevator_request": elevator_request['data']})
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})


@api_view()
def getAllElevatorRequest(request, cookie):
    try:
        query = request.query_params.dict()
        session_id = cookie
        session = Session.objects.get(id=session_id)
        elevator_request_all = session.get_all_lifts_requests(query=query)
        elevator_request_all_serialized = [
            ElevatorRequestSerializer(x).data for x in elevator_request_all]
        return JsonResponse({"message": "success", "elevator_requests": elevator_request_all_serialized})
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})


@api_view()
def getLatestElevatorRequests(request, cookie):
    try:
        query = {"completed": "false"}
        sort = ['-timestamp']
        session_id = cookie
        session = Session.objects.get(id=session_id)
        elevator_request_latest = session.get_all_lifts_requests(
            query=query, sort=sort)[0]
        elevator_request_latest_serialized = ElevatorRequestSerializer(
            elevator_request_latest).data
        return JsonResponse({"message": "success", "elevator_request": elevator_request_latest_serialized})
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})
