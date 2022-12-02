from enum import Enum


class Head_Pose(Enum):
    RIGHT = 1
    CENTER = 2
    LEFT = 3


class Tail_Pose(Enum):
    RIGHT = 1
    CENTER = 2
    LEFT = 3


class Wing_Pose(Enum):
    ON = 1
    OFF = 2


class Leg_Pose(Enum):
    UP = 1
    DOWN = 2
