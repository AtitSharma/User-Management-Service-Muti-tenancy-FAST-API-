from enum import Enum, unique


@unique
class _UniqueEnum(Enum):
    @classmethod
    def keys(cls):
        return list(cls.__members__.keys())


class Gender(_UniqueEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHERS = "OTHERS"
    RATHER_NOT_SAY = "RATHER_NOT_SAY"


class UserType(_UniqueEnum):
    ADMIN = "ADMIN"
    HR = "HR"
    EMPLOYEE = "EMPLOYEE"
    TEAM_LEAD = "TEAM_LEAD"


class UserPosition(_UniqueEnum):
    SENIOR = "SENIOR"
    MID = "MID"
    JUNIOR = "JUNIOR"
    TRAINEE = "TRAINEE"
    INTERN = "INTERN"
