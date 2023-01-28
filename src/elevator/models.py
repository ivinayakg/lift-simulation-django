import os
import binascii
from django.db import models

from elevator.constants import elevator_request_completed


class Session(models.Model):
    id = models.CharField('id', max_length=40, primary_key=True)
    total_elevators = models.IntegerField(default=1)
    total_floors = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generateSessionID()
        return super().save(*args, **kwargs)

    @classmethod
    def generateSessionID(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def get_all_elevators(self, query):
        if (query):
            return self.elevator_set.filter(**query)

        return self.elevator_set.all()

    def get_all_elevators_requests(self, query, sort=[]):
        query_set = self.elevatorrequest_set.order_by(*sort)
        if (query.get('completed')):
            elevator_request_completed_filter = elevator_request_completed[query["completed"]]
            query_set = query_set.filter(
                completed=elevator_request_completed_filter)
        return query_set


class Elevator(models.Model):
    curr_floor = models.IntegerField(default=0)
    direction = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    gates = models.CharField(max_length=30)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class ElevatorRequest(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    destination = models.IntegerField(default=0)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        print(self.session)
        print(self.session.total_floors)
        return super().save(self, *args, **kwargs)

    class Meta:
        db_table = "elevator_request"
