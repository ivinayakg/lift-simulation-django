import os
import binascii
from django.db import models


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

    def get_all_elevators_requests(self, query, sort=['-timestamp']):
        query_set = self.elevatorrequest_set.order_by(*sort)
        if (query):
            query_set = query_set.filter(**query)

        return query_set


class Elevator(models.Model):
    id = models.CharField('id', max_length=40, primary_key=True)
    curr_floor = models.IntegerField(default=0)
    direction = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    gates = models.CharField(max_length=30)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generateSessionID()
        return super().save(*args, **kwargs)

    @classmethod
    def generateSessionID(cls):
        return binascii.hexlify(os.urandom(20)).decode()


class ElevatorRequest(models.Model):
    id = models.CharField('id', max_length=40, primary_key=True)
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    destination = models.IntegerField(default=0)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generateSessionID()
        return super().save(*args, **kwargs)

    @classmethod
    def generateSessionID(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    class Meta:
        db_table = "elevator_request"
