from enum import Enum, unique
f
@unique
class UserTypeEnum(Enum):

    # larger step due to possible new types
    STANDARD_USER = 10
    SCIENTIST_USER = 20
    ADMIN = 30

@unique
class EmailTypeEnum(Enum):

    REGISTRATION_CONFIRM = 1
    PASSWORD_CHANGE = 2
    EMAIL_CHANGE = 3
    USER_INVITE = 4
    REVIEW_REQUEST = 5
    NOTIFICATION = 6
    STAFF_ANSWER = 7
    ACCOUNT_DELETE = 8

@unique
class NotificationTypeEnum(Enum):

    REVIEW_REQUEST = 1
    NEW_REVIEW = 2
    COMMENT_ANSWER = 3
    REVIEW_ANSWER = 4
    SYSTEM_MESSAGE = 5
    ENDORSEMENT_REQUEST = 6
    REVIEW_REMINDER = 7