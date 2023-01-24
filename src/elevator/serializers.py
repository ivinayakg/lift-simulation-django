from rest_framework import serializers
from elevator.models import Elevator, Session, ElevatorRequest


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        exclude = ['id']

    def create(self):
        if not self.is_valid():
            return None
        validated_data = self.validated_data
        session = Session(**validated_data)
        session.save()
        session_data = {"id": session.id, **self.data}
        return {"instance": session, "data": session_data}


class ElevatorRequestSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ElevatorRequest
        exclude = ['id']

    def create(self):
        if not self.is_valid():
            return None
        validated_data = self.validated_data
        elevator_request = ElevatorRequest(**validated_data)
        elevator_request.save()
        elevator_request_data = {"id": elevator_request.id, **self.data}
        return {"instance": elevator_request, "data": elevator_request_data}
