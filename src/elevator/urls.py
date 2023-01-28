from django.urls import path, re_path
from elevator.views import createSession, checkSession, createElevatorRequest, getAllElevatorRequest, getLatestElevatorRequests, getElevatorData, changeElevatorData, getAllElevatorData
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
    path('elevator/all',
         middlewareWrapper(getCookieMiddleware, view=getAllElevatorData)),
    path('elevator/<int:id>/update',
         middlewareWrapper(getCookieMiddleware, view=changeElevatorData)),
    re_path(r'^elevator/(?P<id>\d+)(/(?P<key>\w+))?/$',
            middlewareWrapper(getCookieMiddleware, view=getElevatorData)),
]
