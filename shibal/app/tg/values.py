from enum import IntEnum, StrEnum


class Commands(StrEnum):
    TRIM = "TRIM"
    CUT = "CUT"
    VOLUME_UP = "VOLUME_UP"
    VOLUME_DOWN = "VOLUME_DOWN"
    BACK = "BACK"


class States(StrEnum):
    CMD_CHOOSE = "CMD_CHOOSE"
    TYPING_TRIM_START = "TYPING_TRIM_START"
    TYPING_TRIM_END = "TYPING_TRIM_END"
    TYPING_CUT_START = "TYPING_CUT_START"
    TYPING_CUT_END = "TYPING_CUT_END"
    UPLOAD = "UPLOAD"
    STOP = "STOP"


class Fields(IntEnum):
    CURRENT_FIELD = 9
    START_OVER = 10
    TRIM_START = 11
    TRIM_END = 12
    CUT_START = 13
    CUT_END = 14
    VOLUME_UP = 15
    VOLUME_DOWN = 16
