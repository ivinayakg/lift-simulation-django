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


class CreateElevatorRequestTest(ElevatorAppTests):
    def setUp(self):
        self.factory.cookies[env("COOKIE_NAME")] = self.session["id"]

    def test_create_elevator_request_with_data(self):
        elevator_request_data = {
            "destination": self.get_random_floor(), "elevator": self.elevators[1]['id']}
        _request = self.factory.post(
            'api/request', format='json', data=elevator_request_data)
        _response = middlewareWrapper(
            getCookieMiddleware, view=createElevatorRequest)(_request)
        _response_data = JSONParse(_response.content)
        self.assertTrue(_response_data["elevator_request"]['id'])
        self.assertEqual(
            _response_data["elevator_request"]['session'], self.session['id'])
        self.assertEqual(_response_data["elevator_request"]
                         ['destination'], elevator_request_data['destination'])
        self.assertEqual(
            _response_data["elevator_request"]['elevator'], elevator_request_data['elevator'])

    def test_create_elevator_request_with_invalid_data(self):
        elevator_request_data = {
            "destination": self.get_random_floor(),
            "elevator": 15
        }
        _request = self.factory.post(
            'api/request', format='json', data=elevator_request_data)
        _response = middlewareWrapper(
            getCookieMiddleware, view=createElevatorRequest)(_request)
        _response_data = JSONParse(_response.content)
        self.assertEqual(_response_data["error"], 'Invalid data')
        self.assertEqual(_response_data["message"], 'Something Went Wrong')

    def test_create_elevator_request_with_invalid_destination_data(self):
        elevator_request_data = {
            "destination": 50,
            "elevator": self.elevators[1]['id']
        }
        _request = self.factory.post(
            'api/request', format='json', data=elevator_request_data)
        _response = middlewareWrapper(
            getCookieMiddleware, view=createElevatorRequest)(_request)
        _response_data = JSONParse(_response.content)
        self.assertEqual(
            _response_data["error"], f'Floor range is 1-{self.session["total_floors"]}')
        self.assertEqual(_response_data["message"], 'Something Went Wrong')


class GetAllElevatorRequestsTest(ElevatorAppTests):
    def setUp(self):
        self.factory.cookies[env("COOKIE_NAME")] = self.session["id"]

    def test_get_all_elevator_request(self):
        _request = self.factory.get('api/request/all', format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=getAllElevatorRequests)(_request)
        _response_data = JSONParse(_response.content)
        self.assertEqual(_response_data["message"], "success")
        self.assertTrue(
            len(_response_data["elevator_requests"]), len(self.elevator_requests))

    def test_get_all_elevator_request_with_query(self):
        destination = self.elevator_requests[2]['destination']
        _request = self.factory.get(
            'api/request/all', {"destination": destination, "completed": False}, format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=getAllElevatorRequests)(_request)
        _response_data = JSONParse(_response.content)
        self.assertEqual(_response_data["message"], "success")
        self.assertTrue(len(_response_data["elevator_requests"]) > 0)
        for request in _response_data["elevator_requests"]:
            self.assertEqual(request['destination'], destination)

    def test_get_all_elevator_request_with_query_no_results(self):
        _request = self.factory.get(
            'api/request/all', {"destination": 3, "completed": True}, format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=getAllElevatorRequests)(_request)
        _response_data = JSONParse(_response.content)
        self.assertEqual(_response_data["message"], "success")
        self.assertListEqual(_response_data["elevator_requests"], [])


class GetLatestElevatorRequestTest(ElevatorAppTests):
    def setUp(self):
        self.factory.cookies[env("COOKIE_NAME")] = self.session["id"]

    def test_get_latest_elevator_request(self):
        _request = self.factory.get('api/request/latest', format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=getLatestElevatorRequest)(_request)
        _response_data = JSONParse(_response.content)
        self.assertEqual(_response_data['message'], 'success')
        self.assertDictEqual(
            _response_data['elevator_request'], self.elevator_requests[len(self.elevator_requests) - 1])


class GetElevatorData(ElevatorAppTests):
    def setUp(self):
        self.factory.cookies[env("COOKIE_NAME")] = self.session["id"]
        self.elevator_instance = self.elevators[0]

    def test_get_elevator_data(self):
        _request = self.factory.get(
            f'api/elevator/{self.elevator_instance["id"]}', format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=getElevatorData)(_request, id=self.elevator_instance["id"])
        _response_data = JSONParse(_response.content)

        self.assertEqual(_response_data['message'], 'success')
        self.assertDictEqual(
            _response_data['elevator'], self.elevator_instance)

    def test_get_elevator_data_one_key(self):
        key = 'gates'
        _request = self.factory.get(
            f'api/elevator/{self.elevator_instance["id"]}/{key}', format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=getElevatorData)(_request, id=self.elevator_instance["id"], key=key)
        _response_data = JSONParse(_response.content)

        self.assertEqual(_response_data['message'], 'success')
        self.assertEqual(
            _response_data[f'elevator_{key}'], self.elevator_instance[key])

    def test_get_elevator_data_invalid(self):
        _request = self.factory.get('api/elevator', format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=getElevatorData)(_request)
        _response_data = JSONParse(_response.content)

        self.assertEqual(_response_data['message'], 'Something Went Wrong')
        self.assertEqual(_response_data['error'], 'Pass valid elevator id')


class GetAllElevatorsData(ElevatorAppTests):
    @classmethod
    def setUpClass(cls):
        super(GetAllElevatorsData, cls).setUpClass()
        cls.factory.cookies[env("COOKIE_NAME")] = cls.session["id"]

        # change lift data
        for x in [1, 3]:
            Elevator.objects.filter(id=cls.elevators[x]).update(gates="open")

        cls.elevators = [ElevatorSerializer(
            x).data for x in Elevator.objects.filter(session=cls.session['id'])]

    def setUp(self):
        self.factory.cookies[env("COOKIE_NAME")] = self.session["id"]
        self.elevator_instance = self.elevators[0]

    def test_get_all_elevator_data(self):
        _request = self.factory.get('api/elevator/all', format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=getAllElevatorsData)(_request)
        _response_data = JSONParse(_response.content)

        self.assertEqual(_response_data['message'], 'success')
        self.assertListEqual(_response_data['elevators'], self.elevators)

    def test_get_all_elevator_data_query_id(self):
        _request = self.factory.get(
            f'api/elevator/all', {"id": self.elevator_instance['id']}, format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=getAllElevatorsData)(_request)
        _response_data = JSONParse(_response.content)

        self.assertEqual(_response_data['message'], 'success')
        self.assertDictEqual(
            _response_data['elevators'][0], self.elevator_instance)

    def test_get_all_elevator_data_query_data(self):
        gates = 'open'
        _request = self.factory.get(
            f'api/elevator/all', {"gates": gates}, format='json')
        _response = middlewareWrapper(
            getCookieMiddleware, view=getAllElevatorsData)(_request)
        _response_data = JSONParse(_response.content)

        filtered_elevators = [x for x in self.elevators if x['gates'] == gates]

        self.assertEqual(_response_data['message'], 'success')
        self.assertListEqual(_response_data['elevators'], filtered_elevators)


class UpdateElevatorData(ElevatorAppTests):
    def setUp(self):
        self.factory.cookies[env("COOKIE_NAME")] = self.session["id"]
        self.elevator_instance = self.elevators[0]

    def test_update_elevator_data(self):
        _request_data = {
            "gates": "open",
            "direction": "up",
        }
        _request = self.factory.patch(
            f'api/elevator/{self.elevator_instance["id"]}/update', format='json', data=_request_data)
        _response = middlewareWrapper(
            getCookieMiddleware, view=updateElevatorData)(_request, id=self.elevator_instance["id"])
        _response_data = JSONParse(_response.content)

        self.assertEqual(_response_data['message'], 'success')
        self.assertDictEqual(_response_data['elevator'], {
                             **self.elevator_instance, **_request_data})

    def test_update_elevator_data_with_invalid_floor(self):
        # the curr_floor of the lift cannot be more than that of the total floors available
        _request_data = {
            "curr_floor": 10
        }
        _request = self.factory.patch(
            f'api/elevator/{self.elevator_instance["id"]}/update', format='json', data=_request_data)
        _response = middlewareWrapper(
            getCookieMiddleware, view=updateElevatorData)(_request, id=self.elevator_instance["id"])
        _response_data = JSONParse(_response.content)

        self.assertEqual(_response_data['message'], 'success')
        self.assertDictEqual(
            _response_data['elevator'], self.elevator_instance)
