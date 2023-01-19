from rest_framework.test import APITestCase, APIRequestFactory
from http.cookies import SimpleCookie
from json import dumps as JSONStringify, loads as JSONParse

from elevator.views import createSession, checkSession
from elevator.utils import env
from elevator.models import Session


class CreateSessionTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.factory = APIRequestFactory()
        return super(CreateSessionTest, cls).setUpClass()

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
        self.assertTrue(len(_response.cookies[env("COOKIE_NAME")].value) != 0)
        self.assertJSONEqual(
            _response.content, {"message": "succesfully created"})


class CheckSessionTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        session_data = {
            "total_elevators": 10, "total_floors": 8
        }
        cls.factory = APIRequestFactory()
        session = Session(**session_data)
        session.save()
        cls.session = session
        return super(CheckSessionTest, cls).setUpClass()

    def test_check_session_without_cookie(self):
        cookie = SimpleCookie()
        self.factory.cookies = cookie
        _request = self.factory.get('api',  format='json')
        _response = checkSession(_request)
        self.assertJSONEqual(
            _response.content, {"message": "Something Went Wrong", "error": "Cookie invalid or doesn't exists"})

    def test_check_session_with_cookie(self):
        cookie = SimpleCookie()
        cookie[env("COOKIE_NAME")] = self.session.id
        self.factory.cookies = cookie
        _request = self.factory.get('api',  format='json')
        _response = checkSession(_request)
        _response_data = JSONParse(_response.content)
        self.assertEqual(_response_data["message"],  "success")
        self.assertEqual(_response_data["session"]["id"], self.session.id)
        self.assertEqual(
            _response_data["session"]["total_elevators"], self.session.total_elevators)
        self.assertEqual(
            _response_data["session"]["total_floors"], self.session.total_floors)
