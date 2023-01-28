from rest_framework import serializers
from rest_framework.fields import empty

from elevator.models import Elevator, Session, ElevatorRequest
from elevator.constants import elevator_direction_choices, elevator_gates_choices, elevator_status_choices


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
    class Meta:
        model = ElevatorRequest
        exclude = ['id']
        extra_kwargs = {'timestamp': {'read_only': True}}

    def create(self):
        if not self.is_valid():
            return None
        validated_data = self.validated_data
        elevator_request = ElevatorRequest(**validated_data)
        elevator_request.save()
        elevator_request_data = {"id": elevator_request.id, **self.data}
        return {"instance": elevator_request, "data": elevator_request_data}


class ElevatorSerializer(serializers.ModelSerializer):
    default_gate = elevator_gates_choices.CLOSE
    default_direction = elevator_direction_choices.STALE
    default_status = elevator_status_choices.WORKING
    default_floor = 1

    class Meta:
        model = Elevator
        exclude = ["id"]

    def __init__(self, instance=None, data=empty, **kwargs):
        if not instance:
            if not data.get('curr_floor'):
                data['curr_floor'] = self.default_floor
            if not data.get('direction'):
                data['direction'] = self.default_direction
            if not data.get('gates'):
                data['gates'] = self.default_gate
            if not data.get('status'):
                data['status'] = self.default_status
        super().__init__(instance, data, **kwargs)

    def create(self):
        if not self.is_valid():
            return None
        validated_data = self.validated_data
        elevator = Elevator(**validated_data)
        elevator.save()
        elevator_data = {"id": elevator.id, **self.data}
        return {"instance": elevator, "data": elevator_data}

    def update(self):
        if elevator_gates_choices.has(self.initial_data.get('gates')):
            self.initial_data['gates'] = self.initial_data.get(
                'gates', self.instance.gates)

        if elevator_direction_choices.has(self.initial_data.get('direction')):
            self.initial_data['direction'] = self.initial_data.get(
                'direction', self.instance.direction)

        if elevator_status_choices.has(self.initial_data.get('status')):
            self.initial_data['status'] = self.initial_data.get(
                'status', self.instance.status)

        if self.initial_data.get('curr_floor'):
            self.initial_data['curr_floor'] = int(
                self.initial_data.get('curr_floor'))
        else:
            self.initial_data['curr_floor'] = self.instance.curr_floor

        if not self.is_valid():
            raise Exception("Something went wrong")

        return super().update(self.instance, self.validated_data)
