from django.urls import path
from elevator.views import createSession, checkSession
from elevator.middleware import getCookieMiddleware, middlewareWrapper

urlpatterns = [
    path('initiate', createSession),
    path('', middlewareWrapper(getCookieMiddleware, view=checkSession))
]
