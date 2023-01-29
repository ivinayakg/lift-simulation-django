from rest_framework.test import APITestCase, APIRequestFactory
from http.cookies import SimpleCookie
from json import dumps as JSONStringify, loads as JSONParse

from elevator.views import createSession, checkSession, createElevatorRequest, getAllElevatorRequests, getLatestElevatorRequest, getElevatorData, getAllElevatorsData, updateElevatorData
from elevator.utils import env
from elevator.models import Session, ElevatorRequest, Elevator
from elevator.serializers import ElevatorSerializer
from elevator.middleware import middlewareWrapper, getCookieMiddleware
from random import randint


def CleanDatabase():
    Session.objects.all().delete()


class ElevatorAppTests(APITestCase):
    session_request_data = {"elevators": 5, "floors": 8}
    factory = APIRequestFactory()
    factory.cookies = SimpleCookie()
    initial_elevators_requests = 4

    @classmethod
    def setUpClass(cls):
        CleanDatabase()

        session_request = cls.factory.post(
            'api/initiate', format='json', data=cls.session_request_data)
        session_response = createSession(session_request)
        cls.session = JSONParse(session_response.content)['session']

        cls.elevators = [ElevatorSerializer(
            x).data for x in Elevator.objects.filter(session=cls.session['id'])]

        cls.factory.cookies[env("COOKIE_NAME")] = cls.session["id"]
        cls.elevator_requests = []
        for x in range(cls.initial_elevators_requests):
            random_elevator = randint(1, len(cls.elevators) - 1)
            elevator_request_data = {"destination": cls.get_random_floor(
                cls), "elevator": cls.elevators[random_elevator]['id']}
            _request = cls.factory.post(
                'api/request', format='json', data=elevator_request_data)
            _response = middlewareWrapper(
                getCookieMiddleware, view=createElevatorRequest)(_request)
            _response_data = JSONParse(_response.content)
            cls.elevator_requests.append(_response_data['elevator_request'])

        return super(ElevatorAppTests, cls).setUpClass()

    @classmethod
    def setUp(self):
        self.factory.cookies = SimpleCookie()

    def get_random_floor(self):
        return randint(1, self.session_request_data['floors'])


class CreateSessionTest(ElevatorAppTests):
    def test_create_session_without_data(self):
        _request = self.factory.post('api/initiate', format='json')
        _response = createSession(_request)
        self.assertJSONEqual(
            _response.content, {"message": "Something Went Wrong", "error": "Invalid data"})

    def test_create_session_with_data(self):
        request_data = {
            "elevators": 10,
            "floors": 15
        }
        _request = self.factory.post(
            'api/initiate', data=request_data, format='json')
        _response = createSession(_request)
        _response_data = JSONParse(_response.content)
        self.assertTrue(len(_response_data["session"]["id"]) != 0)
        self.assertEqual(
            _response_data["session"]["total_elevators"], request_data["elevators"])
        self.assertEqual(_response_data["session"]
                         ["total_floors"], request_data["floors"])

    def test_create_session_with_cookie(self):
        self.factory.cookies[env("COOKIE_NAME")] = self.session['id']
        request_data = {"elevators": 10, "floors": 15}
        _request = self.factory.post(
            'api/initiate', data=request_data, format='json')

        _response = createSession(_request)
        _response_data = JSONParse(_response.content)

        self.assertEqual(_response_data["session"]["id"], self.session['id'])
        self.assertEqual(
            _response_data["session"]["total_elevators"], self.session['total_elevators'])
        self.assertEqual(
            _response_data["session"]["total_floors"], self.session['total_floors'])


class CheckSessionTest(ElevatorAppTests):
    def test_check_session_without_cookie(self):
        _request = self.factory.get('api',  format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=checkSession)(_request)
        self.assertJSONEqual(
            _response.content, {"message": "Something Went Wrong", "error": "Cookie invalid or doesn't exists"})

    def test_check_session_with_cookie(self):
        self.factory.cookies[env("COOKIE_NAME")] = self.session['id']
        _request = self.factory.get('api',  format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=checkSession)(_request)
        _response_data = JSONParse(_response.content)
        self.assertEqual(_response_data["session"]["id"], self.session['id'])
        self.assertEqual(
            _response_data["session"]["total_elevators"], self.session['total_elevators'])
        self.assertEqual(
            _response_data["session"]["total_floors"], self.session['total_floors'])