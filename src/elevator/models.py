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

    def get_all_lifts(self, *args, **kwargs):
        return self.elevator_set.all()


class Elevator(models.Model):
    DIRECTION_CHOICES = [("UP", "Up"), ("DOWN", "Down")]
    GATES_OF_LIFT_CHOICES = [("OPEN", "Open"), ("CLOSE", "Close")]
    STATUS_OF_LIFT_CHOICES = [
        ("WORKING", "Working"), ("REPAIRING", "Repairing")]

    curr_floor = models.IntegerField(default=0)
    direction = models.CharField(
        max_length=10, choices=DIRECTION_CHOICES, default="UP")
    status = models.CharField(
        max_length=10, choices=STATUS_OF_LIFT_CHOICES, default="WORKING")
    gates = models.CharField(
        max_length=10, choices=GATES_OF_LIFT_CHOICES, default="CLOSE")
    moving = models.BooleanField(default=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def is_moving(self):
        return self.moving
