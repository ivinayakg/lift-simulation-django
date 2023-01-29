from rest_framework.decorators import api_view
from elevator.serializers import SessionSerializer, ElevatorRequestSerializer, ElevatorSerializer
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
        return JsonResponse({"message": "success created", "session": session_serialized.data})
    except Exception:
        pass
    try:
        data = {
            "total_elevators": request.data.get("elevators"),
            "total_floors": request.data.get("floors")
        }
        session_serialized = SessionSerializer(data=data).create()
        if not session_serialized:
            raise Exception("Invalid data")

        session_serialized_data = session_serialized.data

        for x in range(int(data["total_elevators"])):
            elevator_object = ElevatorSerializer(
                data={"session": session_serialized_data["id"]}).create()

        response = JsonResponse(
            {"message": "success created", "session": session_serialized_data})
        response.set_cookie(env("COOKIE_NAME"), session_serialized_data["id"],
                            expires=int(env("COOKIE_AGE")), httponly=True)
        return response
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})


@api_view()
def checkSession(request, cookie):
    try:
        session_id = cookie
        session = Session.objects.get(id=session_id)
        session_serialized = SessionSerializer(session)
        return JsonResponse({"message": "success", "session": session_serialized.data})
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
        session = Session.objects.get(id=session_id)
        if data["destination"] > session.total_floors or data["destination"] == 0:
            raise Exception(f'Floor range is 1-{session.total_floors}')
        elevator_request = ElevatorRequestSerializer(data=data).create()
        if not elevator_request:
            raise Exception("Invalid data")

        return JsonResponse({"message": "success", "elevator_request": elevator_request.data})
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})


@api_view()
def getAllElevatorRequests(request, cookie):
    try:
        query = request.query_params.dict()
        session_id = cookie
        session = Session.objects.get(id=session_id)
        elevator_request_all = session.get_all_elevators_requests(query=query)
        elevator_request_all_serialized = [
            ElevatorRequestSerializer(x).data for x in elevator_request_all]
        return JsonResponse({"message": "success", "elevator_requests": elevator_request_all_serialized})
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})


@api_view()
def getLatestElevatorRequest(request, cookie):
    try:
        query = {"completed": False}
        sort = ['-timestamp']
        session_id = cookie
        session = Session.objects.get(id=session_id)
        elevator_request_latest = session.get_all_elevators_requests(
            query=query, sort=sort)[0]
        elevator_request_latest_serialized = ElevatorRequestSerializer(
            elevator_request_latest).data
        return JsonResponse({"message": "success", "elevator_request": elevator_request_latest_serialized})
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})


@api_view()
def getElevatorData(request, cookie, id=None, key='all'):
    try:
        if not id:
            raise Exception("Pass valid elevator id")
        session_id = cookie
        session = Session.objects.get(id=session_id)
        elevator_query = {
            "id": id
        }
        elevator = session.get_all_elevators(query=elevator_query)[0]
        elevator_serialized_data = ElevatorSerializer(instance=elevator).data
        if key == "all":
            return JsonResponse({"message": "success", "elevator": elevator_serialized_data})
        else:
            return JsonResponse({"message": "success", f'elevator_{key}': elevator_serialized_data[key]})
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})


@api_view()
def getAllElevatorsData(request, cookie):
    try:
        query = request.query_params.dict()
        session_id = cookie
        session = Session.objects.get(id=session_id)
        elevator_query = {
            **query
        }
        elevator = session.get_all_elevators(query=elevator_query)
        elevator_serialized_data = [ElevatorSerializer(
            instance=x).data for x in elevator]
        return JsonResponse({"message": "success", "elevators": elevator_serialized_data})
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})


@api_view(["PATCH"])
def updateElevatorData(request, cookie, id):
    try:
        session_id = cookie
        session = Session.objects.get(id=session_id)
        elevator_query = {
            "id": id
        }
        elevator = session.get_all_elevators(query=elevator_query)[0]

        elevator_update_data = {
            "curr_floor": request.data.get('curr_floor'),
            "status": request.data.get('status'),
            "direction": request.data.get('direction'),
            "gates": request.data.get('gates'),
            "session": session_id
        }
        elevator_serialized = ElevatorSerializer(
            instance=elevator, data=elevator_update_data)
        elevator_serialized.update()
        return JsonResponse({"message": "success", "elevator": elevator_serialized.data})
    except Exception as e:
        return JsonResponse({"message": "Something Went Wrong", "error": e.args[0]})
