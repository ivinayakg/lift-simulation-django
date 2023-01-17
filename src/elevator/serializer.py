from rest_framework import serializers
from elevator.models import Elevator, Session


class SessionSerializer(serializers.Serializer):
    total_elevators = serializers.IntegerField(default=1)
    total_floors = serializers.IntegerField(default=1)

    def create(self):
        if not self.is_valid():
            return None
        validated_data = self.validated_data
        return Session(**validated_data)
