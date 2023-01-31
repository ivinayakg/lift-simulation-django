from django.urls import path, re_path
from elevator.views import createSession, checkSession, createElevatorRequest, getAllElevatorRequests, getLatestElevatorRequest, getElevatorData, updateElevatorData, getAllElevatorsData
from elevator.middleware import getCookieMiddleware, middlewareWrapper

urlpatterns = [
    path('initiate', createSession),
    path('', middlewareWrapper(getCookieMiddleware, view=checkSession)),
    path('request', middlewareWrapper(
        getCookieMiddleware, view=createElevatorRequest)),
    path('request/all', middlewareWrapper(getCookieMiddleware,
         view=getAllElevatorRequests)),
    path('request/latest', middlewareWrapper(getCookieMiddleware,
         view=getLatestElevatorRequest)),
    path('elevator/all',
         middlewareWrapper(getCookieMiddleware, view=getAllElevatorsData)),
    path('elevator/<str:id>/update',
         middlewareWrapper(getCookieMiddleware, view=updateElevatorData)),
    re_path(r'^elevator/(?P<id>\w+)(/(?P<key>\w+))?/$',
            middlewareWrapper(getCookieMiddleware, view=getElevatorData)),
]
