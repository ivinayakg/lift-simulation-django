elevator_request_completed = {
    "false": False,
    "true": True
}


class Elevator_Direction_Choices:
    UP = 'up'
    DOWN = "down"
    STALE = "stale"

    def has(self, value=''):
        if self.UP == value or self.DOWN == value or self.STALE == value:
            return True

elevator_direction_choices = Elevator_Direction_Choices()

class Elevator_Status_Choices:
    WORKING = "working"
    MAINTAINENCE = "maintainence"

    def has(self, value=''):
        if self.WORKING == value or self.MAINTAINENCE == value:
            return True

elevator_status_choices = Elevator_Status_Choices()

class Elevator_Gates_Choices:
    OPEN = 'open'
    CLOSE = "close"

    def has(self, value=''):
        if self.OPEN == value or self.CLOSE == value:
            return True

elevator_gates_choices = Elevator_Gates_Choices()