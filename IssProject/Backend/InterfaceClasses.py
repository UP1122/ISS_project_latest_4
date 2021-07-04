from enum import Enum

class ShuttleType(Enum):
    MANNED = 1,
    UN_MANNED = 2


class ShuttleState:
    def __init__(self,shuttleId, isFlying, destination, flightPercent, location,shuttleType):
        self.shuttleId = shuttleId
        self.isFlying = isFlying
        self.flightPercent = flightPercent
        self.destination = destination
        self.location = location
        self.type = shuttleType