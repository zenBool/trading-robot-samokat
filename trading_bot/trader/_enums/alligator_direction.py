from enum import Enum


class AlligatorDirection(Enum):
    UP = 2
    UPCORRECTION = 1
    UNCERTAIN = 0
    DOWNCORRECTION = -1
    DOWN = -2
