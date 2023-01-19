from django.urls import path
from elevator.views import createSession, checkSession

urlpatterns = [
    path('initiate', createSession),
    path('', checkSession)
]
