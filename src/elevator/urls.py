from django.urls import path
from elevator.views import createSession, checkSession, createElevatorRequest, getAllElevatorRequest, getLatestElevatorRequests
from elevator.middleware import getCookieMiddleware, middlewareWrapper

urlpatterns = [
    path('initiate', createSession),
    path('', middlewareWrapper(getCookieMiddleware, view=checkSession)),
    path('request', middlewareWrapper(
        getCookieMiddleware, view=createElevatorRequest)),
    path('request/all', middlewareWrapper(getCookieMiddleware,
         view=getAllElevatorRequest)),
    path('request/latest', middlewareWrapper(getCookieMiddleware,
         view=getLatestElevatorRequests)),
]
