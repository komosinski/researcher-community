from enum import Enum, unique


@unique
class UserTypeEnum(Enum):

    # larger step due to possible new types
    STANDARD_USER = 10
    RESEARCHER_USER = 20
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
    PAPER_COMMENT = 4
    REVIEWER_COMMENTED_PAPER = 5
    SYSTEM_MESSAGE = 6
    ENDORSEMENT_REQUEST = 7
    REVIEW_REMINDER = 8
  


@unique 
class MessageTopicEnum(Enum):

    OTHER = 1
    ENDORSEMENT = 2
    TECHNICAL_ISSUES = 3
    CORRETIONCS = 4
