import datetime as dt
from flask import url_for

from open_science import db, app
from open_science.models import create_essential_data, PaperRevision, Comment, Review, Paper, Tag, User, PrivilegeSet, \
    ReviewRequest, VoteComment, MessageToStaff, MessageTopic, NotificationType, Notification, License, Suggestion, \
    CalibrationPaper, RedFlagComment, RedFlagPaperRevision, RedFlagReview, RedFlagTag, RedFlagUser, \
    RevisionChangesComponent

from open_science.enums import UserTypeEnum, NotificationTypeEnum
from text_processing.prepocess_text import get_text


def create_test_data():
    create_essential_data()

    # check if the test data has been created
    if PaperRevision.query.all():
        return False

    # comments
    c1 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c1)

    c2 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c2)

    c3 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c3.rel_related_comment = [c2]
    db.session.add(c3)

    c4 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c4)

    c5 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c5)

    c6 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c6.rel_related_comment = [c5]
    db.session.add(c6)

    c7 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c7)

    c8 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c8)

    c9 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c9.rel_related_comment = [c8]
    db.session.add(c9)

    c10 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c10)

    c11 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c11)

    c12 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c12.rel_related_comment = [c11]
    db.session.add(c12)

    c13 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c13)

    c14 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c14)

    c15 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c15.rel_related_comment = [c14]
    db.session.add(c15)

    c16 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c16)

    c17 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c17)

    c18 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c18.rel_related_comment = [c17]
    db.session.add(c18)

    c19 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c19)

    c20 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c20)

    c21 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c21.rel_related_comment = [c20]
    db.session.add(c21)

    c22 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c22)

    c23 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c23)

    c24 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c24.rel_related_comment = [c23]
    db.session.add(c24)

    c25 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c25)

    c26 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c26)

    c27 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c27.rel_related_comment = [c26]
    db.session.add(c27)

    c28 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c28)

    c29 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c29)

    c30 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c30.rel_related_comment = [c29]
    db.session.add(c30)

    c31 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c31)

    c32 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c32)

    c33 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c33.rel_related_comment = [c32]
    db.session.add(c33)

    c34 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c34)

    c35 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c35)

    c36 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c36.rel_related_comment = [c35]
    db.session.add(c36)

    c37 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c37)

    c38 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c38)

    c39 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c39.rel_related_comment = [c38]
    db.session.add(c39)

    c40 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c40)

    c41 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c41)

    c42 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c42.rel_related_comment = [c41]
    db.session.add(c42)

    c43 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c43)

    c44 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c44)

    c45 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c45.rel_related_comment = [c44]
    db.session.add(c45)

    c46 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c46)

    c47 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c47)

    c48 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c48.rel_related_comment = [c47]
    db.session.add(c48)

    c49 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c49)

    c50 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c50)

    c51 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c51.rel_related_comment = [c50]
    db.session.add(c51)

    c52 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c52)

    c53 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c53)

    c54 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c54.rel_related_comment = [c53]
    db.session.add(c54)

    c55 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c55)

    c56 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c56)

    c57 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c57.rel_related_comment = [c56]
    db.session.add(c57)

    c58 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c58)

    c59 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c59)

    c60 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c60.rel_related_comment = [c59]
    db.session.add(c60)

    c61 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c61)

    c62 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c62)

    c63 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c63.rel_related_comment = [c62]
    db.session.add(c63)

    c64 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c64)

    c65 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c65)

    c66 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c66.rel_related_comment = [c65]
    db.session.add(c66)

    c67 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c67)

    c68 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c68)

    c69 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c69.rel_related_comment = [c68]
    db.session.add(c69)

    c70 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c70)

    c71 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c71)

    c72 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c72.rel_related_comment = [c71]
    db.session.add(c72)

    c73 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c73)

    c74 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c74)

    c75 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c75.rel_related_comment = [c74]
    db.session.add(c75)

    c76 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c76)

    c77 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c77)

    c78 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c78.rel_related_comment = [c77]
    db.session.add(c78)

    c79 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c79)

    c80 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c80)

    c81 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c81.rel_related_comment = [c80]
    db.session.add(c81)

    c82 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c82)

    c83 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c83)

    c84 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c84.rel_related_comment = [c83]
    db.session.add(c84)

    c85 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c85)

    c86 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c86)

    c87 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c87.rel_related_comment = [c86]
    db.session.add(c87)

    c88 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c88)

    c89 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c89)

    c90 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c90.rel_related_comment = [c89]
    db.session.add(c90)

    c91 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c91)

    c92 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c92)

    c93 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c93.rel_related_comment = [c92]
    db.session.add(c93)

    c94 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c94)

    c95 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c95)

    c96 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c96.rel_related_comment = [c95]
    db.session.add(c96)

    c97 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c97)

    c98 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c98)

    c99 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c99.rel_related_comment = [c98]
    db.session.add(c99)

    c100 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c100)

    c101 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c101)

    c102 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c102.rel_related_comment = [c101]
    db.session.add(c102)

    c103 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c103)

    c104 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c104)

    c105 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c105.rel_related_comment = [c104]
    db.session.add(c105)

    c106 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c106)

    c107 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c107)

    c108 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c108.rel_related_comment = [c107]
    db.session.add(c108)

    c109 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c109)

    c110 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c110)

    c111 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c111.rel_related_comment = [c110]
    db.session.add(c111)

    c112 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c112)

    c113 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c113)

    c114 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c114.rel_related_comment = [c113]
    db.session.add(c114)

    c115 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c115)

    c116 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c116)

    c117 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c117.rel_related_comment = [c116]
    db.session.add(c117)

    c118 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c118)

    c119 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c119)

    c120 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c120.rel_related_comment = [c119]
    db.session.add(c120)

    c121 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c121)

    c122 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c122)

    c123 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c123.rel_related_comment = [c122]
    db.session.add(c123)

    c124 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c124)

    c125 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c125)

    c126 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c126.rel_related_comment = [c125]
    db.session.add(c126)

    c127 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c127)

    c128 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c128)

    c129 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c129.rel_related_comment = [c128]
    db.session.add(c129)

    c130 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c130)

    c131 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c131)

    c132 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c132.rel_related_comment = [c131]
    db.session.add(c132)

    c133 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c133)

    c134 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c134)

    c135 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c135.rel_related_comment = [c134]
    db.session.add(c135)

    c136 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c136)

    c137 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c137)

    c138 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c138.rel_related_comment = [c137]
    db.session.add(c138)

    c139 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c139)

    c140 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c140)

    c141 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c141.rel_related_comment = [c140]
    db.session.add(c141)

    c142 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c142)

    c143 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c143)

    c144 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c144.rel_related_comment = [c143]
    db.session.add(c144)

    c145 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c145)

    c146 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c146)

    c147 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c147.rel_related_comment = [c146]
    db.session.add(c147)

    c148 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c148)

    c149 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c149)

    c150 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c150.rel_related_comment = [c149]
    db.session.add(c150)

    c151 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c151)

    c152 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c152)

    c153 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c153.rel_related_comment = [c152]
    db.session.add(c153)

    c154 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c154)

    c155 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c155)

    c156 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c156.rel_related_comment = [c155]
    db.session.add(c156)

    c157 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c157)

    c158 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c158)

    c159 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c159.rel_related_comment = [c158]
    db.session.add(c159)

    c160 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c160)

    c161 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c161)

    c162 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c162.rel_related_comment = [c161]
    db.session.add(c162)

    c163 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c163)

    c164 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c164)

    c165 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c165.rel_related_comment = [c164]
    db.session.add(c165)

    c166 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c166)

    c167 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c167)

    c168 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c168.rel_related_comment = [c167]
    db.session.add(c168)

    c169 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c169)

    c170 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.RESEARCHER_USER.value,
            level=0
        )
    db.session.add(c170)

    c171 = Comment(
            text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ut tellus ac leo accumsan hendrerit. "
                 "Mauris ut justo sed sapien accumsan aliquet. Morbi eros nisl, euismod scelerisque ex id, "
                 "tristique bibendum nisl. Mauris quis magna ultrices, accumsan ligula ac, varius neque. Praesent "
                 "pellentesque ultrices accumsan. Cras euismod metus non nunc vestibulum dictum. Vestibulum ante ipsum "
                 "primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam massa leo, gravida varius "
                 "bibendum ac, venenatis et est. In feugiat lacus quis velit pulvinar, eget luctus est ornare. Sed "
                 "ullamcorper turpis non justo porta, imperdiet egestas quam malesuada. Donec sed libero efficitur, "
                 "maximus felis maximus, elementum enim. Morbi id hendrerit metus, in tristique ante.",
            date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
            creator_role=UserTypeEnum.STANDARD_USER.value,
            level=1
        )
    c171.rel_related_comment = [c170]
    db.session.add(c171)

    # reviews
    r1 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.95,
        evaluation_conclusion=0.25,
        evaluation_error=0.69,
        evaluation_organize=0.94,
        evaluation_accept=True,
        confidence=0.89,
    )
    r1.rel_comments_to_this_review = [c52, c53, c54]
    db.session.add(r1)

    r2 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.67,
        evaluation_conclusion=0.01,
        evaluation_error=0.67,
        evaluation_organize=0.18,
        evaluation_accept=True,
        confidence=0.57,
    )
    r2.rel_comments_to_this_review = [c55, c56, c57]
    db.session.add(r2)

    r3 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.89,
        evaluation_conclusion=0.18,
        evaluation_error=0.87,
        evaluation_organize=0.65,
        evaluation_accept=True,
        confidence=0.65,
    )
    r3.rel_comments_to_this_review = [c58, c59, c60]
    db.session.add(r3)

    r4 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.72,
        evaluation_conclusion=0.89,
        evaluation_error=0.49,
        evaluation_organize=0.65,
        evaluation_accept=True,
        confidence=0.61,
    )
    r4.rel_comments_to_this_review = [c61, c62, c63]
    db.session.add(r4)

    r5 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.98,
        evaluation_conclusion=0.13,
        evaluation_error=0.33,
        evaluation_organize=0.0,
        evaluation_accept=True,
        confidence=0.33,
    )
    r5.rel_comments_to_this_review = [c64, c65, c66]
    db.session.add(r5)

    r6 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.41,
        evaluation_conclusion=0.49,
        evaluation_error=0.1,
        evaluation_organize=0.66,
        evaluation_accept=True,
        confidence=0.12,
    )
    r6.rel_comments_to_this_review = [c67, c68, c69]
    db.session.add(r6)

    r7 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.05,
        evaluation_conclusion=0.0,
        evaluation_error=0.99,
        evaluation_organize=0.93,
        evaluation_accept=True,
        confidence=0.55,
    )
    r7.rel_comments_to_this_review = [c70, c71, c72]
    db.session.add(r7)

    r8 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.08,
        evaluation_conclusion=0.73,
        evaluation_error=0.17,
        evaluation_organize=0.58,
        evaluation_accept=True,
        confidence=0.79,
    )
    r8.rel_comments_to_this_review = [c73, c74, c75]
    db.session.add(r8)

    r9 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.64,
        evaluation_conclusion=0.77,
        evaluation_error=0.77,
        evaluation_organize=0.04,
        evaluation_accept=True,
        confidence=0.38,
    )
    r9.rel_comments_to_this_review = [c76, c77, c78]
    db.session.add(r9)

    r10 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.21,
        evaluation_conclusion=0.15,
        evaluation_error=0.86,
        evaluation_organize=0.28,
        evaluation_accept=True,
        confidence=0.4,
    )
    r10.rel_comments_to_this_review = [c79, c80, c81]
    db.session.add(r10)

    r11 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.68,
        evaluation_conclusion=0.89,
        evaluation_error=0.82,
        evaluation_organize=0.54,
        evaluation_accept=True,
        confidence=0.07,
    )
    r11.rel_comments_to_this_review = [c82, c83, c84]
    db.session.add(r11)

    r12 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.96,
        evaluation_conclusion=0.93,
        evaluation_error=0.27,
        evaluation_organize=0.01,
        evaluation_accept=True,
        confidence=0.14,
    )
    r12.rel_comments_to_this_review = [c85, c86, c87]
    db.session.add(r12)

    r13 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.9,
        evaluation_conclusion=0.07,
        evaluation_error=0.78,
        evaluation_organize=0.71,
        evaluation_accept=True,
        confidence=0.1,
    )
    r13.rel_comments_to_this_review = [c88, c89, c90]
    db.session.add(r13)

    r14 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.81,
        evaluation_conclusion=0.94,
        evaluation_error=0.58,
        evaluation_organize=0.09,
        evaluation_accept=True,
        confidence=0.51,
    )
    r14.rel_comments_to_this_review = [c91, c92, c93]
    db.session.add(r14)

    r15 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.57,
        evaluation_conclusion=0.49,
        evaluation_error=0.39,
        evaluation_organize=0.78,
        evaluation_accept=True,
        confidence=0.22,
    )
    r15.rel_comments_to_this_review = [c94, c95, c96]
    db.session.add(r15)

    r16 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.05,
        evaluation_conclusion=0.83,
        evaluation_error=0.53,
        evaluation_organize=0.18,
        evaluation_accept=True,
        confidence=0.58,
    )
    r16.rel_comments_to_this_review = [c97, c98, c99]
    db.session.add(r16)

    r17 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.28,
        evaluation_conclusion=0.77,
        evaluation_error=0.09,
        evaluation_organize=0.63,
        evaluation_accept=True,
        confidence=0.23,
    )
    r17.rel_comments_to_this_review = [c100, c101, c102]
    db.session.add(r17)

    r18 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.72,
        evaluation_conclusion=0.54,
        evaluation_error=0.41,
        evaluation_organize=0.5,
        evaluation_accept=True,
        confidence=0.07,
    )
    r18.rel_comments_to_this_review = [c103, c104, c105]
    db.session.add(r18)

    r19 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.57,
        evaluation_conclusion=0.72,
        evaluation_error=0.43,
        evaluation_organize=0.07,
        evaluation_accept=True,
        confidence=0.32,
    )
    r19.rel_comments_to_this_review = [c106, c107, c108]
    db.session.add(r19)

    r20 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.76,
        evaluation_conclusion=0.2,
        evaluation_error=0.9,
        evaluation_organize=0.17,
        evaluation_accept=True,
        confidence=0.9,
    )
    r20.rel_comments_to_this_review = [c109, c110, c111]
    db.session.add(r20)

    r21 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=1.0,
        evaluation_conclusion=0.5,
        evaluation_error=0.3,
        evaluation_organize=0.09,
        evaluation_accept=True,
        confidence=0.42,
    )
    r21.rel_comments_to_this_review = [c112, c113, c114]
    db.session.add(r21)

    r22 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.3,
        evaluation_conclusion=0.44,
        evaluation_error=0.66,
        evaluation_organize=0.38,
        evaluation_accept=True,
        confidence=0.56,
    )
    r22.rel_comments_to_this_review = [c115, c116, c117]
    db.session.add(r22)

    r23 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.38,
        evaluation_conclusion=0.02,
        evaluation_error=0.99,
        evaluation_organize=0.72,
        evaluation_accept=True,
        confidence=0.39,
    )
    r23.rel_comments_to_this_review = [c118, c119, c120]
    db.session.add(r23)

    r24 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.76,
        evaluation_conclusion=0.63,
        evaluation_error=0.17,
        evaluation_organize=0.26,
        evaluation_accept=True,
        confidence=0.36,
    )
    r24.rel_comments_to_this_review = [c121, c122, c123]
    db.session.add(r24)

    r25 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.31,
        evaluation_conclusion=0.32,
        evaluation_error=0.15,
        evaluation_organize=0.59,
        evaluation_accept=True,
        confidence=0.07,
    )
    r25.rel_comments_to_this_review = [c124, c125, c126]
    db.session.add(r25)

    r26 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.85,
        evaluation_conclusion=0.56,
        evaluation_error=0.19,
        evaluation_organize=0.41,
        evaluation_accept=True,
        confidence=0.88,
    )
    r26.rel_comments_to_this_review = [c127, c128, c129]
    db.session.add(r26)

    r27 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.59,
        evaluation_conclusion=0.03,
        evaluation_error=0.63,
        evaluation_organize=0.93,
        evaluation_accept=False,
        confidence=0.66,
    )
    r27.rel_comments_to_this_review = [c130, c131, c132]
    db.session.add(r27)

    r28 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.33,
        evaluation_conclusion=0.57,
        evaluation_error=0.08,
        evaluation_organize=0.57,
        evaluation_accept=False,
        confidence=0.68,
    )
    r28.rel_comments_to_this_review = [c133, c134, c135]
    db.session.add(r28)

    r29 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.66,
        evaluation_conclusion=0.99,
        evaluation_error=0.48,
        evaluation_organize=0.55,
        evaluation_accept=True,
        confidence=0.47,
    )
    r29.rel_comments_to_this_review = [c136, c137, c138]
    db.session.add(r29)

    r30 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.25,
        evaluation_conclusion=0.67,
        evaluation_error=0.12,
        evaluation_organize=0.08,
        evaluation_accept=True,
        confidence=0.27,
    )
    r30.rel_comments_to_this_review = [c139, c140, c141]
    db.session.add(r30)

    r31 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.32,
        evaluation_conclusion=0.37,
        evaluation_error=0.66,
        evaluation_organize=0.77,
        evaluation_accept=True,
        confidence=0.14,
    )
    r31.rel_comments_to_this_review = [c142, c143, c144]
    db.session.add(r31)

    r32 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.41,
        evaluation_conclusion=0.92,
        evaluation_error=0.47,
        evaluation_organize=0.83,
        evaluation_accept=True,
        confidence=0.34,
    )
    r32.rel_comments_to_this_review = [c145, c146, c147]
    db.session.add(r32)

    r33 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.39,
        evaluation_conclusion=0.43,
        evaluation_error=0.89,
        evaluation_organize=0.4,
        evaluation_accept=True,
        confidence=0.35,
    )
    r33.rel_comments_to_this_review = [c148, c149, c150]
    db.session.add(r33)

    r34 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.95,
        evaluation_conclusion=0.87,
        evaluation_error=0.9,
        evaluation_organize=0.46,
        evaluation_accept=True,
        confidence=0.92,
    )
    r34.rel_comments_to_this_review = [c151, c152, c153]
    db.session.add(r34)

    r35 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.18,
        evaluation_conclusion=0.56,
        evaluation_error=0.06,
        evaluation_organize=0.58,
        evaluation_accept=True,
        confidence=0.95,
    )
    r35.rel_comments_to_this_review = [c154, c155, c156]
    db.session.add(r35)

    r36 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.0,
        evaluation_conclusion=0.95,
        evaluation_error=0.9,
        evaluation_organize=0.25,
        evaluation_accept=True,
        confidence=0.06,
    )
    r36.rel_comments_to_this_review = [c157, c158, c159]
    db.session.add(r36)

    r37 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.62,
        evaluation_conclusion=0.23,
        evaluation_error=0.49,
        evaluation_organize=0.43,
        evaluation_accept=False,
        confidence=0.69,
    )
    r37.rel_comments_to_this_review = [c160, c161, c162]
    db.session.add(r37)

    r38 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.13,
        evaluation_conclusion=0.75,
        evaluation_error=0.49,
        evaluation_organize=0.19,
        evaluation_accept=False,
        confidence=0.38,
    )
    r38.rel_comments_to_this_review = [c163, c164, c165]
    db.session.add(r38)

    r39 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.22,
        evaluation_conclusion=0.79,
        evaluation_error=0.45,
        evaluation_organize=0.13,
        evaluation_accept=True,
        confidence=0.07,
    )
    r39.rel_comments_to_this_review = [c166, c167, c168]
    db.session.add(r39)

    r40 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.55,
        evaluation_conclusion=0.8,
        evaluation_error=0.49,
        evaluation_organize=0.71,
        evaluation_accept=True,
        confidence=0.38,
    )
    r40.rel_comments_to_this_review = [c169, c170, c171]
    db.session.add(r40)

    p1 = Paper()
    db.session.add(p1)

    p2 = Paper()
    db.session.add(p2)

    p3 = Paper()
    db.session.add(p3)

    p4 = Paper()
    db.session.add(p4)

    p5 = Paper()
    db.session.add(p5)

    p6 = Paper()
    db.session.add(p6)

    p7 = Paper()
    db.session.add(p7)

    p8 = Paper()
    db.session.add(p8)

    p9 = Paper()
    db.session.add(p9)

    p10 = Paper()
    db.session.add(p10)

    p11 = Paper()
    db.session.add(p11)

    p12 = Paper()
    db.session.add(p12)

    p13 = Paper()
    db.session.add(p13)

    p14 = Paper()
    db.session.add(p14)

    p15 = Paper()
    db.session.add(p15)

    # paper revisions
    pve1_1 = PaperRevision(
        version=1,
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}1.pdf",
        title="Assistance of an expert in the participatory planning model in the area included in the revitalisation "
              "programme in view of the desired changes. Based on the example of the district of Śródka in Poznań",
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}1.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=3
    )
    pve1_1.rel_related_comments = [c1, c2, c3]
    pve1_1.rel_parent_paper = p1
    pve1_1.rel_related_reviews = [r1, r2, r3, r4]
    db.session.add(pve1_1)

    pve1_2 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}1.pdf",
        title="Assistance of an expert in the participatory planning model in the area included in the revitalisation "
              "programme in view of the desired changes. Based on the example of the district of Śródka in Poznań",
        version=2,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}1.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=3
    )
    pve1_2.rel_related_comments = [c4, c5, c6]
    pve1_2.rel_parent_paper = p1
    pve1_2.rel_related_reviews = [r5, r6, r7, r8]
    db.session.add(pve1_2)

    pve1_3 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}1.pdf",
        title="Assistance of an expert in the participatory planning model in the area included in the revitalisation "
              "programme in view of the desired changes. Based on the example of the district of Śródka in Poznań",
        version=3,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}1.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=3
    )
    pve1_3.rel_related_comments = [c7, c8, c9]
    pve1_3.rel_parent_paper = p1
    pve1_3.rel_related_reviews = [r9, r10, r11, r12]
    db.session.add(pve1_3)

    pve2_1 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}2.pdf",
        title="Climate Change and Building Energy Consumption: AReview of the Impact of Weather Parameters Influenced "
              "by Climate Change on Household Heating and Cooling Demands of Buildings",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}2.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve2_1.rel_related_comments = [c10, c11, c12]
    pve2_1.rel_parent_paper = p2
    pve2_1.rel_related_reviews = [r13, r14]
    db.session.add(pve2_1)

    pve2_2 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}2.pdf",
        title="Climate Change and Building Energy Consumption: AReview of the Impact of Weather Parameters Influenced "
              "by Climate Change on Household Heating and Cooling Demands of Buildings",
        version=2,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}2.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=3
    )
    pve2_2.rel_parent_paper = p2
    db.session.add(pve2_2)

    pve3 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}3.pdf",
        title="Drawing Skills of Candidates for Architectural Studies vs.Learning Outcomes of Graduates. Comparative "
              "Research Basedon the Example of The Faculty of Architecture, PoznanUniversity of Technology",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}3.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve3.rel_related_comments = [c13, c14, c15]
    pve3.rel_parent_paper = p3
    pve3.rel_related_reviews = [r15, r16]
    db.session.add(pve3)

    pve4 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}4.pdf",
        title="Housing Expectations of Future Seniors Based on an Example ofthe Inhabitants of Poland",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}4.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve4.rel_related_comments = [c16, c17, c18]
    pve4.rel_parent_paper = p4
    pve4.rel_related_reviews = [r17, r18]
    db.session.add(pve4)

    pve5 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}5.pdf",
        title="How to combine descriptive and normative approaches in participatory urban planning: an experimental "
              "mixed-method implemented in the downtown district of Poznań, Poland",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}5.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve5.rel_related_comments = [c19, c20, c21]
    pve5.rel_parent_paper = p5
    pve5.rel_related_reviews = [r19, r20]
    db.session.add(pve5)

    pve6 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}6.pdf",
        title="Inclusiveness of Urban Space and Tools for the Assessment ofthe Quality of Urban Life—A Critical "
              "Approach",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}6.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve6.rel_related_comments = [c22, c23, c24]
    pve6.rel_parent_paper = p6
    pve6.rel_related_reviews = [r21, r22]
    db.session.add(pve6)

    pve7 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}7.pdf",
        title="Teaching acoustics to students of architecture",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}7.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve7.rel_related_comments = [c25, c26, c27]
    pve7.rel_parent_paper = p7
    pve7.rel_related_reviews = [r23, r24]
    db.session.add(pve7)

    pve8 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}8.pdf",
        title="The Impact Assessment of Climate Change on Building Energy Consumption in Poland",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}8.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve8.rel_related_comments = [c28, c29, c30]
    pve8.rel_parent_paper = p8
    pve8.rel_related_reviews = [r25, r26]
    db.session.add(pve8)

    pve9 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}9.pdf",
        title="THE IMPORTANCE OF FLEXIBILITY IN ADAPTIVE REUSE OF INDUSTRIAL HERITAGE: LEARNING FROM IRANIAN CASES",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}9.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve9.rel_related_comments = [c31, c32, c33]
    pve9.rel_parent_paper = p9
    pve9.rel_related_reviews = [r27, r28]
    db.session.add(pve9)

    pve10 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}10.pdf",
        title="The Importance of Water and Climate-Related Aspects in theQuality of Urban Life Assessment",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}10.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve10.rel_related_comments = [c34, c35, c36]
    pve10.rel_parent_paper = p10
    pve10.rel_related_reviews = [r29, r30]
    db.session.add(pve10)

    pve11 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}11.pdf",
        title="BANK CORPORATE FINANCING: WORLD EXPERIENCE AND UKRAINIAN REALITIES",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}11.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve11.rel_related_comments = [c37, c38, c39]
    pve11.rel_parent_paper = p11
    pve11.rel_related_reviews = [r31, r32]
    db.session.add(pve11)

    pve12 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}12.pdf",
        title="economic activity and social determinants versus entrepreneurship in smes – selected aspects",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}12.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve12.rel_related_comments = [c40, c41, c42]
    pve12.rel_parent_paper = p12
    pve12.rel_related_reviews = [r33, r34]
    db.session.add(pve12)

    pve13 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}13.pdf",
        title="Application of Grey Systems Theory in the Analysis of Data Obtained from Family Businesses",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}13.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve13.rel_related_comments = [c43, c44, c45]
    pve13.rel_parent_paper = p13
    pve13.rel_related_reviews = [r35, r36]
    db.session.add(pve13)

    pve14 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}14.pdf",
        title="Attitudes of Polish entrepreneurs towards knowledge workers aged 65 plus in the context of their good "
              "employment practices",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}14.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve14.rel_related_comments = [c46, c47, c48]
    pve14.rel_parent_paper = p14
    pve14.rel_related_reviews = [r37, r38]
    db.session.add(pve14)

    pve15_1 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}15.pdf",
        title="Decision Making in Health Management during Crisis: A Case Study Based on Epidemiological Curves of "
              "China and Italy against COVID-19",
        version=1,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}15.pdf"),
        publication_date=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        confidence_level=2
    )
    pve15_1.rel_related_comments = [c49, c50, c51]
    pve15_1.rel_parent_paper = p15
    pve15_1.rel_related_reviews = [r39, r40]
    db.session.add(pve15_1)

    pve15_2 = PaperRevision(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}15.pdf",
        title="Decision Making in Health Management during Crisis: A Case Study Based on Epidemiological Curves of "
              "China and Italy against COVID-19",
        version=2,
        abstract="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus in felis metus. Integer commodo "
                 "scelerisque finibus. Donec eget tincidunt sapien, a egestas ex. Nullam eget pulvinar elit. Praesent "
                 "blandit vel dui eu maximus. Aliquam mauris purus, semper sed condimentum quis, varius a nisi. "
                 "Suspendisse id consequat lacus. Sed nec mollis nunc, in ullamcorper quam. Praesent nec diam "
                 "fringilla, laoreet risus at, iaculis enim. Nunc lobortis, quam id faucibus interdum, dolor quam "
                 "lacinia nulla, quis laoreet sapien lectus sit amet lectus. Etiam in consequat nunc, vel ornare "
                 "nisl. Aliquam aliquet felis dictum elit molestie, quis iaculis nisl vulputate. Morbi vel augue "
                 "luctus arcu tempus interdum. Mauris in diam eu sapien bibendum auctor laoreet sit amet quam. "
                 "Suspendisse auctor id orci quis placerat.",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}15.pdf"),
        confidence_level=2
    )
    pve15_2.rel_parent_paper = p15
    db.session.add(pve15_2)

    # to read Papers' id from autoincrement
    db.session.flush()

    # tags
    t1 = Tag(
        name="Mechanics",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t1.rel_related_paper_revisions = [pve1_1, pve1_2, pve1_3, pve8]
    db.session.add(t1)

    t2 = Tag(
        name="Electromagnetics",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t2.rel_related_paper_revisions = [pve2_1, pve9]
    db.session.add(t2)

    t3 = Tag(
        name="Thermodynamics",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t3.rel_related_paper_revisions = [pve3, pve10]
    db.session.add(t3)

    t4 = Tag(
        name="Kinetics",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t4.rel_related_paper_revisions = [pve4, pve11]
    db.session.add(t4)

    t5 = Tag(
        name="Chemistry",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t5.rel_related_paper_revisions = [pve5, pve12]
    db.session.add(t5)

    t6 = Tag(
        name="Inorganic_Chemistry",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t6.rel_related_paper_revisions = [pve6, pve13]
    db.session.add(t6)

    t7 = Tag(
        name="Electrochemistry",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t7.rel_related_paper_revisions = [pve7, pve14]
    db.session.add(t7)

    t8 = Tag(
        name="Analytical_Chemistry",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t8.rel_related_paper_revisions = [pve8, pve15_1, pve15_2]
    db.session.add(t8)

    t9 = Tag(
        name="Earth_Sciences",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t9.rel_related_paper_revisions = [pve9, pve1_1, pve1_2, pve1_3]
    db.session.add(t9)

    t10 = Tag(
        name="Anatomy",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t10.rel_related_paper_revisions = [pve10, pve2_1]
    db.session.add(t10)

    t11 = Tag(
        name="Botany",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t11.rel_related_paper_revisions = [pve11, pve3]
    db.session.add(t11)

    t12 = Tag(
        name="Biology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t12.rel_related_paper_revisions = [pve12, pve4]
    db.session.add(t12)

    t13 = Tag(
        name="Zoology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t13.rel_related_paper_revisions = [pve13, pve5]
    db.session.add(t13)

    t14 = Tag(
        name="Neurobiology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t14.rel_related_paper_revisions = [pve14, pve6]
    db.session.add(t14)

    t15 = Tag(
        name="Marine_Biology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t15.rel_related_paper_revisions = [pve15_1, pve15_2, pve7]
    db.session.add(t15)

    t16 = Tag(
        name="Embryology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t16.rel_related_paper_revisions = [pve1_1, pve1_2, pve1_3, pve8]
    db.session.add(t16)

    t17 = Tag(
        name="Ecology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t17.rel_related_paper_revisions = [pve2_1, pve9]
    db.session.add(t17)

    t18 = Tag(
        name="Paleontology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t18.rel_related_paper_revisions = [pve3, pve10]
    db.session.add(t18)

    t19 = Tag(
        name="Genetics",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t19.rel_related_paper_revisions = [pve4, pve11]
    db.session.add(t19)

    t20 = Tag(
        name="Cell_Biology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t20.rel_related_paper_revisions = [pve5, pve12]
    db.session.add(t20)

    t21 = Tag(
        name="Ethology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t21.rel_related_paper_revisions = [pve6, pve13]
    db.session.add(t21)

    t22 = Tag(
        name="Astronomy",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t22.rel_related_paper_revisions = [pve7, pve14]
    db.session.add(t22)

    t23 = Tag(
        name="Meteorology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t23.rel_related_paper_revisions = [pve8, pve15_1, pve15_2]
    db.session.add(t23)

    t24 = Tag(
        name="Geology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t24.rel_related_paper_revisions = [pve9, pve1_1, pve1_2, pve1_3]
    db.session.add(t24)

    t25 = Tag(
        name="Atmospheric_Sciences",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t25.rel_related_paper_revisions = [pve10, pve2_1]
    db.session.add(t25)

    t26 = Tag(
        name="Glaciology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t26.rel_related_paper_revisions = [pve11, pve3]
    db.session.add(t26)

    t27 = Tag(
        name="Climatology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t27.rel_related_paper_revisions = [pve12, pve4]
    db.session.add(t27)

    t28 = Tag(
        name="Structural_Geology",
        description="In orci lectus, convallis et velit at, ultrices rhoncus ante",
        creation_date=dt.datetime(2020, 1, 17, 1, 1, 1, 1),
        deadline=dt.datetime(2023, 1, 17, 1, 1, 1, 1),
    )
    t28.rel_related_paper_revisions = [pve13, pve5]
    db.session.add(t28)

    # users
    u1 = User(
        first_name="Shayla",
        second_name="Jackson",
        email="shayla.jackson@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2),
        affiliation="university",
        orcid="0000000218250091",
        google_scholar="https://scholar.google.com/profil1",
        about_me="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut mauris dui, posuere in purus vitae, "
                 "tristique elementum mi. Quisque maximus nunc ante, et interdum purus condimentum tincidunt. Ut eu "
                 "magna eget enim viverra maximus. Nulla non rhoncus odio, id ullamcorper lectus. Proin quis ligula "
                 "pretium, hendrerit erat non, rutrum enim. Pellentesque aliquam suscipit magna, vel ultrices ligula "
                 "feugiat vitae. Sed lacinia mauris vitae turpis hendrerit, vel luctus arcu sagittis. Pellentesque "
                 "habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus sit amet "
                 "libero eleifend, consequat justo nec, hendrerit risus. Vestibulum condimentum nec ex vel "
                 "consectetur. Duis in ipsum sit amet tellus rhoncus gravida sed ut magna. Suspendisse facilisis "
                 "vulputate pellentesque.",
        personal_website="https://personalwebsite1.com",
        review_mails_limit=1,
        notifications_frequency=7,
        last_seen=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        weight=1.1,
        registered_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2)
    )
    u1.rel_created_paper_revisions = [pve1_1, pve1_2, pve1_3, pve2_1, pve6, pve11]
    u1.rel_tags_to_user = [t1, t2, t3, t4]
    u1.rel_created_tags = [t11, t12, t13, t14]
    u1.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.RESEARCHER_USER.value).first()
    u1.rel_created_reviews = [r15, r20, r25, r30, r35, r40]
    u1.rel_created_comments = [c1, c8, c16, c23, c31, c38, c46, c53, c61, c68, c76, c83,
                               c91, c98, c106, c113, c121, c128, c136, c143, c151, c158, c166]
    db.session.add(u1)

    p1.rel_creators = [u1]
    p2.rel_creators = [u1]
    p4.rel_creators = [u1]
    p5.rel_creators = [u1]
    p6.rel_creators = [u1]
    p8.rel_creators = [u1]
    p9.rel_creators = [u1]
    p10.rel_creators = [u1]

    u2 = User(
        first_name="Oakley",
        second_name="Muir",
        email="oakley.muir@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2),
        affiliation="college",
        orcid="0000000218250092",
        google_scholar="https://scholar.google.com/profil2",
        about_me="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut mauris dui, posuere in purus vitae, "
                 "tristique elementum mi. Quisque maximus nunc ante, et interdum purus condimentum tincidunt. Ut eu "
                 "magna eget enim viverra maximus. Nulla non rhoncus odio, id ullamcorper lectus. Proin quis ligula "
                 "pretium, hendrerit erat non, rutrum enim. Pellentesque aliquam suscipit magna, vel ultrices ligula "
                 "feugiat vitae. Sed lacinia mauris vitae turpis hendrerit, vel luctus arcu sagittis. Pellentesque "
                 "habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus sit amet "
                 "libero eleifend, consequat justo nec, hendrerit risus. Vestibulum condimentum nec ex vel "
                 "consectetur. Duis in ipsum sit amet tellus rhoncus gravida sed ut magna. Suspendisse facilisis "
                 "vulputate pellentesque.",
        personal_website="https://personalwebsite2.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=2.2,
        registered_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2)
    )
    u2.rel_created_paper_revisions = [pve2_1, pve7, pve12]
    u2.rel_tags_to_user = [t5, t6, t7, t8]
    u2.rel_created_tags = [t15, t16, t17, t18]
    u2.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.RESEARCHER_USER.value).first()
    u2.rel_created_reviews = [r1, r5, r9, r16, r21, r26, r31, r36]
    u2.rel_created_comments = [c2, c10, c17, c25, c32, c40, c47, c55, c62, c70, c77, c85,
                               c92, c100, c107, c115, c122, c130, c137, c145, c152, c160, c167]
    db.session.add(u2)

    p3.rel_creators = [u2]
    p10.rel_creators = [u2]
    p11.rel_creators = [u1, u2]

    u3 = User(
        first_name="Rafael",
        second_name="Carson",
        email="rafael.carson@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2),
        affiliation="company",
        orcid="0000000218250093",
        google_scholar="https://scholar.google.com/profil3",
        about_me="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut mauris dui, posuere in purus vitae, "
                 "tristique elementum mi. Quisque maximus nunc ante, et interdum purus condimentum tincidunt. Ut eu "
                 "magna eget enim viverra maximus. Nulla non rhoncus odio, id ullamcorper lectus. Proin quis ligula "
                 "pretium, hendrerit erat non, rutrum enim. Pellentesque aliquam suscipit magna, vel ultrices ligula "
                 "feugiat vitae. Sed lacinia mauris vitae turpis hendrerit, vel luctus arcu sagittis. Pellentesque "
                 "habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus sit amet "
                 "libero eleifend, consequat justo nec, hendrerit risus. Vestibulum condimentum nec ex vel "
                 "consectetur. Duis in ipsum sit amet tellus rhoncus gravida sed ut magna. Suspendisse facilisis "
                 "vulputate pellentesque.",
        personal_website="https://personalwebsite3.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=3.3,
        registered_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2)
    )
    u3.rel_created_paper_revisions = [pve2_1, pve3, pve8, pve13]
    u3.rel_tags_to_user = [t9, t10, t11, t12]
    u3.rel_created_tags = [t19, t20, t21, t22]
    u3.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.RESEARCHER_USER.value).first()
    u3.rel_created_reviews = [r2, r6, r10, r17, r22, r27, r32, r37]
    u3.rel_created_comments = [c4, c11, c19, c26, c34, c41, c49, c56, c64, c71, c79, c86,
                               c94, c101, c109, c116, c124, c131, c139, c146, c154, c161, c169]
    db.session.add(u3)

    u4 = User(
        first_name="Sylvia",
        second_name="Osborne",
        email="sylvia.osborne@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2),
        affiliation="college",
        orcid="0000000218250094",
        google_scholar="https://scholar.google.com/profil4",
        about_me="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut mauris dui, posuere in purus vitae, "
                 "tristique elementum mi. Quisque maximus nunc ante, et interdum purus condimentum tincidunt. Ut eu "
                 "magna eget enim viverra maximus. Nulla non rhoncus odio, id ullamcorper lectus. Proin quis ligula "
                 "pretium, hendrerit erat non, rutrum enim. Pellentesque aliquam suscipit magna, vel ultrices ligula "
                 "feugiat vitae. Sed lacinia mauris vitae turpis hendrerit, vel luctus arcu sagittis. Pellentesque "
                 "habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus sit amet "
                 "libero eleifend, consequat justo nec, hendrerit risus. Vestibulum condimentum nec ex vel "
                 "consectetur. Duis in ipsum sit amet tellus rhoncus gravida sed ut magna. Suspendisse facilisis "
                 "vulputate pellentesque.",
        personal_website="https://personalwebsite4.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=3.3,
        registered_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2)
    )
    u4.rel_created_paper_revisions = [pve4, pve9, pve14]
    u4.rel_tags_to_user = [t13, t14, t15, t16]
    u4.rel_created_tags = [t23, t24, t25, t26]
    u4.rel_created_comments = [c5, c13, c20, c28, c35, c43, c50, c58, c65, c73, c80, c88,
                               c95, c103, c110, c118, c125, c133, c140, c148, c155, c163, c170]
    u4.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.RESEARCHER_USER.value).first()
    u4.rel_created_reviews = [r3, r7, r11, r13, r19, r23, r29, r33, r39]
    db.session.add(u4)

    u5 = User(
        first_name="Kerys",
        second_name="Campbell",
        email="kerys.campbell@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2),
        affiliation="company",
        orcid="0000000218250095",
        google_scholar="https://scholar.google.com/profil5",
        about_me="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut mauris dui, posuere in purus vitae, "
                 "tristique elementum mi. Quisque maximus nunc ante, et interdum purus condimentum tincidunt. Ut eu "
                 "magna eget enim viverra maximus. Nulla non rhoncus odio, id ullamcorper lectus. Proin quis ligula "
                 "pretium, hendrerit erat non, rutrum enim. Pellentesque aliquam suscipit magna, vel ultrices ligula "
                 "feugiat vitae. Sed lacinia mauris vitae turpis hendrerit, vel luctus arcu sagittis. Pellentesque "
                 "habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus sit amet "
                 "libero eleifend, consequat justo nec, hendrerit risus. Vestibulum condimentum nec ex vel "
                 "consectetur. Duis in ipsum sit amet tellus rhoncus gravida sed ut magna. Suspendisse facilisis "
                 "vulputate pellentesque.",
        personal_website="https://personalwebsite5.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=3.3,
        registered_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2)
    )
    u5.rel_created_paper_revisions = [pve5, pve10, pve15_1, pve15_2]
    u5.rel_tags_to_user = [t17, t18, t19, t20]
    u5.rel_created_tags = [t27, t28, t1]
    u5.rel_created_comments = [c7, c14, c22, c29, c37, c44, c52, c59, c67, c74, c82, c89,
                               c97, c104, c112, c119, c127, c134, c142, c149, c157, c164]
    u5.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.RESEARCHER_USER.value).first()
    u5.rel_created_reviews = [r4, r8, r12, r14, r18, r24, r28, r34, r38]
    db.session.add(u5)

    u6 = User(
        first_name="Dustin",
        second_name="Velazquez",
        email="dustin.velazquez@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=False,
        affiliation="",
        orcid="",
        google_scholar="",
        about_me="",
        personal_website="",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=4.4,
        registered_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2)
    )
    u6.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.STANDARD_USER.value).first()
    u6.rel_created_comments = [c3, c12, c21, c30, c39, c48, c57, c66, c75, c84,
                               c93, c102, c111, c120, c129, c138, c147, c156, c165]
    db.session.add(u6)

    u7 = User(
        first_name="admin_name",
        second_name="admin_second_name",
        email="email7@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2),
        affiliation="",
        orcid="",
        google_scholar="",
        about_me="",
        personal_website="",
        review_mails_limit=0,
        notifications_frequency=0,
        weight=5.5,
        registered_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2)
    )
    u7.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.ADMIN.value).first()
    db.session.add(u7)

    u8 = User(
        first_name="Shannon",
        second_name="Major",
        email="shannon.major@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2),
        affiliation="university",
        orcid="0000000218250096",
        google_scholar="https://scholar.google.com/profil5",
        about_me="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut mauris dui, posuere in purus vitae, "
                 "tristique elementum mi. Quisque maximus nunc ante, et interdum purus condimentum tincidunt. Ut eu "
                 "magna eget enim viverra maximus. Nulla non rhoncus odio, id ullamcorper lectus. Proin quis ligula "
                 "pretium, hendrerit erat non, rutrum enim. Pellentesque aliquam suscipit magna, vel ultrices ligula "
                 "feugiat vitae. Sed lacinia mauris vitae turpis hendrerit, vel luctus arcu sagittis. Pellentesque "
                 "habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus sit amet "
                 "libero eleifend, consequat justo nec, hendrerit risus. Vestibulum condimentum nec ex vel "
                 "consectetur. Duis in ipsum sit amet tellus rhoncus gravida sed ut magna. Suspendisse facilisis "
                 "vulputate pellentesque.",
        personal_website="https://personalwebsite5.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=3.3,
        registered_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2)
    )
    u8.rel_tags_to_user = [t21, t22, t23, t24]
    u8.rel_created_tags = [t2, t3, t4]
    u8.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.STANDARD_USER.value).first()
    db.session.add(u8)

    u9 = User(
        first_name="Jane",
        second_name="Orozco",
        email="jane.orozco@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2),
        affiliation="college",
        orcid="0000000218250097",
        google_scholar="https://scholar.google.com/profil5",
        about_me="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut mauris dui, posuere in purus vitae, "
                 "tristique elementum mi. Quisque maximus nunc ante, et interdum purus condimentum tincidunt. Ut eu "
                 "magna eget enim viverra maximus. Nulla non rhoncus odio, id ullamcorper lectus. Proin quis ligula "
                 "pretium, hendrerit erat non, rutrum enim. Pellentesque aliquam suscipit magna, vel ultrices ligula "
                 "feugiat vitae. Sed lacinia mauris vitae turpis hendrerit, vel luctus arcu sagittis. Pellentesque "
                 "habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus sit amet "
                 "libero eleifend, consequat justo nec, hendrerit risus. Vestibulum condimentum nec ex vel "
                 "consectetur. Duis in ipsum sit amet tellus rhoncus gravida sed ut magna. Suspendisse facilisis "
                 "vulputate pellentesque.",
        personal_website="https://personalwebsite5.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=3.3,
        registered_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2)
    )
    u9.rel_tags_to_user = [t25, t26, t27, t28]
    u9.rel_created_tags = [t5, t6, t7]
    u9.rel_created_comments = [c6, c15, c24, c33, c42, c51, c60, c69, c78, c87,
                               c96, c105, c114, c123, c132, c141, c150, c159, c168]
    u9.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.STANDARD_USER.value).first()
    db.session.add(u9)

    u10 = User(
        first_name="Veronika",
        second_name="Alvarado",
        email="veronika.alvarado@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2),
        affiliation="company",
        orcid="0000000218250098",
        google_scholar="https://scholar.google.com/profil5",
        about_me="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut mauris dui, posuere in purus vitae, "
                 "tristique elementum mi. Quisque maximus nunc ante, et interdum purus condimentum tincidunt. Ut eu "
                 "magna eget enim viverra maximus. Nulla non rhoncus odio, id ullamcorper lectus. Proin quis ligula "
                 "pretium, hendrerit erat non, rutrum enim. Pellentesque aliquam suscipit magna, vel ultrices ligula "
                 "feugiat vitae. Sed lacinia mauris vitae turpis hendrerit, vel luctus arcu sagittis. Pellentesque "
                 "habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus sit amet "
                 "libero eleifend, consequat justo nec, hendrerit risus. Vestibulum condimentum nec ex vel "
                 "consectetur. Duis in ipsum sit amet tellus rhoncus gravida sed ut magna. Suspendisse facilisis "
                 "vulputate pellentesque.",
        personal_website="https://personalwebsite5.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=3.3,
        registered_on=dt.datetime(2020, 7, 1, 2, 2, 2, 2)
    )
    u10.rel_tags_to_user = [t1, t2, t3, t4]
    u10.rel_created_tags = [t8, t9, t10]
    u10.rel_created_comments = [c9, c18, c27, c36, c45, c54, c63, c72, c81, c90,
                                c99, c108, c117, c126, c135, c144, c153, c162, c171]
    u10.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.STANDARD_USER.value).first()
    db.session.add(u10)

    # review requests
    rr1 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 1, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 2),
        deadline_date=dt.date(2020, 9, 1),
    )
    rr1.rel_requested_user = u2
    rr1.rel_related_paper_version = pve1_1
    db.session.add(rr1)

    rr2 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 2, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 2),
        deadline_date=dt.date(2020, 9, 2),
    )
    rr2.rel_requested_user = u3
    rr2.rel_related_paper_version = pve1_1
    db.session.add(rr2)

    rr3 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 3, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 4),
        deadline_date=dt.date(2020, 9, 3),
    )
    rr3.rel_requested_user = u4
    rr3.rel_related_paper_version = pve1_1
    db.session.add(rr3)

    rr4 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 4, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 5),
        deadline_date=dt.date(2020, 9, 4),
    )
    rr4.rel_requested_user = u5
    rr4.rel_related_paper_version = pve1_1
    db.session.add(rr4)

    rr5 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 5, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 6),
        deadline_date=dt.date(2020, 9, 5),
    )
    rr5.rel_requested_user = u2
    rr5.rel_related_paper_version = pve1_2
    db.session.add(rr5)

    rr6 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 6, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 7),
        deadline_date=dt.date(2020, 9, 6),
    )
    rr6.rel_requested_user = u3
    rr6.rel_related_paper_version = pve1_2
    db.session.add(rr6)

    rr7 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 7, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 8),
        deadline_date=dt.date(2020, 9, 7),
    )
    rr7.rel_requested_user = u4
    rr7.rel_related_paper_version = pve1_2
    db.session.add(rr7)

    rr8 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 8, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 9),
        deadline_date=dt.date(2020, 9, 8),
    )
    rr8.rel_requested_user = u5
    rr8.rel_related_paper_version = pve1_2
    db.session.add(rr8)

    rr9 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 9, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 10),
        deadline_date=dt.date(2020, 9, 9),
    )
    rr9.rel_requested_user = u2
    rr9.rel_related_paper_version = pve1_3
    db.session.add(rr9)

    rr10 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 10, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 11),
        deadline_date=dt.date(2020, 9, 10),
    )
    rr10.rel_requested_user = u3
    rr10.rel_related_paper_version = pve1_3
    db.session.add(rr10)

    rr11 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 11, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 12),
        deadline_date=dt.date(2020, 9, 11),
    )
    rr11.rel_requested_user = u4
    rr11.rel_related_paper_version = pve1_3
    db.session.add(rr11)

    rr12 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 12, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 13),
        deadline_date=dt.date(2020, 9, 12),
    )
    rr12.rel_requested_user = u5
    rr12.rel_related_paper_version = pve1_3
    db.session.add(rr12)

    rr13 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 13, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 14),
        deadline_date=dt.date(2020, 9, 13),
    )
    rr13.rel_requested_user = u4
    rr13.rel_related_paper_version = pve2_1
    db.session.add(rr13)

    rr14 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 14, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 15),
        deadline_date=dt.date(2020, 9, 14),
    )
    rr14.rel_requested_user = u5
    rr14.rel_related_paper_version = pve2_1
    db.session.add(rr14)

    rr15 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 15, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 16),
        deadline_date=dt.date(2020, 9, 15),
    )
    rr15.rel_requested_user = u1
    rr15.rel_related_paper_version = pve3
    db.session.add(rr15)

    rr16 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 16, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 17),
        deadline_date=dt.date(2020, 9, 16),
    )
    rr16.rel_requested_user = u2
    rr16.rel_related_paper_version = pve3
    db.session.add(rr16)

    rr17 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 17, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 18),
        deadline_date=dt.date(2020, 9, 17),
    )
    rr17.rel_requested_user = u3
    rr17.rel_related_paper_version = pve4
    db.session.add(rr17)

    rr18 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 18, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 19),
        deadline_date=dt.date(2020, 9, 18),
    )
    rr18.rel_requested_user = u5
    rr18.rel_related_paper_version = pve4
    db.session.add(rr18)

    rr19 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 19, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 20),
        deadline_date=dt.date(2020, 9, 19),
    )
    rr19.rel_requested_user = u4
    rr19.rel_related_paper_version = pve5
    db.session.add(rr19)

    rr20 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 20, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 21),
        deadline_date=dt.date(2020, 9, 20),
    )
    rr20.rel_requested_user = u1
    rr20.rel_related_paper_version = pve5
    db.session.add(rr20)

    rr21 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 21, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 22),
        deadline_date=dt.date(2020, 9, 21),
    )
    rr21.rel_requested_user = u2
    rr21.rel_related_paper_version = pve6
    db.session.add(rr21)

    rr22 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 22, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 23),
        deadline_date=dt.date(2020, 9, 22),
    )
    rr22.rel_requested_user = u3
    rr22.rel_related_paper_version = pve6
    db.session.add(rr22)

    rr23 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 23, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 24),
        deadline_date=dt.date(2020, 9, 23),
    )
    rr23.rel_requested_user = u4
    rr23.rel_related_paper_version = pve7
    db.session.add(rr23)

    rr24 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 24, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 25),
        deadline_date=dt.date(2020, 9, 24),
    )
    rr24.rel_requested_user = u5
    rr24.rel_related_paper_version = pve7
    db.session.add(rr24)

    rr25 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 25, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 26),
        deadline_date=dt.date(2020, 9, 25),
    )
    rr25.rel_requested_user = u1
    rr25.rel_related_paper_version = pve8
    db.session.add(rr25)

    rr26 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 26, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 27),
        deadline_date=dt.date(2020, 9, 26),
    )
    rr26.rel_requested_user = u2
    rr26.rel_related_paper_version = pve8
    db.session.add(rr26)

    rr27 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 27, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 28),
        deadline_date=dt.date(2020, 9, 27),
    )
    rr27.rel_requested_user = u3
    rr27.rel_related_paper_version = pve9
    db.session.add(rr27)

    rr28 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 28, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 29),
        deadline_date=dt.date(2020, 9, 28),
    )
    rr28.rel_requested_user = u5
    rr28.rel_related_paper_version = pve9
    db.session.add(rr28)

    rr29 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 29, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 30),
        deadline_date=dt.date(2020, 9, 29),
    )
    rr29.rel_requested_user = u4
    rr29.rel_related_paper_version = pve10
    db.session.add(rr29)

    rr30 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 30, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 31),
        deadline_date=dt.date(2020, 9, 30),
    )
    rr30.rel_requested_user = u1
    rr30.rel_related_paper_version = pve10
    db.session.add(rr30)

    rr31 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 31, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 9, 1),
        deadline_date=dt.date(2020, 9, 30),
    )
    rr31.rel_requested_user = u2
    rr31.rel_related_paper_version = pve11
    db.session.add(rr31)

    rr32 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 9, 2),
        deadline_date=dt.date(2020, 10, 1),
    )
    rr32.rel_requested_user = u3
    rr32.rel_related_paper_version = pve11
    db.session.add(rr32)

    rr33 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 2, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 9, 3),
        deadline_date=dt.date(2020, 10, 2),
    )
    rr33.rel_requested_user = u4
    rr33.rel_related_paper_version = pve12
    db.session.add(rr33)

    rr34 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 3, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 9, 4),
        deadline_date=dt.date(2020, 10, 3),
    )
    rr34.rel_requested_user = u5
    rr34.rel_related_paper_version = pve12
    db.session.add(rr34)

    rr35 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 4, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 9, 5),
        deadline_date=dt.date(2020, 10, 4),
    )
    rr35.rel_requested_user = u1
    rr35.rel_related_paper_version = pve13
    db.session.add(rr35)

    rr36 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 5, 2, 2, 2, 2),
        deadline_date=dt.date(2020, 10, 5),
    )
    rr36.rel_requested_user = u2
    rr36.rel_related_paper_version = pve13
    db.session.add(rr36)

    rr37 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 6, 2, 2, 2, 2),
        deadline_date=dt.date(2020, 10, 6),
    )
    rr37.rel_requested_user = u3
    rr37.rel_related_paper_version = pve14
    db.session.add(rr37)

    rr38 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 7, 2, 2, 2, 2),
        deadline_date=dt.date(2020, 10, 7),
    )
    rr38.rel_requested_user = u5
    rr38.rel_related_paper_version = pve14
    db.session.add(rr38)

    rr39 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 8, 2, 2, 2, 2),
        deadline_date=dt.date(2020, 10, 8),
    )
    rr39.rel_requested_user = u4
    rr39.rel_related_paper_version = pve15_1
    db.session.add(rr39)

    rr40 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 9, 2, 2, 2, 2),
        deadline_date=dt.date(2020, 10, 9),
    )
    rr40.rel_requested_user = u1
    rr40.rel_related_paper_version = pve15_1
    db.session.add(rr40)

    rr41 = ReviewRequest(
        decision=False,
        creation_datetime=dt.datetime(2020, 9, 10, 2, 2, 2, 2),
        deadline_date=dt.date(2020, 10, 10),
        reason_conflict_interest=True,
        reason_lack_expertise=True,
    )
    rr41.rel_requested_user = u1
    rr41.rel_related_paper_version = pve15_1
    db.session.add(rr41)

    rr42 = ReviewRequest(
        creation_datetime=dt.datetime(2020, 9, 10, 2, 2, 2, 2),
        deadline_date=dt.date(2020, 10, 10)
    )
    rr42.rel_requested_user = u1
    rr42.rel_related_paper_version = pve2_2
    db.session.add(rr42)

    rr43 = ReviewRequest(
        creation_datetime=dt.datetime(2020, 9, 10, 2, 2, 2, 2),
        deadline_date=dt.date(2020, 10, 10)
    )
    rr43.rel_requested_user = u2
    rr43.rel_related_paper_version = pve2_2
    db.session.add(rr43)

    rr44 = ReviewRequest(
        creation_datetime=dt.datetime(2020, 9, 10, 2, 2, 2, 2),
        deadline_date=dt.date(2020, 10, 10)
    )
    rr44.rel_requested_user = u3
    rr44.rel_related_paper_version = pve2_2
    db.session.add(rr44)

    # comments votes
    # comments votes
    vc1 = VoteComment(
            is_up=False
        )
    vc1.rel_creator = u8
    vc1.rel_to_comment = c1
    db.session.add(vc1)

    vc2 = VoteComment(
            is_up=True
        )
    vc2.rel_creator = u9
    vc2.rel_to_comment = c1
    db.session.add(vc2)

    vc3 = VoteComment(
            is_up=True
        )
    vc3.rel_creator = u10
    vc3.rel_to_comment = c1
    db.session.add(vc3)

    vc4 = VoteComment(
            is_up=True
        )
    vc4.rel_creator = u8
    vc4.rel_to_comment = c2
    db.session.add(vc4)

    vc5 = VoteComment(
            is_up=False
        )
    vc5.rel_creator = u9
    vc5.rel_to_comment = c2
    db.session.add(vc5)

    vc6 = VoteComment(
            is_up=True
        )
    vc6.rel_creator = u10
    vc6.rel_to_comment = c2
    db.session.add(vc6)

    vc7 = VoteComment(
            is_up=False
        )
    vc7.rel_creator = u1
    vc7.rel_to_comment = c3
    db.session.add(vc7)

    vc8 = VoteComment(
            is_up=True
        )
    vc8.rel_creator = u2
    vc8.rel_to_comment = c3
    db.session.add(vc8)

    vc9 = VoteComment(
            is_up=False
        )
    vc9.rel_creator = u3
    vc9.rel_to_comment = c3
    db.session.add(vc9)

    vc10 = VoteComment(
            is_up=False
        )
    vc10.rel_creator = u8
    vc10.rel_to_comment = c4
    db.session.add(vc10)

    vc11 = VoteComment(
            is_up=True
        )
    vc11.rel_creator = u9
    vc11.rel_to_comment = c4
    db.session.add(vc11)

    vc12 = VoteComment(
            is_up=False
        )
    vc12.rel_creator = u10
    vc12.rel_to_comment = c4
    db.session.add(vc12)

    vc13 = VoteComment(
            is_up=False
        )
    vc13.rel_creator = u8
    vc13.rel_to_comment = c5
    db.session.add(vc13)

    vc14 = VoteComment(
            is_up=True
        )
    vc14.rel_creator = u9
    vc14.rel_to_comment = c5
    db.session.add(vc14)

    vc15 = VoteComment(
            is_up=True
        )
    vc15.rel_creator = u10
    vc15.rel_to_comment = c5
    db.session.add(vc15)

    vc16 = VoteComment(
            is_up=True
        )
    vc16.rel_creator = u1
    vc16.rel_to_comment = c6
    db.session.add(vc16)

    vc17 = VoteComment(
            is_up=False
        )
    vc17.rel_creator = u2
    vc17.rel_to_comment = c6
    db.session.add(vc17)

    vc18 = VoteComment(
            is_up=True
        )
    vc18.rel_creator = u3
    vc18.rel_to_comment = c6
    db.session.add(vc18)

    vc19 = VoteComment(
            is_up=True
        )
    vc19.rel_creator = u8
    vc19.rel_to_comment = c7
    db.session.add(vc19)

    vc20 = VoteComment(
            is_up=True
        )
    vc20.rel_creator = u9
    vc20.rel_to_comment = c7
    db.session.add(vc20)

    vc21 = VoteComment(
            is_up=False
        )
    vc21.rel_creator = u10
    vc21.rel_to_comment = c7
    db.session.add(vc21)

    vc22 = VoteComment(
            is_up=False
        )
    vc22.rel_creator = u8
    vc22.rel_to_comment = c8
    db.session.add(vc22)

    vc23 = VoteComment(
            is_up=False
        )
    vc23.rel_creator = u9
    vc23.rel_to_comment = c8
    db.session.add(vc23)

    vc24 = VoteComment(
            is_up=True
        )
    vc24.rel_creator = u10
    vc24.rel_to_comment = c8
    db.session.add(vc24)

    vc25 = VoteComment(
            is_up=True
        )
    vc25.rel_creator = u1
    vc25.rel_to_comment = c9
    db.session.add(vc25)

    vc26 = VoteComment(
            is_up=True
        )
    vc26.rel_creator = u2
    vc26.rel_to_comment = c9
    db.session.add(vc26)

    vc27 = VoteComment(
            is_up=False
        )
    vc27.rel_creator = u3
    vc27.rel_to_comment = c9
    db.session.add(vc27)

    vc28 = VoteComment(
            is_up=True
        )
    vc28.rel_creator = u8
    vc28.rel_to_comment = c10
    db.session.add(vc28)

    vc29 = VoteComment(
            is_up=True
        )
    vc29.rel_creator = u9
    vc29.rel_to_comment = c10
    db.session.add(vc29)

    vc30 = VoteComment(
            is_up=True
        )
    vc30.rel_creator = u10
    vc30.rel_to_comment = c10
    db.session.add(vc30)

    vc31 = VoteComment(
            is_up=True
        )
    vc31.rel_creator = u8
    vc31.rel_to_comment = c11
    db.session.add(vc31)

    vc32 = VoteComment(
            is_up=True
        )
    vc32.rel_creator = u9
    vc32.rel_to_comment = c11
    db.session.add(vc32)

    vc33 = VoteComment(
            is_up=False
        )
    vc33.rel_creator = u10
    vc33.rel_to_comment = c11
    db.session.add(vc33)

    vc34 = VoteComment(
            is_up=True
        )
    vc34.rel_creator = u1
    vc34.rel_to_comment = c12
    db.session.add(vc34)

    vc35 = VoteComment(
            is_up=True
        )
    vc35.rel_creator = u2
    vc35.rel_to_comment = c12
    db.session.add(vc35)

    vc36 = VoteComment(
            is_up=True
        )
    vc36.rel_creator = u3
    vc36.rel_to_comment = c12
    db.session.add(vc36)

    vc37 = VoteComment(
            is_up=True
        )
    vc37.rel_creator = u8
    vc37.rel_to_comment = c13
    db.session.add(vc37)

    vc38 = VoteComment(
            is_up=False
        )
    vc38.rel_creator = u9
    vc38.rel_to_comment = c13
    db.session.add(vc38)

    vc39 = VoteComment(
            is_up=True
        )
    vc39.rel_creator = u10
    vc39.rel_to_comment = c13
    db.session.add(vc39)

    vc40 = VoteComment(
            is_up=False
        )
    vc40.rel_creator = u8
    vc40.rel_to_comment = c14
    db.session.add(vc40)

    vc41 = VoteComment(
            is_up=True
        )
    vc41.rel_creator = u9
    vc41.rel_to_comment = c14
    db.session.add(vc41)

    vc42 = VoteComment(
            is_up=True
        )
    vc42.rel_creator = u10
    vc42.rel_to_comment = c14
    db.session.add(vc42)

    vc43 = VoteComment(
            is_up=False
        )
    vc43.rel_creator = u1
    vc43.rel_to_comment = c15
    db.session.add(vc43)

    vc44 = VoteComment(
            is_up=False
        )
    vc44.rel_creator = u2
    vc44.rel_to_comment = c15
    db.session.add(vc44)

    vc45 = VoteComment(
            is_up=False
        )
    vc45.rel_creator = u3
    vc45.rel_to_comment = c15
    db.session.add(vc45)

    vc46 = VoteComment(
            is_up=True
        )
    vc46.rel_creator = u8
    vc46.rel_to_comment = c16
    db.session.add(vc46)

    vc47 = VoteComment(
            is_up=False
        )
    vc47.rel_creator = u9
    vc47.rel_to_comment = c16
    db.session.add(vc47)

    vc48 = VoteComment(
            is_up=True
        )
    vc48.rel_creator = u10
    vc48.rel_to_comment = c16
    db.session.add(vc48)

    vc49 = VoteComment(
            is_up=True
        )
    vc49.rel_creator = u8
    vc49.rel_to_comment = c17
    db.session.add(vc49)

    vc50 = VoteComment(
            is_up=False
        )
    vc50.rel_creator = u9
    vc50.rel_to_comment = c17
    db.session.add(vc50)

    vc51 = VoteComment(
            is_up=True
        )
    vc51.rel_creator = u10
    vc51.rel_to_comment = c17
    db.session.add(vc51)

    vc52 = VoteComment(
            is_up=True
        )
    vc52.rel_creator = u1
    vc52.rel_to_comment = c18
    db.session.add(vc52)

    vc53 = VoteComment(
            is_up=False
        )
    vc53.rel_creator = u2
    vc53.rel_to_comment = c18
    db.session.add(vc53)

    vc54 = VoteComment(
            is_up=False
        )
    vc54.rel_creator = u3
    vc54.rel_to_comment = c18
    db.session.add(vc54)

    vc55 = VoteComment(
            is_up=False
        )
    vc55.rel_creator = u8
    vc55.rel_to_comment = c19
    db.session.add(vc55)

    vc56 = VoteComment(
            is_up=False
        )
    vc56.rel_creator = u9
    vc56.rel_to_comment = c19
    db.session.add(vc56)

    vc57 = VoteComment(
            is_up=False
        )
    vc57.rel_creator = u10
    vc57.rel_to_comment = c19
    db.session.add(vc57)

    vc58 = VoteComment(
            is_up=True
        )
    vc58.rel_creator = u8
    vc58.rel_to_comment = c20
    db.session.add(vc58)

    vc59 = VoteComment(
            is_up=True
        )
    vc59.rel_creator = u9
    vc59.rel_to_comment = c20
    db.session.add(vc59)

    vc60 = VoteComment(
            is_up=False
        )
    vc60.rel_creator = u10
    vc60.rel_to_comment = c20
    db.session.add(vc60)

    vc61 = VoteComment(
            is_up=True
        )
    vc61.rel_creator = u1
    vc61.rel_to_comment = c21
    db.session.add(vc61)

    vc62 = VoteComment(
            is_up=True
        )
    vc62.rel_creator = u2
    vc62.rel_to_comment = c21
    db.session.add(vc62)

    vc63 = VoteComment(
            is_up=True
        )
    vc63.rel_creator = u3
    vc63.rel_to_comment = c21
    db.session.add(vc63)

    vc64 = VoteComment(
            is_up=True
        )
    vc64.rel_creator = u8
    vc64.rel_to_comment = c22
    db.session.add(vc64)

    vc65 = VoteComment(
            is_up=False
        )
    vc65.rel_creator = u9
    vc65.rel_to_comment = c22
    db.session.add(vc65)

    vc66 = VoteComment(
            is_up=True
        )
    vc66.rel_creator = u10
    vc66.rel_to_comment = c22
    db.session.add(vc66)

    vc67 = VoteComment(
            is_up=True
        )
    vc67.rel_creator = u8
    vc67.rel_to_comment = c23
    db.session.add(vc67)

    vc68 = VoteComment(
            is_up=True
        )
    vc68.rel_creator = u9
    vc68.rel_to_comment = c23
    db.session.add(vc68)

    vc69 = VoteComment(
            is_up=True
        )
    vc69.rel_creator = u10
    vc69.rel_to_comment = c23
    db.session.add(vc69)

    vc70 = VoteComment(
            is_up=False
        )
    vc70.rel_creator = u1
    vc70.rel_to_comment = c24
    db.session.add(vc70)

    vc71 = VoteComment(
            is_up=True
        )
    vc71.rel_creator = u2
    vc71.rel_to_comment = c24
    db.session.add(vc71)

    vc72 = VoteComment(
            is_up=True
        )
    vc72.rel_creator = u3
    vc72.rel_to_comment = c24
    db.session.add(vc72)

    vc73 = VoteComment(
            is_up=False
        )
    vc73.rel_creator = u8
    vc73.rel_to_comment = c25
    db.session.add(vc73)

    vc74 = VoteComment(
            is_up=True
        )
    vc74.rel_creator = u9
    vc74.rel_to_comment = c25
    db.session.add(vc74)

    vc75 = VoteComment(
            is_up=False
        )
    vc75.rel_creator = u10
    vc75.rel_to_comment = c25
    db.session.add(vc75)

    vc76 = VoteComment(
            is_up=True
        )
    vc76.rel_creator = u8
    vc76.rel_to_comment = c26
    db.session.add(vc76)

    vc77 = VoteComment(
            is_up=True
        )
    vc77.rel_creator = u9
    vc77.rel_to_comment = c26
    db.session.add(vc77)

    vc78 = VoteComment(
            is_up=True
        )
    vc78.rel_creator = u10
    vc78.rel_to_comment = c26
    db.session.add(vc78)

    vc79 = VoteComment(
            is_up=True
        )
    vc79.rel_creator = u1
    vc79.rel_to_comment = c27
    db.session.add(vc79)

    vc80 = VoteComment(
            is_up=True
        )
    vc80.rel_creator = u2
    vc80.rel_to_comment = c27
    db.session.add(vc80)

    vc81 = VoteComment(
            is_up=False
        )
    vc81.rel_creator = u3
    vc81.rel_to_comment = c27
    db.session.add(vc81)

    vc82 = VoteComment(
            is_up=False
        )
    vc82.rel_creator = u8
    vc82.rel_to_comment = c28
    db.session.add(vc82)

    vc83 = VoteComment(
            is_up=False
        )
    vc83.rel_creator = u9
    vc83.rel_to_comment = c28
    db.session.add(vc83)

    vc84 = VoteComment(
            is_up=True
        )
    vc84.rel_creator = u10
    vc84.rel_to_comment = c28
    db.session.add(vc84)

    vc85 = VoteComment(
            is_up=False
        )
    vc85.rel_creator = u8
    vc85.rel_to_comment = c29
    db.session.add(vc85)

    vc86 = VoteComment(
            is_up=False
        )
    vc86.rel_creator = u9
    vc86.rel_to_comment = c29
    db.session.add(vc86)

    vc87 = VoteComment(
            is_up=True
        )
    vc87.rel_creator = u10
    vc87.rel_to_comment = c29
    db.session.add(vc87)

    vc88 = VoteComment(
            is_up=True
        )
    vc88.rel_creator = u1
    vc88.rel_to_comment = c30
    db.session.add(vc88)

    vc89 = VoteComment(
            is_up=False
        )
    vc89.rel_creator = u2
    vc89.rel_to_comment = c30
    db.session.add(vc89)

    vc90 = VoteComment(
            is_up=True
        )
    vc90.rel_creator = u3
    vc90.rel_to_comment = c30
    db.session.add(vc90)

    vc91 = VoteComment(
            is_up=True
        )
    vc91.rel_creator = u8
    vc91.rel_to_comment = c31
    db.session.add(vc91)

    vc92 = VoteComment(
            is_up=True
        )
    vc92.rel_creator = u9
    vc92.rel_to_comment = c31
    db.session.add(vc92)

    vc93 = VoteComment(
            is_up=False
        )
    vc93.rel_creator = u10
    vc93.rel_to_comment = c31
    db.session.add(vc93)

    vc94 = VoteComment(
            is_up=True
        )
    vc94.rel_creator = u8
    vc94.rel_to_comment = c32
    db.session.add(vc94)

    vc95 = VoteComment(
            is_up=True
        )
    vc95.rel_creator = u9
    vc95.rel_to_comment = c32
    db.session.add(vc95)

    vc96 = VoteComment(
            is_up=False
        )
    vc96.rel_creator = u10
    vc96.rel_to_comment = c32
    db.session.add(vc96)

    vc97 = VoteComment(
            is_up=True
        )
    vc97.rel_creator = u1
    vc97.rel_to_comment = c33
    db.session.add(vc97)

    vc98 = VoteComment(
            is_up=True
        )
    vc98.rel_creator = u2
    vc98.rel_to_comment = c33
    db.session.add(vc98)

    vc99 = VoteComment(
            is_up=True
        )
    vc99.rel_creator = u3
    vc99.rel_to_comment = c33
    db.session.add(vc99)

    vc100 = VoteComment(
            is_up=True
        )
    vc100.rel_creator = u8
    vc100.rel_to_comment = c34
    db.session.add(vc100)

    vc101 = VoteComment(
            is_up=False
        )
    vc101.rel_creator = u9
    vc101.rel_to_comment = c34
    db.session.add(vc101)

    vc102 = VoteComment(
            is_up=True
        )
    vc102.rel_creator = u10
    vc102.rel_to_comment = c34
    db.session.add(vc102)

    vc103 = VoteComment(
            is_up=True
        )
    vc103.rel_creator = u8
    vc103.rel_to_comment = c35
    db.session.add(vc103)

    vc104 = VoteComment(
            is_up=True
        )
    vc104.rel_creator = u9
    vc104.rel_to_comment = c35
    db.session.add(vc104)

    vc105 = VoteComment(
            is_up=False
        )
    vc105.rel_creator = u10
    vc105.rel_to_comment = c35
    db.session.add(vc105)

    vc106 = VoteComment(
            is_up=False
        )
    vc106.rel_creator = u1
    vc106.rel_to_comment = c36
    db.session.add(vc106)

    vc107 = VoteComment(
            is_up=True
        )
    vc107.rel_creator = u2
    vc107.rel_to_comment = c36
    db.session.add(vc107)

    vc108 = VoteComment(
            is_up=True
        )
    vc108.rel_creator = u3
    vc108.rel_to_comment = c36
    db.session.add(vc108)

    vc109 = VoteComment(
            is_up=False
        )
    vc109.rel_creator = u8
    vc109.rel_to_comment = c37
    db.session.add(vc109)

    vc110 = VoteComment(
            is_up=False
        )
    vc110.rel_creator = u9
    vc110.rel_to_comment = c37
    db.session.add(vc110)

    vc111 = VoteComment(
            is_up=True
        )
    vc111.rel_creator = u10
    vc111.rel_to_comment = c37
    db.session.add(vc111)

    vc112 = VoteComment(
            is_up=True
        )
    vc112.rel_creator = u8
    vc112.rel_to_comment = c38
    db.session.add(vc112)

    vc113 = VoteComment(
            is_up=True
        )
    vc113.rel_creator = u9
    vc113.rel_to_comment = c38
    db.session.add(vc113)

    vc114 = VoteComment(
            is_up=True
        )
    vc114.rel_creator = u10
    vc114.rel_to_comment = c38
    db.session.add(vc114)

    vc115 = VoteComment(
            is_up=True
        )
    vc115.rel_creator = u1
    vc115.rel_to_comment = c39
    db.session.add(vc115)

    vc116 = VoteComment(
            is_up=True
        )
    vc116.rel_creator = u2
    vc116.rel_to_comment = c39
    db.session.add(vc116)

    vc117 = VoteComment(
            is_up=False
        )
    vc117.rel_creator = u3
    vc117.rel_to_comment = c39
    db.session.add(vc117)

    vc118 = VoteComment(
            is_up=False
        )
    vc118.rel_creator = u8
    vc118.rel_to_comment = c40
    db.session.add(vc118)

    vc119 = VoteComment(
            is_up=False
        )
    vc119.rel_creator = u9
    vc119.rel_to_comment = c40
    db.session.add(vc119)

    vc120 = VoteComment(
            is_up=False
        )
    vc120.rel_creator = u10
    vc120.rel_to_comment = c40
    db.session.add(vc120)

    vc121 = VoteComment(
            is_up=True
        )
    vc121.rel_creator = u8
    vc121.rel_to_comment = c41
    db.session.add(vc121)

    vc122 = VoteComment(
            is_up=True
        )
    vc122.rel_creator = u9
    vc122.rel_to_comment = c41
    db.session.add(vc122)

    vc123 = VoteComment(
            is_up=True
        )
    vc123.rel_creator = u10
    vc123.rel_to_comment = c41
    db.session.add(vc123)

    vc124 = VoteComment(
            is_up=False
        )
    vc124.rel_creator = u1
    vc124.rel_to_comment = c42
    db.session.add(vc124)

    vc125 = VoteComment(
            is_up=True
        )
    vc125.rel_creator = u2
    vc125.rel_to_comment = c42
    db.session.add(vc125)

    vc126 = VoteComment(
            is_up=True
        )
    vc126.rel_creator = u3
    vc126.rel_to_comment = c42
    db.session.add(vc126)

    vc127 = VoteComment(
            is_up=False
        )
    vc127.rel_creator = u8
    vc127.rel_to_comment = c43
    db.session.add(vc127)

    vc128 = VoteComment(
            is_up=False
        )
    vc128.rel_creator = u9
    vc128.rel_to_comment = c43
    db.session.add(vc128)

    vc129 = VoteComment(
            is_up=True
        )
    vc129.rel_creator = u10
    vc129.rel_to_comment = c43
    db.session.add(vc129)

    vc130 = VoteComment(
            is_up=True
        )
    vc130.rel_creator = u8
    vc130.rel_to_comment = c44
    db.session.add(vc130)

    vc131 = VoteComment(
            is_up=False
        )
    vc131.rel_creator = u9
    vc131.rel_to_comment = c44
    db.session.add(vc131)

    vc132 = VoteComment(
            is_up=True
        )
    vc132.rel_creator = u10
    vc132.rel_to_comment = c44
    db.session.add(vc132)

    vc133 = VoteComment(
            is_up=True
        )
    vc133.rel_creator = u1
    vc133.rel_to_comment = c45
    db.session.add(vc133)

    vc134 = VoteComment(
            is_up=True
        )
    vc134.rel_creator = u2
    vc134.rel_to_comment = c45
    db.session.add(vc134)

    vc135 = VoteComment(
            is_up=False
        )
    vc135.rel_creator = u3
    vc135.rel_to_comment = c45
    db.session.add(vc135)

    vc136 = VoteComment(
            is_up=False
        )
    vc136.rel_creator = u8
    vc136.rel_to_comment = c46
    db.session.add(vc136)

    vc137 = VoteComment(
            is_up=True
        )
    vc137.rel_creator = u9
    vc137.rel_to_comment = c46
    db.session.add(vc137)

    vc138 = VoteComment(
            is_up=False
        )
    vc138.rel_creator = u10
    vc138.rel_to_comment = c46
    db.session.add(vc138)

    vc139 = VoteComment(
            is_up=False
        )
    vc139.rel_creator = u8
    vc139.rel_to_comment = c47
    db.session.add(vc139)

    vc140 = VoteComment(
            is_up=True
        )
    vc140.rel_creator = u9
    vc140.rel_to_comment = c47
    db.session.add(vc140)

    vc141 = VoteComment(
            is_up=True
        )
    vc141.rel_creator = u10
    vc141.rel_to_comment = c47
    db.session.add(vc141)

    vc142 = VoteComment(
            is_up=False
        )
    vc142.rel_creator = u1
    vc142.rel_to_comment = c48
    db.session.add(vc142)

    vc143 = VoteComment(
            is_up=False
        )
    vc143.rel_creator = u2
    vc143.rel_to_comment = c48
    db.session.add(vc143)

    vc144 = VoteComment(
            is_up=False
        )
    vc144.rel_creator = u3
    vc144.rel_to_comment = c48
    db.session.add(vc144)

    vc145 = VoteComment(
            is_up=False
        )
    vc145.rel_creator = u8
    vc145.rel_to_comment = c49
    db.session.add(vc145)

    vc146 = VoteComment(
            is_up=True
        )
    vc146.rel_creator = u9
    vc146.rel_to_comment = c49
    db.session.add(vc146)

    vc147 = VoteComment(
            is_up=False
        )
    vc147.rel_creator = u10
    vc147.rel_to_comment = c49
    db.session.add(vc147)

    vc148 = VoteComment(
            is_up=True
        )
    vc148.rel_creator = u8
    vc148.rel_to_comment = c50
    db.session.add(vc148)

    vc149 = VoteComment(
            is_up=False
        )
    vc149.rel_creator = u9
    vc149.rel_to_comment = c50
    db.session.add(vc149)

    vc150 = VoteComment(
            is_up=True
        )
    vc150.rel_creator = u10
    vc150.rel_to_comment = c50
    db.session.add(vc150)

    vc151 = VoteComment(
            is_up=False
        )
    vc151.rel_creator = u1
    vc151.rel_to_comment = c51
    db.session.add(vc151)

    vc152 = VoteComment(
            is_up=True
        )
    vc152.rel_creator = u2
    vc152.rel_to_comment = c51
    db.session.add(vc152)

    vc153 = VoteComment(
            is_up=True
        )
    vc153.rel_creator = u3
    vc153.rel_to_comment = c51
    db.session.add(vc153)

    vc154 = VoteComment(
            is_up=True
        )
    vc154.rel_creator = u8
    vc154.rel_to_comment = c52
    db.session.add(vc154)

    vc155 = VoteComment(
            is_up=False
        )
    vc155.rel_creator = u9
    vc155.rel_to_comment = c52
    db.session.add(vc155)

    vc156 = VoteComment(
            is_up=True
        )
    vc156.rel_creator = u10
    vc156.rel_to_comment = c52
    db.session.add(vc156)

    vc157 = VoteComment(
            is_up=True
        )
    vc157.rel_creator = u8
    vc157.rel_to_comment = c53
    db.session.add(vc157)

    vc158 = VoteComment(
            is_up=True
        )
    vc158.rel_creator = u9
    vc158.rel_to_comment = c53
    db.session.add(vc158)

    vc159 = VoteComment(
            is_up=False
        )
    vc159.rel_creator = u10
    vc159.rel_to_comment = c53
    db.session.add(vc159)

    vc160 = VoteComment(
            is_up=False
        )
    vc160.rel_creator = u1
    vc160.rel_to_comment = c54
    db.session.add(vc160)

    vc161 = VoteComment(
            is_up=True
        )
    vc161.rel_creator = u2
    vc161.rel_to_comment = c54
    db.session.add(vc161)

    vc162 = VoteComment(
            is_up=True
        )
    vc162.rel_creator = u3
    vc162.rel_to_comment = c54
    db.session.add(vc162)

    vc163 = VoteComment(
            is_up=True
        )
    vc163.rel_creator = u8
    vc163.rel_to_comment = c55
    db.session.add(vc163)

    vc164 = VoteComment(
            is_up=True
        )
    vc164.rel_creator = u9
    vc164.rel_to_comment = c55
    db.session.add(vc164)

    vc165 = VoteComment(
            is_up=True
        )
    vc165.rel_creator = u10
    vc165.rel_to_comment = c55
    db.session.add(vc165)

    vc166 = VoteComment(
            is_up=True
        )
    vc166.rel_creator = u8
    vc166.rel_to_comment = c56
    db.session.add(vc166)

    vc167 = VoteComment(
            is_up=False
        )
    vc167.rel_creator = u9
    vc167.rel_to_comment = c56
    db.session.add(vc167)

    vc168 = VoteComment(
            is_up=False
        )
    vc168.rel_creator = u10
    vc168.rel_to_comment = c56
    db.session.add(vc168)

    vc169 = VoteComment(
            is_up=True
        )
    vc169.rel_creator = u1
    vc169.rel_to_comment = c57
    db.session.add(vc169)

    vc170 = VoteComment(
            is_up=True
        )
    vc170.rel_creator = u2
    vc170.rel_to_comment = c57
    db.session.add(vc170)

    vc171 = VoteComment(
            is_up=True
        )
    vc171.rel_creator = u3
    vc171.rel_to_comment = c57
    db.session.add(vc171)

    vc172 = VoteComment(
            is_up=True
        )
    vc172.rel_creator = u8
    vc172.rel_to_comment = c58
    db.session.add(vc172)

    vc173 = VoteComment(
            is_up=False
        )
    vc173.rel_creator = u9
    vc173.rel_to_comment = c58
    db.session.add(vc173)

    vc174 = VoteComment(
            is_up=False
        )
    vc174.rel_creator = u10
    vc174.rel_to_comment = c58
    db.session.add(vc174)

    vc175 = VoteComment(
            is_up=False
        )
    vc175.rel_creator = u8
    vc175.rel_to_comment = c59
    db.session.add(vc175)

    vc176 = VoteComment(
            is_up=False
        )
    vc176.rel_creator = u9
    vc176.rel_to_comment = c59
    db.session.add(vc176)

    vc177 = VoteComment(
            is_up=False
        )
    vc177.rel_creator = u10
    vc177.rel_to_comment = c59
    db.session.add(vc177)

    vc178 = VoteComment(
            is_up=True
        )
    vc178.rel_creator = u1
    vc178.rel_to_comment = c60
    db.session.add(vc178)

    vc179 = VoteComment(
            is_up=False
        )
    vc179.rel_creator = u2
    vc179.rel_to_comment = c60
    db.session.add(vc179)

    vc180 = VoteComment(
            is_up=True
        )
    vc180.rel_creator = u3
    vc180.rel_to_comment = c60
    db.session.add(vc180)

    vc181 = VoteComment(
            is_up=False
        )
    vc181.rel_creator = u8
    vc181.rel_to_comment = c61
    db.session.add(vc181)

    vc182 = VoteComment(
            is_up=False
        )
    vc182.rel_creator = u9
    vc182.rel_to_comment = c61
    db.session.add(vc182)

    vc183 = VoteComment(
            is_up=False
        )
    vc183.rel_creator = u10
    vc183.rel_to_comment = c61
    db.session.add(vc183)

    vc184 = VoteComment(
            is_up=True
        )
    vc184.rel_creator = u8
    vc184.rel_to_comment = c62
    db.session.add(vc184)

    vc185 = VoteComment(
            is_up=True
        )
    vc185.rel_creator = u9
    vc185.rel_to_comment = c62
    db.session.add(vc185)

    vc186 = VoteComment(
            is_up=True
        )
    vc186.rel_creator = u10
    vc186.rel_to_comment = c62
    db.session.add(vc186)

    vc187 = VoteComment(
            is_up=False
        )
    vc187.rel_creator = u1
    vc187.rel_to_comment = c63
    db.session.add(vc187)

    vc188 = VoteComment(
            is_up=True
        )
    vc188.rel_creator = u2
    vc188.rel_to_comment = c63
    db.session.add(vc188)

    vc189 = VoteComment(
            is_up=True
        )
    vc189.rel_creator = u3
    vc189.rel_to_comment = c63
    db.session.add(vc189)

    vc190 = VoteComment(
            is_up=True
        )
    vc190.rel_creator = u8
    vc190.rel_to_comment = c64
    db.session.add(vc190)

    vc191 = VoteComment(
            is_up=True
        )
    vc191.rel_creator = u9
    vc191.rel_to_comment = c64
    db.session.add(vc191)

    vc192 = VoteComment(
            is_up=False
        )
    vc192.rel_creator = u10
    vc192.rel_to_comment = c64
    db.session.add(vc192)

    vc193 = VoteComment(
            is_up=True
        )
    vc193.rel_creator = u8
    vc193.rel_to_comment = c65
    db.session.add(vc193)

    vc194 = VoteComment(
            is_up=True
        )
    vc194.rel_creator = u9
    vc194.rel_to_comment = c65
    db.session.add(vc194)

    vc195 = VoteComment(
            is_up=True
        )
    vc195.rel_creator = u10
    vc195.rel_to_comment = c65
    db.session.add(vc195)

    vc196 = VoteComment(
            is_up=True
        )
    vc196.rel_creator = u1
    vc196.rel_to_comment = c66
    db.session.add(vc196)

    vc197 = VoteComment(
            is_up=True
        )
    vc197.rel_creator = u2
    vc197.rel_to_comment = c66
    db.session.add(vc197)

    vc198 = VoteComment(
            is_up=True
        )
    vc198.rel_creator = u3
    vc198.rel_to_comment = c66
    db.session.add(vc198)

    vc199 = VoteComment(
            is_up=True
        )
    vc199.rel_creator = u8
    vc199.rel_to_comment = c67
    db.session.add(vc199)

    vc200 = VoteComment(
            is_up=True
        )
    vc200.rel_creator = u9
    vc200.rel_to_comment = c67
    db.session.add(vc200)

    vc201 = VoteComment(
            is_up=True
        )
    vc201.rel_creator = u10
    vc201.rel_to_comment = c67
    db.session.add(vc201)

    vc202 = VoteComment(
            is_up=True
        )
    vc202.rel_creator = u8
    vc202.rel_to_comment = c68
    db.session.add(vc202)

    vc203 = VoteComment(
            is_up=True
        )
    vc203.rel_creator = u9
    vc203.rel_to_comment = c68
    db.session.add(vc203)

    vc204 = VoteComment(
            is_up=False
        )
    vc204.rel_creator = u10
    vc204.rel_to_comment = c68
    db.session.add(vc204)

    vc205 = VoteComment(
            is_up=False
        )
    vc205.rel_creator = u1
    vc205.rel_to_comment = c69
    db.session.add(vc205)

    vc206 = VoteComment(
            is_up=True
        )
    vc206.rel_creator = u2
    vc206.rel_to_comment = c69
    db.session.add(vc206)

    vc207 = VoteComment(
            is_up=True
        )
    vc207.rel_creator = u3
    vc207.rel_to_comment = c69
    db.session.add(vc207)

    vc208 = VoteComment(
            is_up=True
        )
    vc208.rel_creator = u8
    vc208.rel_to_comment = c70
    db.session.add(vc208)

    vc209 = VoteComment(
            is_up=True
        )
    vc209.rel_creator = u9
    vc209.rel_to_comment = c70
    db.session.add(vc209)

    vc210 = VoteComment(
            is_up=True
        )
    vc210.rel_creator = u10
    vc210.rel_to_comment = c70
    db.session.add(vc210)

    vc211 = VoteComment(
            is_up=True
        )
    vc211.rel_creator = u8
    vc211.rel_to_comment = c71
    db.session.add(vc211)

    vc212 = VoteComment(
            is_up=True
        )
    vc212.rel_creator = u9
    vc212.rel_to_comment = c71
    db.session.add(vc212)

    vc213 = VoteComment(
            is_up=True
        )
    vc213.rel_creator = u10
    vc213.rel_to_comment = c71
    db.session.add(vc213)

    vc214 = VoteComment(
            is_up=True
        )
    vc214.rel_creator = u1
    vc214.rel_to_comment = c72
    db.session.add(vc214)

    vc215 = VoteComment(
            is_up=True
        )
    vc215.rel_creator = u2
    vc215.rel_to_comment = c72
    db.session.add(vc215)

    vc216 = VoteComment(
            is_up=True
        )
    vc216.rel_creator = u3
    vc216.rel_to_comment = c72
    db.session.add(vc216)

    vc217 = VoteComment(
            is_up=False
        )
    vc217.rel_creator = u8
    vc217.rel_to_comment = c73
    db.session.add(vc217)

    vc218 = VoteComment(
            is_up=True
        )
    vc218.rel_creator = u9
    vc218.rel_to_comment = c73
    db.session.add(vc218)

    vc219 = VoteComment(
            is_up=True
        )
    vc219.rel_creator = u10
    vc219.rel_to_comment = c73
    db.session.add(vc219)

    vc220 = VoteComment(
            is_up=False
        )
    vc220.rel_creator = u8
    vc220.rel_to_comment = c74
    db.session.add(vc220)

    vc221 = VoteComment(
            is_up=False
        )
    vc221.rel_creator = u9
    vc221.rel_to_comment = c74
    db.session.add(vc221)

    vc222 = VoteComment(
            is_up=False
        )
    vc222.rel_creator = u10
    vc222.rel_to_comment = c74
    db.session.add(vc222)

    vc223 = VoteComment(
            is_up=False
        )
    vc223.rel_creator = u1
    vc223.rel_to_comment = c75
    db.session.add(vc223)

    vc224 = VoteComment(
            is_up=True
        )
    vc224.rel_creator = u2
    vc224.rel_to_comment = c75
    db.session.add(vc224)

    vc225 = VoteComment(
            is_up=True
        )
    vc225.rel_creator = u3
    vc225.rel_to_comment = c75
    db.session.add(vc225)

    vc226 = VoteComment(
            is_up=True
        )
    vc226.rel_creator = u8
    vc226.rel_to_comment = c76
    db.session.add(vc226)

    vc227 = VoteComment(
            is_up=True
        )
    vc227.rel_creator = u9
    vc227.rel_to_comment = c76
    db.session.add(vc227)

    vc228 = VoteComment(
            is_up=False
        )
    vc228.rel_creator = u10
    vc228.rel_to_comment = c76
    db.session.add(vc228)

    vc229 = VoteComment(
            is_up=False
        )
    vc229.rel_creator = u8
    vc229.rel_to_comment = c77
    db.session.add(vc229)

    vc230 = VoteComment(
            is_up=True
        )
    vc230.rel_creator = u9
    vc230.rel_to_comment = c77
    db.session.add(vc230)

    vc231 = VoteComment(
            is_up=True
        )
    vc231.rel_creator = u10
    vc231.rel_to_comment = c77
    db.session.add(vc231)

    vc232 = VoteComment(
            is_up=True
        )
    vc232.rel_creator = u1
    vc232.rel_to_comment = c78
    db.session.add(vc232)

    vc233 = VoteComment(
            is_up=True
        )
    vc233.rel_creator = u2
    vc233.rel_to_comment = c78
    db.session.add(vc233)

    vc234 = VoteComment(
            is_up=False
        )
    vc234.rel_creator = u3
    vc234.rel_to_comment = c78
    db.session.add(vc234)

    vc235 = VoteComment(
            is_up=False
        )
    vc235.rel_creator = u8
    vc235.rel_to_comment = c79
    db.session.add(vc235)

    vc236 = VoteComment(
            is_up=True
        )
    vc236.rel_creator = u9
    vc236.rel_to_comment = c79
    db.session.add(vc236)

    vc237 = VoteComment(
            is_up=True
        )
    vc237.rel_creator = u10
    vc237.rel_to_comment = c79
    db.session.add(vc237)

    vc238 = VoteComment(
            is_up=True
        )
    vc238.rel_creator = u8
    vc238.rel_to_comment = c80
    db.session.add(vc238)

    vc239 = VoteComment(
            is_up=True
        )
    vc239.rel_creator = u9
    vc239.rel_to_comment = c80
    db.session.add(vc239)

    vc240 = VoteComment(
            is_up=True
        )
    vc240.rel_creator = u10
    vc240.rel_to_comment = c80
    db.session.add(vc240)

    vc241 = VoteComment(
            is_up=True
        )
    vc241.rel_creator = u1
    vc241.rel_to_comment = c81
    db.session.add(vc241)

    vc242 = VoteComment(
            is_up=True
        )
    vc242.rel_creator = u2
    vc242.rel_to_comment = c81
    db.session.add(vc242)

    vc243 = VoteComment(
            is_up=True
        )
    vc243.rel_creator = u3
    vc243.rel_to_comment = c81
    db.session.add(vc243)

    vc244 = VoteComment(
            is_up=False
        )
    vc244.rel_creator = u8
    vc244.rel_to_comment = c82
    db.session.add(vc244)

    vc245 = VoteComment(
            is_up=True
        )
    vc245.rel_creator = u9
    vc245.rel_to_comment = c82
    db.session.add(vc245)

    vc246 = VoteComment(
            is_up=False
        )
    vc246.rel_creator = u10
    vc246.rel_to_comment = c82
    db.session.add(vc246)

    vc247 = VoteComment(
            is_up=False
        )
    vc247.rel_creator = u8
    vc247.rel_to_comment = c83
    db.session.add(vc247)

    vc248 = VoteComment(
            is_up=True
        )
    vc248.rel_creator = u9
    vc248.rel_to_comment = c83
    db.session.add(vc248)

    vc249 = VoteComment(
            is_up=False
        )
    vc249.rel_creator = u10
    vc249.rel_to_comment = c83
    db.session.add(vc249)

    vc250 = VoteComment(
            is_up=True
        )
    vc250.rel_creator = u1
    vc250.rel_to_comment = c84
    db.session.add(vc250)

    vc251 = VoteComment(
            is_up=True
        )
    vc251.rel_creator = u2
    vc251.rel_to_comment = c84
    db.session.add(vc251)

    vc252 = VoteComment(
            is_up=True
        )
    vc252.rel_creator = u3
    vc252.rel_to_comment = c84
    db.session.add(vc252)

    vc253 = VoteComment(
            is_up=True
        )
    vc253.rel_creator = u8
    vc253.rel_to_comment = c85
    db.session.add(vc253)

    vc254 = VoteComment(
            is_up=True
        )
    vc254.rel_creator = u9
    vc254.rel_to_comment = c85
    db.session.add(vc254)

    vc255 = VoteComment(
            is_up=False
        )
    vc255.rel_creator = u10
    vc255.rel_to_comment = c85
    db.session.add(vc255)

    vc256 = VoteComment(
            is_up=True
        )
    vc256.rel_creator = u8
    vc256.rel_to_comment = c86
    db.session.add(vc256)

    vc257 = VoteComment(
            is_up=False
        )
    vc257.rel_creator = u9
    vc257.rel_to_comment = c86
    db.session.add(vc257)

    vc258 = VoteComment(
            is_up=True
        )
    vc258.rel_creator = u10
    vc258.rel_to_comment = c86
    db.session.add(vc258)

    vc259 = VoteComment(
            is_up=False
        )
    vc259.rel_creator = u1
    vc259.rel_to_comment = c87
    db.session.add(vc259)

    vc260 = VoteComment(
            is_up=False
        )
    vc260.rel_creator = u2
    vc260.rel_to_comment = c87
    db.session.add(vc260)

    vc261 = VoteComment(
            is_up=True
        )
    vc261.rel_creator = u3
    vc261.rel_to_comment = c87
    db.session.add(vc261)

    vc262 = VoteComment(
            is_up=False
        )
    vc262.rel_creator = u8
    vc262.rel_to_comment = c88
    db.session.add(vc262)

    vc263 = VoteComment(
            is_up=True
        )
    vc263.rel_creator = u9
    vc263.rel_to_comment = c88
    db.session.add(vc263)

    vc264 = VoteComment(
            is_up=True
        )
    vc264.rel_creator = u10
    vc264.rel_to_comment = c88
    db.session.add(vc264)

    vc265 = VoteComment(
            is_up=True
        )
    vc265.rel_creator = u8
    vc265.rel_to_comment = c89
    db.session.add(vc265)

    vc266 = VoteComment(
            is_up=False
        )
    vc266.rel_creator = u9
    vc266.rel_to_comment = c89
    db.session.add(vc266)

    vc267 = VoteComment(
            is_up=True
        )
    vc267.rel_creator = u10
    vc267.rel_to_comment = c89
    db.session.add(vc267)

    vc268 = VoteComment(
            is_up=False
        )
    vc268.rel_creator = u1
    vc268.rel_to_comment = c90
    db.session.add(vc268)

    vc269 = VoteComment(
            is_up=True
        )
    vc269.rel_creator = u2
    vc269.rel_to_comment = c90
    db.session.add(vc269)

    vc270 = VoteComment(
            is_up=False
        )
    vc270.rel_creator = u3
    vc270.rel_to_comment = c90
    db.session.add(vc270)

    vc271 = VoteComment(
            is_up=True
        )
    vc271.rel_creator = u8
    vc271.rel_to_comment = c91
    db.session.add(vc271)

    vc272 = VoteComment(
            is_up=True
        )
    vc272.rel_creator = u9
    vc272.rel_to_comment = c91
    db.session.add(vc272)

    vc273 = VoteComment(
            is_up=True
        )
    vc273.rel_creator = u10
    vc273.rel_to_comment = c91
    db.session.add(vc273)

    vc274 = VoteComment(
            is_up=True
        )
    vc274.rel_creator = u8
    vc274.rel_to_comment = c92
    db.session.add(vc274)

    vc275 = VoteComment(
            is_up=True
        )
    vc275.rel_creator = u9
    vc275.rel_to_comment = c92
    db.session.add(vc275)

    vc276 = VoteComment(
            is_up=True
        )
    vc276.rel_creator = u10
    vc276.rel_to_comment = c92
    db.session.add(vc276)

    vc277 = VoteComment(
            is_up=False
        )
    vc277.rel_creator = u1
    vc277.rel_to_comment = c93
    db.session.add(vc277)

    vc278 = VoteComment(
            is_up=True
        )
    vc278.rel_creator = u2
    vc278.rel_to_comment = c93
    db.session.add(vc278)

    vc279 = VoteComment(
            is_up=True
        )
    vc279.rel_creator = u3
    vc279.rel_to_comment = c93
    db.session.add(vc279)

    vc280 = VoteComment(
            is_up=True
        )
    vc280.rel_creator = u8
    vc280.rel_to_comment = c94
    db.session.add(vc280)

    vc281 = VoteComment(
            is_up=False
        )
    vc281.rel_creator = u9
    vc281.rel_to_comment = c94
    db.session.add(vc281)

    vc282 = VoteComment(
            is_up=False
        )
    vc282.rel_creator = u10
    vc282.rel_to_comment = c94
    db.session.add(vc282)

    vc283 = VoteComment(
            is_up=True
        )
    vc283.rel_creator = u8
    vc283.rel_to_comment = c95
    db.session.add(vc283)

    vc284 = VoteComment(
            is_up=True
        )
    vc284.rel_creator = u9
    vc284.rel_to_comment = c95
    db.session.add(vc284)

    vc285 = VoteComment(
            is_up=True
        )
    vc285.rel_creator = u10
    vc285.rel_to_comment = c95
    db.session.add(vc285)

    vc286 = VoteComment(
            is_up=True
        )
    vc286.rel_creator = u1
    vc286.rel_to_comment = c96
    db.session.add(vc286)

    vc287 = VoteComment(
            is_up=False
        )
    vc287.rel_creator = u2
    vc287.rel_to_comment = c96
    db.session.add(vc287)

    vc288 = VoteComment(
            is_up=True
        )
    vc288.rel_creator = u3
    vc288.rel_to_comment = c96
    db.session.add(vc288)

    vc289 = VoteComment(
            is_up=True
        )
    vc289.rel_creator = u8
    vc289.rel_to_comment = c97
    db.session.add(vc289)

    vc290 = VoteComment(
            is_up=False
        )
    vc290.rel_creator = u9
    vc290.rel_to_comment = c97
    db.session.add(vc290)

    vc291 = VoteComment(
            is_up=True
        )
    vc291.rel_creator = u10
    vc291.rel_to_comment = c97
    db.session.add(vc291)

    vc292 = VoteComment(
            is_up=True
        )
    vc292.rel_creator = u8
    vc292.rel_to_comment = c98
    db.session.add(vc292)

    vc293 = VoteComment(
            is_up=False
        )
    vc293.rel_creator = u9
    vc293.rel_to_comment = c98
    db.session.add(vc293)

    vc294 = VoteComment(
            is_up=True
        )
    vc294.rel_creator = u10
    vc294.rel_to_comment = c98
    db.session.add(vc294)

    vc295 = VoteComment(
            is_up=True
        )
    vc295.rel_creator = u1
    vc295.rel_to_comment = c99
    db.session.add(vc295)

    vc296 = VoteComment(
            is_up=True
        )
    vc296.rel_creator = u2
    vc296.rel_to_comment = c99
    db.session.add(vc296)

    vc297 = VoteComment(
            is_up=True
        )
    vc297.rel_creator = u3
    vc297.rel_to_comment = c99
    db.session.add(vc297)

    vc298 = VoteComment(
            is_up=False
        )
    vc298.rel_creator = u8
    vc298.rel_to_comment = c100
    db.session.add(vc298)

    vc299 = VoteComment(
            is_up=True
        )
    vc299.rel_creator = u9
    vc299.rel_to_comment = c100
    db.session.add(vc299)

    vc300 = VoteComment(
            is_up=True
        )
    vc300.rel_creator = u10
    vc300.rel_to_comment = c100
    db.session.add(vc300)

    vc301 = VoteComment(
            is_up=False
        )
    vc301.rel_creator = u8
    vc301.rel_to_comment = c101
    db.session.add(vc301)

    vc302 = VoteComment(
            is_up=False
        )
    vc302.rel_creator = u9
    vc302.rel_to_comment = c101
    db.session.add(vc302)

    vc303 = VoteComment(
            is_up=True
        )
    vc303.rel_creator = u10
    vc303.rel_to_comment = c101
    db.session.add(vc303)

    vc304 = VoteComment(
            is_up=True
        )
    vc304.rel_creator = u1
    vc304.rel_to_comment = c102
    db.session.add(vc304)

    vc305 = VoteComment(
            is_up=False
        )
    vc305.rel_creator = u2
    vc305.rel_to_comment = c102
    db.session.add(vc305)

    vc306 = VoteComment(
            is_up=True
        )
    vc306.rel_creator = u3
    vc306.rel_to_comment = c102
    db.session.add(vc306)

    vc307 = VoteComment(
            is_up=True
        )
    vc307.rel_creator = u8
    vc307.rel_to_comment = c103
    db.session.add(vc307)

    vc308 = VoteComment(
            is_up=True
        )
    vc308.rel_creator = u9
    vc308.rel_to_comment = c103
    db.session.add(vc308)

    vc309 = VoteComment(
            is_up=True
        )
    vc309.rel_creator = u10
    vc309.rel_to_comment = c103
    db.session.add(vc309)

    vc310 = VoteComment(
            is_up=False
        )
    vc310.rel_creator = u8
    vc310.rel_to_comment = c104
    db.session.add(vc310)

    vc311 = VoteComment(
            is_up=False
        )
    vc311.rel_creator = u9
    vc311.rel_to_comment = c104
    db.session.add(vc311)

    vc312 = VoteComment(
            is_up=True
        )
    vc312.rel_creator = u10
    vc312.rel_to_comment = c104
    db.session.add(vc312)

    vc313 = VoteComment(
            is_up=True
        )
    vc313.rel_creator = u1
    vc313.rel_to_comment = c105
    db.session.add(vc313)

    vc314 = VoteComment(
            is_up=False
        )
    vc314.rel_creator = u2
    vc314.rel_to_comment = c105
    db.session.add(vc314)

    vc315 = VoteComment(
            is_up=False
        )
    vc315.rel_creator = u3
    vc315.rel_to_comment = c105
    db.session.add(vc315)

    vc316 = VoteComment(
            is_up=True
        )
    vc316.rel_creator = u8
    vc316.rel_to_comment = c106
    db.session.add(vc316)

    vc317 = VoteComment(
            is_up=True
        )
    vc317.rel_creator = u9
    vc317.rel_to_comment = c106
    db.session.add(vc317)

    vc318 = VoteComment(
            is_up=False
        )
    vc318.rel_creator = u10
    vc318.rel_to_comment = c106
    db.session.add(vc318)

    vc319 = VoteComment(
            is_up=True
        )
    vc319.rel_creator = u8
    vc319.rel_to_comment = c107
    db.session.add(vc319)

    vc320 = VoteComment(
            is_up=True
        )
    vc320.rel_creator = u9
    vc320.rel_to_comment = c107
    db.session.add(vc320)

    vc321 = VoteComment(
            is_up=True
        )
    vc321.rel_creator = u10
    vc321.rel_to_comment = c107
    db.session.add(vc321)

    vc322 = VoteComment(
            is_up=False
        )
    vc322.rel_creator = u1
    vc322.rel_to_comment = c108
    db.session.add(vc322)

    vc323 = VoteComment(
            is_up=True
        )
    vc323.rel_creator = u2
    vc323.rel_to_comment = c108
    db.session.add(vc323)

    vc324 = VoteComment(
            is_up=True
        )
    vc324.rel_creator = u3
    vc324.rel_to_comment = c108
    db.session.add(vc324)

    vc325 = VoteComment(
            is_up=False
        )
    vc325.rel_creator = u8
    vc325.rel_to_comment = c109
    db.session.add(vc325)

    vc326 = VoteComment(
            is_up=True
        )
    vc326.rel_creator = u9
    vc326.rel_to_comment = c109
    db.session.add(vc326)

    vc327 = VoteComment(
            is_up=True
        )
    vc327.rel_creator = u10
    vc327.rel_to_comment = c109
    db.session.add(vc327)

    vc328 = VoteComment(
            is_up=False
        )
    vc328.rel_creator = u8
    vc328.rel_to_comment = c110
    db.session.add(vc328)

    vc329 = VoteComment(
            is_up=True
        )
    vc329.rel_creator = u9
    vc329.rel_to_comment = c110
    db.session.add(vc329)

    vc330 = VoteComment(
            is_up=False
        )
    vc330.rel_creator = u10
    vc330.rel_to_comment = c110
    db.session.add(vc330)

    vc331 = VoteComment(
            is_up=True
        )
    vc331.rel_creator = u1
    vc331.rel_to_comment = c111
    db.session.add(vc331)

    vc332 = VoteComment(
            is_up=False
        )
    vc332.rel_creator = u2
    vc332.rel_to_comment = c111
    db.session.add(vc332)

    vc333 = VoteComment(
            is_up=True
        )
    vc333.rel_creator = u3
    vc333.rel_to_comment = c111
    db.session.add(vc333)

    vc334 = VoteComment(
            is_up=False
        )
    vc334.rel_creator = u8
    vc334.rel_to_comment = c112
    db.session.add(vc334)

    vc335 = VoteComment(
            is_up=False
        )
    vc335.rel_creator = u9
    vc335.rel_to_comment = c112
    db.session.add(vc335)

    vc336 = VoteComment(
            is_up=True
        )
    vc336.rel_creator = u10
    vc336.rel_to_comment = c112
    db.session.add(vc336)

    vc337 = VoteComment(
            is_up=True
        )
    vc337.rel_creator = u8
    vc337.rel_to_comment = c113
    db.session.add(vc337)

    vc338 = VoteComment(
            is_up=True
        )
    vc338.rel_creator = u9
    vc338.rel_to_comment = c113
    db.session.add(vc338)

    vc339 = VoteComment(
            is_up=True
        )
    vc339.rel_creator = u10
    vc339.rel_to_comment = c113
    db.session.add(vc339)

    vc340 = VoteComment(
            is_up=False
        )
    vc340.rel_creator = u1
    vc340.rel_to_comment = c114
    db.session.add(vc340)

    vc341 = VoteComment(
            is_up=True
        )
    vc341.rel_creator = u2
    vc341.rel_to_comment = c114
    db.session.add(vc341)

    vc342 = VoteComment(
            is_up=True
        )
    vc342.rel_creator = u3
    vc342.rel_to_comment = c114
    db.session.add(vc342)

    vc343 = VoteComment(
            is_up=False
        )
    vc343.rel_creator = u8
    vc343.rel_to_comment = c115
    db.session.add(vc343)

    vc344 = VoteComment(
            is_up=True
        )
    vc344.rel_creator = u9
    vc344.rel_to_comment = c115
    db.session.add(vc344)

    vc345 = VoteComment(
            is_up=False
        )
    vc345.rel_creator = u10
    vc345.rel_to_comment = c115
    db.session.add(vc345)

    vc346 = VoteComment(
            is_up=True
        )
    vc346.rel_creator = u8
    vc346.rel_to_comment = c116
    db.session.add(vc346)

    vc347 = VoteComment(
            is_up=True
        )
    vc347.rel_creator = u9
    vc347.rel_to_comment = c116
    db.session.add(vc347)

    vc348 = VoteComment(
            is_up=True
        )
    vc348.rel_creator = u10
    vc348.rel_to_comment = c116
    db.session.add(vc348)

    vc349 = VoteComment(
            is_up=False
        )
    vc349.rel_creator = u1
    vc349.rel_to_comment = c117
    db.session.add(vc349)

    vc350 = VoteComment(
            is_up=True
        )
    vc350.rel_creator = u2
    vc350.rel_to_comment = c117
    db.session.add(vc350)

    vc351 = VoteComment(
            is_up=True
        )
    vc351.rel_creator = u3
    vc351.rel_to_comment = c117
    db.session.add(vc351)

    vc352 = VoteComment(
            is_up=False
        )
    vc352.rel_creator = u8
    vc352.rel_to_comment = c118
    db.session.add(vc352)

    vc353 = VoteComment(
            is_up=True
        )
    vc353.rel_creator = u9
    vc353.rel_to_comment = c118
    db.session.add(vc353)

    vc354 = VoteComment(
            is_up=False
        )
    vc354.rel_creator = u10
    vc354.rel_to_comment = c118
    db.session.add(vc354)

    vc355 = VoteComment(
            is_up=False
        )
    vc355.rel_creator = u8
    vc355.rel_to_comment = c119
    db.session.add(vc355)

    vc356 = VoteComment(
            is_up=True
        )
    vc356.rel_creator = u9
    vc356.rel_to_comment = c119
    db.session.add(vc356)

    vc357 = VoteComment(
            is_up=True
        )
    vc357.rel_creator = u10
    vc357.rel_to_comment = c119
    db.session.add(vc357)

    vc358 = VoteComment(
            is_up=False
        )
    vc358.rel_creator = u1
    vc358.rel_to_comment = c120
    db.session.add(vc358)

    vc359 = VoteComment(
            is_up=False
        )
    vc359.rel_creator = u2
    vc359.rel_to_comment = c120
    db.session.add(vc359)

    vc360 = VoteComment(
            is_up=False
        )
    vc360.rel_creator = u3
    vc360.rel_to_comment = c120
    db.session.add(vc360)

    vc361 = VoteComment(
            is_up=True
        )
    vc361.rel_creator = u8
    vc361.rel_to_comment = c121
    db.session.add(vc361)

    vc362 = VoteComment(
            is_up=True
        )
    vc362.rel_creator = u9
    vc362.rel_to_comment = c121
    db.session.add(vc362)

    vc363 = VoteComment(
            is_up=False
        )
    vc363.rel_creator = u10
    vc363.rel_to_comment = c121
    db.session.add(vc363)

    vc364 = VoteComment(
            is_up=False
        )
    vc364.rel_creator = u8
    vc364.rel_to_comment = c122
    db.session.add(vc364)

    vc365 = VoteComment(
            is_up=True
        )
    vc365.rel_creator = u9
    vc365.rel_to_comment = c122
    db.session.add(vc365)

    vc366 = VoteComment(
            is_up=True
        )
    vc366.rel_creator = u10
    vc366.rel_to_comment = c122
    db.session.add(vc366)

    vc367 = VoteComment(
            is_up=False
        )
    vc367.rel_creator = u1
    vc367.rel_to_comment = c123
    db.session.add(vc367)

    vc368 = VoteComment(
            is_up=True
        )
    vc368.rel_creator = u2
    vc368.rel_to_comment = c123
    db.session.add(vc368)

    vc369 = VoteComment(
            is_up=True
        )
    vc369.rel_creator = u3
    vc369.rel_to_comment = c123
    db.session.add(vc369)

    vc370 = VoteComment(
            is_up=True
        )
    vc370.rel_creator = u8
    vc370.rel_to_comment = c124
    db.session.add(vc370)

    vc371 = VoteComment(
            is_up=True
        )
    vc371.rel_creator = u9
    vc371.rel_to_comment = c124
    db.session.add(vc371)

    vc372 = VoteComment(
            is_up=True
        )
    vc372.rel_creator = u10
    vc372.rel_to_comment = c124
    db.session.add(vc372)

    vc373 = VoteComment(
            is_up=False
        )
    vc373.rel_creator = u8
    vc373.rel_to_comment = c125
    db.session.add(vc373)

    vc374 = VoteComment(
            is_up=True
        )
    vc374.rel_creator = u9
    vc374.rel_to_comment = c125
    db.session.add(vc374)

    vc375 = VoteComment(
            is_up=False
        )
    vc375.rel_creator = u10
    vc375.rel_to_comment = c125
    db.session.add(vc375)

    vc376 = VoteComment(
            is_up=True
        )
    vc376.rel_creator = u1
    vc376.rel_to_comment = c126
    db.session.add(vc376)

    vc377 = VoteComment(
            is_up=True
        )
    vc377.rel_creator = u2
    vc377.rel_to_comment = c126
    db.session.add(vc377)

    vc378 = VoteComment(
            is_up=True
        )
    vc378.rel_creator = u3
    vc378.rel_to_comment = c126
    db.session.add(vc378)

    vc379 = VoteComment(
            is_up=True
        )
    vc379.rel_creator = u8
    vc379.rel_to_comment = c127
    db.session.add(vc379)

    vc380 = VoteComment(
            is_up=False
        )
    vc380.rel_creator = u9
    vc380.rel_to_comment = c127
    db.session.add(vc380)

    vc381 = VoteComment(
            is_up=False
        )
    vc381.rel_creator = u10
    vc381.rel_to_comment = c127
    db.session.add(vc381)

    vc382 = VoteComment(
            is_up=True
        )
    vc382.rel_creator = u8
    vc382.rel_to_comment = c128
    db.session.add(vc382)

    vc383 = VoteComment(
            is_up=True
        )
    vc383.rel_creator = u9
    vc383.rel_to_comment = c128
    db.session.add(vc383)

    vc384 = VoteComment(
            is_up=True
        )
    vc384.rel_creator = u10
    vc384.rel_to_comment = c128
    db.session.add(vc384)

    vc385 = VoteComment(
            is_up=True
        )
    vc385.rel_creator = u1
    vc385.rel_to_comment = c129
    db.session.add(vc385)

    vc386 = VoteComment(
            is_up=True
        )
    vc386.rel_creator = u2
    vc386.rel_to_comment = c129
    db.session.add(vc386)

    vc387 = VoteComment(
            is_up=False
        )
    vc387.rel_creator = u3
    vc387.rel_to_comment = c129
    db.session.add(vc387)

    vc388 = VoteComment(
            is_up=True
        )
    vc388.rel_creator = u8
    vc388.rel_to_comment = c130
    db.session.add(vc388)

    vc389 = VoteComment(
            is_up=False
        )
    vc389.rel_creator = u9
    vc389.rel_to_comment = c130
    db.session.add(vc389)

    vc390 = VoteComment(
            is_up=True
        )
    vc390.rel_creator = u10
    vc390.rel_to_comment = c130
    db.session.add(vc390)

    vc391 = VoteComment(
            is_up=False
        )
    vc391.rel_creator = u8
    vc391.rel_to_comment = c131
    db.session.add(vc391)

    vc392 = VoteComment(
            is_up=True
        )
    vc392.rel_creator = u9
    vc392.rel_to_comment = c131
    db.session.add(vc392)

    vc393 = VoteComment(
            is_up=False
        )
    vc393.rel_creator = u10
    vc393.rel_to_comment = c131
    db.session.add(vc393)

    vc394 = VoteComment(
            is_up=True
        )
    vc394.rel_creator = u1
    vc394.rel_to_comment = c132
    db.session.add(vc394)

    vc395 = VoteComment(
            is_up=True
        )
    vc395.rel_creator = u2
    vc395.rel_to_comment = c132
    db.session.add(vc395)

    vc396 = VoteComment(
            is_up=False
        )
    vc396.rel_creator = u3
    vc396.rel_to_comment = c132
    db.session.add(vc396)

    vc397 = VoteComment(
            is_up=False
        )
    vc397.rel_creator = u8
    vc397.rel_to_comment = c133
    db.session.add(vc397)

    vc398 = VoteComment(
            is_up=True
        )
    vc398.rel_creator = u9
    vc398.rel_to_comment = c133
    db.session.add(vc398)

    vc399 = VoteComment(
            is_up=True
        )
    vc399.rel_creator = u10
    vc399.rel_to_comment = c133
    db.session.add(vc399)

    vc400 = VoteComment(
            is_up=True
        )
    vc400.rel_creator = u8
    vc400.rel_to_comment = c134
    db.session.add(vc400)

    vc401 = VoteComment(
            is_up=False
        )
    vc401.rel_creator = u9
    vc401.rel_to_comment = c134
    db.session.add(vc401)

    vc402 = VoteComment(
            is_up=True
        )
    vc402.rel_creator = u10
    vc402.rel_to_comment = c134
    db.session.add(vc402)

    vc403 = VoteComment(
            is_up=True
        )
    vc403.rel_creator = u1
    vc403.rel_to_comment = c135
    db.session.add(vc403)

    vc404 = VoteComment(
            is_up=True
        )
    vc404.rel_creator = u2
    vc404.rel_to_comment = c135
    db.session.add(vc404)

    vc405 = VoteComment(
            is_up=True
        )
    vc405.rel_creator = u3
    vc405.rel_to_comment = c135
    db.session.add(vc405)

    vc406 = VoteComment(
            is_up=True
        )
    vc406.rel_creator = u8
    vc406.rel_to_comment = c136
    db.session.add(vc406)

    vc407 = VoteComment(
            is_up=True
        )
    vc407.rel_creator = u9
    vc407.rel_to_comment = c136
    db.session.add(vc407)

    vc408 = VoteComment(
            is_up=True
        )
    vc408.rel_creator = u10
    vc408.rel_to_comment = c136
    db.session.add(vc408)

    vc409 = VoteComment(
            is_up=True
        )
    vc409.rel_creator = u8
    vc409.rel_to_comment = c137
    db.session.add(vc409)

    vc410 = VoteComment(
            is_up=True
        )
    vc410.rel_creator = u9
    vc410.rel_to_comment = c137
    db.session.add(vc410)

    vc411 = VoteComment(
            is_up=False
        )
    vc411.rel_creator = u10
    vc411.rel_to_comment = c137
    db.session.add(vc411)

    vc412 = VoteComment(
            is_up=False
        )
    vc412.rel_creator = u1
    vc412.rel_to_comment = c138
    db.session.add(vc412)

    vc413 = VoteComment(
            is_up=False
        )
    vc413.rel_creator = u2
    vc413.rel_to_comment = c138
    db.session.add(vc413)

    vc414 = VoteComment(
            is_up=False
        )
    vc414.rel_creator = u3
    vc414.rel_to_comment = c138
    db.session.add(vc414)

    vc415 = VoteComment(
            is_up=True
        )
    vc415.rel_creator = u8
    vc415.rel_to_comment = c139
    db.session.add(vc415)

    vc416 = VoteComment(
            is_up=True
        )
    vc416.rel_creator = u9
    vc416.rel_to_comment = c139
    db.session.add(vc416)

    vc417 = VoteComment(
            is_up=True
        )
    vc417.rel_creator = u10
    vc417.rel_to_comment = c139
    db.session.add(vc417)

    vc418 = VoteComment(
            is_up=True
        )
    vc418.rel_creator = u8
    vc418.rel_to_comment = c140
    db.session.add(vc418)

    vc419 = VoteComment(
            is_up=False
        )
    vc419.rel_creator = u9
    vc419.rel_to_comment = c140
    db.session.add(vc419)

    vc420 = VoteComment(
            is_up=True
        )
    vc420.rel_creator = u10
    vc420.rel_to_comment = c140
    db.session.add(vc420)

    vc421 = VoteComment(
            is_up=True
        )
    vc421.rel_creator = u1
    vc421.rel_to_comment = c141
    db.session.add(vc421)

    vc422 = VoteComment(
            is_up=False
        )
    vc422.rel_creator = u2
    vc422.rel_to_comment = c141
    db.session.add(vc422)

    vc423 = VoteComment(
            is_up=True
        )
    vc423.rel_creator = u3
    vc423.rel_to_comment = c141
    db.session.add(vc423)

    vc424 = VoteComment(
            is_up=False
        )
    vc424.rel_creator = u8
    vc424.rel_to_comment = c142
    db.session.add(vc424)

    vc425 = VoteComment(
            is_up=True
        )
    vc425.rel_creator = u9
    vc425.rel_to_comment = c142
    db.session.add(vc425)

    vc426 = VoteComment(
            is_up=True
        )
    vc426.rel_creator = u10
    vc426.rel_to_comment = c142
    db.session.add(vc426)

    vc427 = VoteComment(
            is_up=True
        )
    vc427.rel_creator = u8
    vc427.rel_to_comment = c143
    db.session.add(vc427)

    vc428 = VoteComment(
            is_up=True
        )
    vc428.rel_creator = u9
    vc428.rel_to_comment = c143
    db.session.add(vc428)

    vc429 = VoteComment(
            is_up=False
        )
    vc429.rel_creator = u10
    vc429.rel_to_comment = c143
    db.session.add(vc429)

    vc430 = VoteComment(
            is_up=False
        )
    vc430.rel_creator = u1
    vc430.rel_to_comment = c144
    db.session.add(vc430)

    vc431 = VoteComment(
            is_up=True
        )
    vc431.rel_creator = u2
    vc431.rel_to_comment = c144
    db.session.add(vc431)

    vc432 = VoteComment(
            is_up=True
        )
    vc432.rel_creator = u3
    vc432.rel_to_comment = c144
    db.session.add(vc432)

    vc433 = VoteComment(
            is_up=True
        )
    vc433.rel_creator = u8
    vc433.rel_to_comment = c145
    db.session.add(vc433)

    vc434 = VoteComment(
            is_up=True
        )
    vc434.rel_creator = u9
    vc434.rel_to_comment = c145
    db.session.add(vc434)

    vc435 = VoteComment(
            is_up=True
        )
    vc435.rel_creator = u10
    vc435.rel_to_comment = c145
    db.session.add(vc435)

    vc436 = VoteComment(
            is_up=True
        )
    vc436.rel_creator = u8
    vc436.rel_to_comment = c146
    db.session.add(vc436)

    vc437 = VoteComment(
            is_up=False
        )
    vc437.rel_creator = u9
    vc437.rel_to_comment = c146
    db.session.add(vc437)

    vc438 = VoteComment(
            is_up=True
        )
    vc438.rel_creator = u10
    vc438.rel_to_comment = c146
    db.session.add(vc438)

    vc439 = VoteComment(
            is_up=False
        )
    vc439.rel_creator = u1
    vc439.rel_to_comment = c147
    db.session.add(vc439)

    vc440 = VoteComment(
            is_up=True
        )
    vc440.rel_creator = u2
    vc440.rel_to_comment = c147
    db.session.add(vc440)

    vc441 = VoteComment(
            is_up=True
        )
    vc441.rel_creator = u3
    vc441.rel_to_comment = c147
    db.session.add(vc441)

    vc442 = VoteComment(
            is_up=True
        )
    vc442.rel_creator = u8
    vc442.rel_to_comment = c148
    db.session.add(vc442)

    vc443 = VoteComment(
            is_up=False
        )
    vc443.rel_creator = u9
    vc443.rel_to_comment = c148
    db.session.add(vc443)

    vc444 = VoteComment(
            is_up=True
        )
    vc444.rel_creator = u10
    vc444.rel_to_comment = c148
    db.session.add(vc444)

    vc445 = VoteComment(
            is_up=True
        )
    vc445.rel_creator = u8
    vc445.rel_to_comment = c149
    db.session.add(vc445)

    vc446 = VoteComment(
            is_up=False
        )
    vc446.rel_creator = u9
    vc446.rel_to_comment = c149
    db.session.add(vc446)

    vc447 = VoteComment(
            is_up=False
        )
    vc447.rel_creator = u10
    vc447.rel_to_comment = c149
    db.session.add(vc447)

    vc448 = VoteComment(
            is_up=True
        )
    vc448.rel_creator = u1
    vc448.rel_to_comment = c150
    db.session.add(vc448)

    vc449 = VoteComment(
            is_up=True
        )
    vc449.rel_creator = u2
    vc449.rel_to_comment = c150
    db.session.add(vc449)

    vc450 = VoteComment(
            is_up=True
        )
    vc450.rel_creator = u3
    vc450.rel_to_comment = c150
    db.session.add(vc450)

    vc451 = VoteComment(
            is_up=True
        )
    vc451.rel_creator = u8
    vc451.rel_to_comment = c151
    db.session.add(vc451)

    vc452 = VoteComment(
            is_up=True
        )
    vc452.rel_creator = u9
    vc452.rel_to_comment = c151
    db.session.add(vc452)

    vc453 = VoteComment(
            is_up=False
        )
    vc453.rel_creator = u10
    vc453.rel_to_comment = c151
    db.session.add(vc453)

    vc454 = VoteComment(
            is_up=False
        )
    vc454.rel_creator = u8
    vc454.rel_to_comment = c152
    db.session.add(vc454)

    vc455 = VoteComment(
            is_up=False
        )
    vc455.rel_creator = u9
    vc455.rel_to_comment = c152
    db.session.add(vc455)

    vc456 = VoteComment(
            is_up=True
        )
    vc456.rel_creator = u10
    vc456.rel_to_comment = c152
    db.session.add(vc456)

    vc457 = VoteComment(
            is_up=False
        )
    vc457.rel_creator = u1
    vc457.rel_to_comment = c153
    db.session.add(vc457)

    vc458 = VoteComment(
            is_up=False
        )
    vc458.rel_creator = u2
    vc458.rel_to_comment = c153
    db.session.add(vc458)

    vc459 = VoteComment(
            is_up=True
        )
    vc459.rel_creator = u3
    vc459.rel_to_comment = c153
    db.session.add(vc459)

    vc460 = VoteComment(
            is_up=True
        )
    vc460.rel_creator = u8
    vc460.rel_to_comment = c154
    db.session.add(vc460)

    vc461 = VoteComment(
            is_up=False
        )
    vc461.rel_creator = u9
    vc461.rel_to_comment = c154
    db.session.add(vc461)

    vc462 = VoteComment(
            is_up=True
        )
    vc462.rel_creator = u10
    vc462.rel_to_comment = c154
    db.session.add(vc462)

    vc463 = VoteComment(
            is_up=True
        )
    vc463.rel_creator = u8
    vc463.rel_to_comment = c155
    db.session.add(vc463)

    vc464 = VoteComment(
            is_up=True
        )
    vc464.rel_creator = u9
    vc464.rel_to_comment = c155
    db.session.add(vc464)

    vc465 = VoteComment(
            is_up=True
        )
    vc465.rel_creator = u10
    vc465.rel_to_comment = c155
    db.session.add(vc465)

    vc466 = VoteComment(
            is_up=False
        )
    vc466.rel_creator = u1
    vc466.rel_to_comment = c156
    db.session.add(vc466)

    vc467 = VoteComment(
            is_up=False
        )
    vc467.rel_creator = u2
    vc467.rel_to_comment = c156
    db.session.add(vc467)

    vc468 = VoteComment(
            is_up=False
        )
    vc468.rel_creator = u3
    vc468.rel_to_comment = c156
    db.session.add(vc468)

    vc469 = VoteComment(
            is_up=True
        )
    vc469.rel_creator = u8
    vc469.rel_to_comment = c157
    db.session.add(vc469)

    vc470 = VoteComment(
            is_up=False
        )
    vc470.rel_creator = u9
    vc470.rel_to_comment = c157
    db.session.add(vc470)

    vc471 = VoteComment(
            is_up=True
        )
    vc471.rel_creator = u10
    vc471.rel_to_comment = c157
    db.session.add(vc471)

    vc472 = VoteComment(
            is_up=True
        )
    vc472.rel_creator = u8
    vc472.rel_to_comment = c158
    db.session.add(vc472)

    vc473 = VoteComment(
            is_up=True
        )
    vc473.rel_creator = u9
    vc473.rel_to_comment = c158
    db.session.add(vc473)

    vc474 = VoteComment(
            is_up=False
        )
    vc474.rel_creator = u10
    vc474.rel_to_comment = c158
    db.session.add(vc474)

    vc475 = VoteComment(
            is_up=True
        )
    vc475.rel_creator = u1
    vc475.rel_to_comment = c159
    db.session.add(vc475)

    vc476 = VoteComment(
            is_up=True
        )
    vc476.rel_creator = u2
    vc476.rel_to_comment = c159
    db.session.add(vc476)

    vc477 = VoteComment(
            is_up=False
        )
    vc477.rel_creator = u3
    vc477.rel_to_comment = c159
    db.session.add(vc477)

    vc478 = VoteComment(
            is_up=True
        )
    vc478.rel_creator = u8
    vc478.rel_to_comment = c160
    db.session.add(vc478)

    vc479 = VoteComment(
            is_up=True
        )
    vc479.rel_creator = u9
    vc479.rel_to_comment = c160
    db.session.add(vc479)

    vc480 = VoteComment(
            is_up=False
        )
    vc480.rel_creator = u10
    vc480.rel_to_comment = c160
    db.session.add(vc480)

    vc481 = VoteComment(
            is_up=True
        )
    vc481.rel_creator = u8
    vc481.rel_to_comment = c161
    db.session.add(vc481)

    vc482 = VoteComment(
            is_up=False
        )
    vc482.rel_creator = u9
    vc482.rel_to_comment = c161
    db.session.add(vc482)

    vc483 = VoteComment(
            is_up=True
        )
    vc483.rel_creator = u10
    vc483.rel_to_comment = c161
    db.session.add(vc483)

    vc484 = VoteComment(
            is_up=False
        )
    vc484.rel_creator = u1
    vc484.rel_to_comment = c162
    db.session.add(vc484)

    vc485 = VoteComment(
            is_up=True
        )
    vc485.rel_creator = u2
    vc485.rel_to_comment = c162
    db.session.add(vc485)

    vc486 = VoteComment(
            is_up=False
        )
    vc486.rel_creator = u3
    vc486.rel_to_comment = c162
    db.session.add(vc486)

    vc487 = VoteComment(
            is_up=False
        )
    vc487.rel_creator = u8
    vc487.rel_to_comment = c163
    db.session.add(vc487)

    vc488 = VoteComment(
            is_up=False
        )
    vc488.rel_creator = u9
    vc488.rel_to_comment = c163
    db.session.add(vc488)

    vc489 = VoteComment(
            is_up=True
        )
    vc489.rel_creator = u10
    vc489.rel_to_comment = c163
    db.session.add(vc489)

    vc490 = VoteComment(
            is_up=True
        )
    vc490.rel_creator = u8
    vc490.rel_to_comment = c164
    db.session.add(vc490)

    vc491 = VoteComment(
            is_up=True
        )
    vc491.rel_creator = u9
    vc491.rel_to_comment = c164
    db.session.add(vc491)

    vc492 = VoteComment(
            is_up=False
        )
    vc492.rel_creator = u10
    vc492.rel_to_comment = c164
    db.session.add(vc492)

    vc493 = VoteComment(
            is_up=True
        )
    vc493.rel_creator = u1
    vc493.rel_to_comment = c165
    db.session.add(vc493)

    vc494 = VoteComment(
            is_up=True
        )
    vc494.rel_creator = u2
    vc494.rel_to_comment = c165
    db.session.add(vc494)

    vc495 = VoteComment(
            is_up=True
        )
    vc495.rel_creator = u3
    vc495.rel_to_comment = c165
    db.session.add(vc495)

    vc496 = VoteComment(
            is_up=True
        )
    vc496.rel_creator = u8
    vc496.rel_to_comment = c166
    db.session.add(vc496)

    vc497 = VoteComment(
            is_up=False
        )
    vc497.rel_creator = u9
    vc497.rel_to_comment = c166
    db.session.add(vc497)

    vc498 = VoteComment(
            is_up=True
        )
    vc498.rel_creator = u10
    vc498.rel_to_comment = c166
    db.session.add(vc498)

    vc499 = VoteComment(
            is_up=True
        )
    vc499.rel_creator = u8
    vc499.rel_to_comment = c167
    db.session.add(vc499)

    vc500 = VoteComment(
            is_up=True
        )
    vc500.rel_creator = u9
    vc500.rel_to_comment = c167
    db.session.add(vc500)

    vc501 = VoteComment(
            is_up=True
        )
    vc501.rel_creator = u10
    vc501.rel_to_comment = c167
    db.session.add(vc501)

    vc502 = VoteComment(
            is_up=False
        )
    vc502.rel_creator = u1
    vc502.rel_to_comment = c168
    db.session.add(vc502)

    vc503 = VoteComment(
            is_up=True
        )
    vc503.rel_creator = u2
    vc503.rel_to_comment = c168
    db.session.add(vc503)

    vc504 = VoteComment(
            is_up=True
        )
    vc504.rel_creator = u3
    vc504.rel_to_comment = c168
    db.session.add(vc504)

    vc505 = VoteComment(
            is_up=True
        )
    vc505.rel_creator = u8
    vc505.rel_to_comment = c169
    db.session.add(vc505)

    vc506 = VoteComment(
            is_up=False
        )
    vc506.rel_creator = u9
    vc506.rel_to_comment = c169
    db.session.add(vc506)

    vc507 = VoteComment(
            is_up=True
        )
    vc507.rel_creator = u10
    vc507.rel_to_comment = c169
    db.session.add(vc507)

    vc508 = VoteComment(
            is_up=False
        )
    vc508.rel_creator = u8
    vc508.rel_to_comment = c170
    db.session.add(vc508)

    vc509 = VoteComment(
            is_up=True
        )
    vc509.rel_creator = u9
    vc509.rel_to_comment = c170
    db.session.add(vc509)

    vc510 = VoteComment(
            is_up=True
        )
    vc510.rel_creator = u10
    vc510.rel_to_comment = c170
    db.session.add(vc510)

    vc511 = VoteComment(
            is_up=True
        )
    vc511.rel_creator = u1
    vc511.rel_to_comment = c171
    db.session.add(vc511)

    vc512 = VoteComment(
            is_up=True
        )
    vc512.rel_creator = u2
    vc512.rel_to_comment = c171
    db.session.add(vc512)

    vc513 = VoteComment(
            is_up=False
        )
    vc513.rel_creator = u3
    vc513.rel_to_comment = c171
    db.session.add(vc513)

    mts1 = MessageToStaff(
        text="text1",
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        replied=True
    )
    mts1.rel_sender = u1
    mts1.rel_topic = MessageTopic.query.filter(MessageTopic.topic == 'Endorsement').first()
    db.session.add(mts1)

    mts2 = MessageToStaff(
        text="text2",
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        replied=False
    )
    mts2.rel_sender = u1
    mts2.rel_topic = MessageTopic.query.filter(MessageTopic.topic == 'Other').first()
    db.session.add(mts2)

    mts3 = MessageToStaff(
        text="text3",
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        replied=False
    )
    mts3.rel_sender = u2
    mts3.rel_topic = MessageTopic.query.filter(MessageTopic.topic == 'Technical issues, corrections').first()
    db.session.add(mts3)

    # notification types
    nt_review_request = NotificationType.query.get(NotificationTypeEnum.REVIEW_REQUEST.value)

    # notifications
    n1 = Notification(
        datetime=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        title=Notification.prepare_title(nt_review_request),
        text='New review request',
        action_url=url_for('review_request_page', request_id=42)
    )
    n1.rel_notification_type = nt_review_request
    n1.rel_user = u1
    db.session.add(n1)

    n2 = Notification(
        datetime=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        title=Notification.prepare_title(nt_review_request),
        text='New review request',
        action_url=url_for('review_request_page', request_id=43)
    )
    n2.rel_notification_type = nt_review_request
    n2.rel_user = u2
    db.session.add(n2)

    n3 = Notification(
        datetime=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        title=Notification.prepare_title(nt_review_request),
        text='New review request',
        action_url=url_for('review_request_page', request_id=44)
    )
    n3.rel_notification_type = nt_review_request
    n3.rel_user = u3
    db.session.add(n3)

    # suggestions
    s1 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s1.rel_review = r1
    db.session.add(s1)

    s2 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s2.rel_review = r1
    db.session.add(s2)

    s3 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s3.rel_review = r1
    db.session.add(s3)

    s4 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s4.rel_review = r2
    db.session.add(s4)

    s5 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s5.rel_review = r2
    db.session.add(s5)

    s6 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s6.rel_review = r2
    db.session.add(s6)

    s7 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s7.rel_review = r3
    db.session.add(s7)

    s8 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s8.rel_review = r3
    db.session.add(s8)

    s9 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s9.rel_review = r3
    db.session.add(s9)

    s10 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s10.rel_review = r4
    db.session.add(s10)

    s11 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s11.rel_review = r4
    db.session.add(s11)

    s12 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s12.rel_review = r4
    db.session.add(s12)

    s13 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s13.rel_review = r5
    db.session.add(s13)

    s14 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s14.rel_review = r5
    db.session.add(s14)

    s15 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s15.rel_review = r5
    db.session.add(s15)

    s16 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s16.rel_review = r6
    db.session.add(s16)

    s17 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s17.rel_review = r6
    db.session.add(s17)

    s18 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s18.rel_review = r6
    db.session.add(s18)

    s19 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s19.rel_review = r7
    db.session.add(s19)

    s20 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s20.rel_review = r7
    db.session.add(s20)

    s21 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s21.rel_review = r7
    db.session.add(s21)

    s22 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s22.rel_review = r8
    db.session.add(s22)

    s23 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s23.rel_review = r8
    db.session.add(s23)

    s24 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s24.rel_review = r8
    db.session.add(s24)

    s25 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s25.rel_review = r9
    db.session.add(s25)

    s26 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s26.rel_review = r9
    db.session.add(s26)

    s27 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s27.rel_review = r9
    db.session.add(s27)

    s28 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s28.rel_review = r10
    db.session.add(s28)

    s29 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s29.rel_review = r10
    db.session.add(s29)

    s30 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s30.rel_review = r10
    db.session.add(s30)

    s31 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s31.rel_review = r11
    db.session.add(s31)

    s32 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s32.rel_review = r11
    db.session.add(s32)

    s33 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s33.rel_review = r11
    db.session.add(s33)

    s34 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s34.rel_review = r12
    db.session.add(s34)

    s35 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s35.rel_review = r12
    db.session.add(s35)

    s36 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s36.rel_review = r12
    db.session.add(s36)

    s37 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s37.rel_review = r13
    db.session.add(s37)

    s38 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s38.rel_review = r13
    db.session.add(s38)

    s39 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s39.rel_review = r13
    db.session.add(s39)

    s40 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s40.rel_review = r14
    db.session.add(s40)

    s41 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s41.rel_review = r14
    db.session.add(s41)

    s42 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s42.rel_review = r14
    db.session.add(s42)

    s43 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s43.rel_review = r15
    db.session.add(s43)

    s44 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s44.rel_review = r15
    db.session.add(s44)

    s45 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s45.rel_review = r15
    db.session.add(s45)

    s46 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s46.rel_review = r16
    db.session.add(s46)

    s47 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s47.rel_review = r16
    db.session.add(s47)

    s48 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s48.rel_review = r16
    db.session.add(s48)

    s49 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s49.rel_review = r17
    db.session.add(s49)

    s50 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s50.rel_review = r17
    db.session.add(s50)

    s51 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s51.rel_review = r17
    db.session.add(s51)

    s52 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s52.rel_review = r18
    db.session.add(s52)

    s53 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s53.rel_review = r18
    db.session.add(s53)

    s54 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s54.rel_review = r18
    db.session.add(s54)

    s55 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s55.rel_review = r19
    db.session.add(s55)

    s56 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s56.rel_review = r19
    db.session.add(s56)

    s57 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s57.rel_review = r19
    db.session.add(s57)

    s58 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s58.rel_review = r20
    db.session.add(s58)

    s59 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s59.rel_review = r20
    db.session.add(s59)

    s60 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s60.rel_review = r20
    db.session.add(s60)

    s61 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s61.rel_review = r21
    db.session.add(s61)

    s62 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s62.rel_review = r21
    db.session.add(s62)

    s63 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s63.rel_review = r21
    db.session.add(s63)

    s64 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s64.rel_review = r22
    db.session.add(s64)

    s65 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s65.rel_review = r22
    db.session.add(s65)

    s66 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s66.rel_review = r22
    db.session.add(s66)

    s67 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s67.rel_review = r23
    db.session.add(s67)

    s68 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s68.rel_review = r23
    db.session.add(s68)

    s69 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s69.rel_review = r23
    db.session.add(s69)

    s70 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s70.rel_review = r24
    db.session.add(s70)

    s71 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s71.rel_review = r24
    db.session.add(s71)

    s72 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s72.rel_review = r24
    db.session.add(s72)

    s73 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s73.rel_review = r25
    db.session.add(s73)

    s74 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s74.rel_review = r25
    db.session.add(s74)

    s75 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s75.rel_review = r25
    db.session.add(s75)

    s76 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s76.rel_review = r26
    db.session.add(s76)

    s77 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s77.rel_review = r26
    db.session.add(s77)

    s78 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s78.rel_review = r26
    db.session.add(s78)

    s79 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s79.rel_review = r27
    db.session.add(s79)

    s80 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s80.rel_review = r27
    db.session.add(s80)

    s81 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s81.rel_review = r27
    db.session.add(s81)

    s82 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s82.rel_review = r28
    db.session.add(s82)

    s83 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s83.rel_review = r28
    db.session.add(s83)

    s84 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s84.rel_review = r28
    db.session.add(s84)

    s85 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s85.rel_review = r29
    db.session.add(s85)

    s86 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s86.rel_review = r29
    db.session.add(s86)

    s87 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s87.rel_review = r29
    db.session.add(s87)

    s88 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s88.rel_review = r30
    db.session.add(s88)

    s89 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s89.rel_review = r30
    db.session.add(s89)

    s90 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s90.rel_review = r30
    db.session.add(s90)

    s91 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s91.rel_review = r31
    db.session.add(s91)

    s92 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s92.rel_review = r31
    db.session.add(s92)

    s93 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s93.rel_review = r31
    db.session.add(s93)

    s94 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s94.rel_review = r32
    db.session.add(s94)

    s95 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s95.rel_review = r32
    db.session.add(s95)

    s96 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s96.rel_review = r32
    db.session.add(s96)

    s97 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s97.rel_review = r33
    db.session.add(s97)

    s98 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s98.rel_review = r33
    db.session.add(s98)

    s99 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s99.rel_review = r33
    db.session.add(s99)

    s100 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s100.rel_review = r34
    db.session.add(s100)

    s101 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s101.rel_review = r34
    db.session.add(s101)

    s102 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s102.rel_review = r34
    db.session.add(s102)

    s103 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s103.rel_review = r35
    db.session.add(s103)

    s104 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s104.rel_review = r35
    db.session.add(s104)

    s105 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s105.rel_review = r35
    db.session.add(s105)

    s106 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s106.rel_review = r36
    db.session.add(s106)

    s107 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s107.rel_review = r36
    db.session.add(s107)

    s108 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s108.rel_review = r36
    db.session.add(s108)

    s109 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s109.rel_review = r37
    db.session.add(s109)

    s110 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s110.rel_review = r37
    db.session.add(s110)

    s111 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s111.rel_review = r37
    db.session.add(s111)

    s112 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s112.rel_review = r38
    db.session.add(s112)

    s113 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s113.rel_review = r38
    db.session.add(s113)

    s114 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s114.rel_review = r38
    db.session.add(s114)

    s115 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s115.rel_review = r39
    db.session.add(s115)

    s116 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s116.rel_review = r39
    db.session.add(s116)

    s117 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s117.rel_review = r39
    db.session.add(s117)

    s118 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s118.rel_review = r40
    db.session.add(s118)

    s119 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s119.rel_review = r40
    db.session.add(s119)

    s120 = Suggestion(
        suggestion="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus augue a "
                   "suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, luctus sed nulla a, "
                   "hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. Vestibulum posuere imperdiet "
                   "tincidunt. Pellentesque pellentesque nisi at velit dapibus, vel blandit mi maximus. Cras diam "
                   "sem, ultricies et quam vel, gravida sagittis dolor. Nam eu nunc nec orci euismod tincidunt. Nulla "
                   "nisl libero, aliquet ut ante sed, auctor aliquet mauris. Donec vel dapibus sem. Morbi eget "
                   "interdum felis, eu efficitur mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam "
                   "ante neque, consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut "
                   "massa sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                   "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    s120.rel_review = r40
    db.session.add(s120)

    # calibration papers
    cp1 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}16.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}16.pdf"),
    )
    cp1.rel_author = u1
    db.session.add(cp1)

    cp2 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}17.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}17.pdf"),
    )
    cp2.rel_author = u1
    db.session.add(cp2)

    cp3 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}18.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}18.pdf"),
    )
    cp3.rel_author = u1
    db.session.add(cp3)

    cp4 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}19.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}19.pdf"),
    )
    cp4.rel_author = u1
    db.session.add(cp4)

    cp5 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}20.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}20.pdf"),
    )
    cp5.rel_author = u1
    db.session.add(cp5)

    cp6 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}21.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}21.pdf"),
    )
    cp6.rel_author = u1
    db.session.add(cp6)

    cp7 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}22.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}22.pdf"),
    )
    cp7.rel_author = u1
    db.session.add(cp7)

    cp8 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}23.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}23.pdf"),
    )
    cp8.rel_author = u1
    db.session.add(cp8)

    cp9 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}24.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}24.pdf"),
    )
    cp9.rel_author = u1
    db.session.add(cp9)

    cp10 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}25.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}25.pdf"),
    )
    cp10.rel_author = u1
    db.session.add(cp10)

    cp11 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}26.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}26.pdf"),
    )
    cp11.rel_author = u1
    db.session.add(cp11)

    cp12 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}27.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}27.pdf"),
    )
    cp12.rel_author = u1
    db.session.add(cp12)

    cp13 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}28.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}28.pdf"),
    )
    cp13.rel_author = u1
    db.session.add(cp13)

    cp14 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}29.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}29.pdf"),
    )
    cp14.rel_author = u1
    db.session.add(cp14)

    cp15 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}30.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}30.pdf"),
    )
    cp15.rel_author = u1
    db.session.add(cp15)

    cp16 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}31.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}31.pdf"),
    )
    cp16.rel_author = u1
    db.session.add(cp16)

    cp17 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}32.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}32.pdf"),
    )
    cp17.rel_author = u1
    db.session.add(cp17)

    cp18 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}33.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}33.pdf"),
    )
    cp18.rel_author = u1
    db.session.add(cp18)

    cp19 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}34.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}34.pdf"),
    )
    cp19.rel_author = u1
    db.session.add(cp19)

    cp20 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}35.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}35.pdf"),
    )
    cp20.rel_author = u1
    db.session.add(cp20)

    cp21 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}36.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}36.pdf"),
    )
    cp21.rel_author = u1
    db.session.add(cp21)

    cp22 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}37.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}37.pdf"),
    )
    cp22.rel_author = u1
    db.session.add(cp22)

    cp23 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}38.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}38.pdf"),
    )
    cp23.rel_author = u1
    db.session.add(cp23)

    cp24 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}39.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}39.pdf"),
    )
    cp24.rel_author = u2
    db.session.add(cp24)

    cp25 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}40.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}40.pdf"),
    )
    cp25.rel_author = u2
    db.session.add(cp25)

    cp26 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}41.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}41.pdf"),
    )
    cp26.rel_author = u2
    db.session.add(cp26)

    cp27 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}42.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}42.pdf"),
    )
    cp27.rel_author = u2
    db.session.add(cp27)

    cp28 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}43.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}43.pdf"),
    )
    cp28.rel_author = u2
    db.session.add(cp28)

    cp29 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}44.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}44.pdf"),
    )
    cp29.rel_author = u2
    db.session.add(cp29)

    cp30 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}45.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}45.pdf"),
    )
    cp30.rel_author = u2
    db.session.add(cp30)

    cp31 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}46.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}46.pdf"),
    )
    cp31.rel_author = u2
    db.session.add(cp31)

    cp32 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}47.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}47.pdf"),
    )
    cp32.rel_author = u2
    db.session.add(cp32)

    cp33 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}48.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}48.pdf"),
    )
    cp33.rel_author = u2
    db.session.add(cp33)

    cp34 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}49.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}49.pdf"),
    )
    cp34.rel_author = u2
    db.session.add(cp34)

    cp35 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}50.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}50.pdf"),
    )
    cp35.rel_author = u2
    db.session.add(cp35)

    cp36 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}51.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}51.pdf"),
    )
    cp36.rel_author = u2
    db.session.add(cp36)

    cp37 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}52.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}52.pdf"),
    )
    cp37.rel_author = u2
    db.session.add(cp37)

    cp38 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}53.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}53.pdf"),
    )
    cp38.rel_author = u2
    db.session.add(cp38)

    cp39 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}54.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}54.pdf"),
    )
    cp39.rel_author = u2
    db.session.add(cp39)

    cp40 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}55.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}55.pdf"),
    )
    cp40.rel_author = u2
    db.session.add(cp40)

    cp41 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}56.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}56.pdf"),
    )
    cp41.rel_author = u2
    db.session.add(cp41)

    cp42 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}57.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}57.pdf"),
    )
    cp42.rel_author = u2
    db.session.add(cp42)

    cp43 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}58.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}58.pdf"),
    )
    cp43.rel_author = u2
    db.session.add(cp43)

    cp44 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}59.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}59.pdf"),
    )
    cp44.rel_author = u2
    db.session.add(cp44)

    cp45 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}60.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}60.pdf"),
    )
    cp45.rel_author = u2
    db.session.add(cp45)

    cp46 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}61.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}61.pdf"),
    )
    cp46.rel_author = u2
    db.session.add(cp46)

    cp47 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}62.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}62.pdf"),
    )
    cp47.rel_author = u3
    db.session.add(cp47)

    cp48 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}63.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}63.pdf"),
    )
    cp48.rel_author = u3
    db.session.add(cp48)

    cp49 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}64.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}64.pdf"),
    )
    cp49.rel_author = u3
    db.session.add(cp49)

    cp50 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}65.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}65.pdf"),
    )
    cp50.rel_author = u3
    db.session.add(cp50)

    cp51 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}66.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}66.pdf"),
    )
    cp51.rel_author = u3
    db.session.add(cp51)

    cp52 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}67.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}67.pdf"),
    )
    cp52.rel_author = u3
    db.session.add(cp52)

    cp53 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}68.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}68.pdf"),
    )
    cp53.rel_author = u3
    db.session.add(cp53)

    cp54 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}69.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}69.pdf"),
    )
    cp54.rel_author = u3
    db.session.add(cp54)

    cp55 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}70.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}70.pdf"),
    )
    cp55.rel_author = u3
    db.session.add(cp55)

    cp56 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}71.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}71.pdf"),
    )
    cp56.rel_author = u3
    db.session.add(cp56)

    cp57 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}72.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}72.pdf"),
    )
    cp57.rel_author = u3
    db.session.add(cp57)

    cp58 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}73.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}73.pdf"),
    )
    cp58.rel_author = u3
    db.session.add(cp58)

    cp59 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}74.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}74.pdf"),
    )
    cp59.rel_author = u3
    db.session.add(cp59)

    cp60 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}75.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}75.pdf"),
    )
    cp60.rel_author = u3
    db.session.add(cp60)

    cp61 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}76.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}76.pdf"),
    )
    cp61.rel_author = u3
    db.session.add(cp61)

    cp62 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}77.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}77.pdf"),
    )
    cp62.rel_author = u3
    db.session.add(cp62)

    cp63 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}78.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}78.pdf"),
    )
    cp63.rel_author = u3
    db.session.add(cp63)

    cp64 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}79.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}79.pdf"),
    )
    cp64.rel_author = u3
    db.session.add(cp64)

    cp65 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}80.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}80.pdf"),
    )
    cp65.rel_author = u3
    db.session.add(cp65)

    cp66 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}81.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}81.pdf"),
    )
    cp66.rel_author = u3
    db.session.add(cp66)

    cp67 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}82.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}82.pdf"),
    )
    cp67.rel_author = u3
    db.session.add(cp67)

    cp68 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}83.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}83.pdf"),
    )
    cp68.rel_author = u3
    db.session.add(cp68)

    cp69 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}84.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}84.pdf"),
    )
    cp69.rel_author = u3
    db.session.add(cp69)

    cp70 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}85.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}85.pdf"),
    )
    cp70.rel_author = u4
    db.session.add(cp70)

    cp71 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}86.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}86.pdf"),
    )
    cp71.rel_author = u4
    db.session.add(cp71)

    cp72 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}87.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}87.pdf"),
    )
    cp72.rel_author = u4
    db.session.add(cp72)

    cp73 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}88.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}88.pdf"),
    )
    cp73.rel_author = u4
    db.session.add(cp73)

    cp74 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}89.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}89.pdf"),
    )
    cp74.rel_author = u4
    db.session.add(cp74)

    cp75 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}90.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}90.pdf"),
    )
    cp75.rel_author = u4
    db.session.add(cp75)

    cp76 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}91.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}91.pdf"),
    )
    cp76.rel_author = u4
    db.session.add(cp76)

    cp77 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}92.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}92.pdf"),
    )
    cp77.rel_author = u4
    db.session.add(cp77)

    cp78 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}93.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}93.pdf"),
    )
    cp78.rel_author = u4
    db.session.add(cp78)

    cp79 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}94.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}94.pdf"),
    )
    cp79.rel_author = u4
    db.session.add(cp79)

    cp80 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}95.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}95.pdf"),
    )
    cp80.rel_author = u4
    db.session.add(cp80)

    cp81 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}96.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}96.pdf"),
    )
    cp81.rel_author = u4
    db.session.add(cp81)

    cp82 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}97.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}97.pdf"),
    )
    cp82.rel_author = u4
    db.session.add(cp82)

    cp83 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}98.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}98.pdf"),
    )
    cp83.rel_author = u4
    db.session.add(cp83)

    cp84 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}99.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}99.pdf"),
    )
    cp84.rel_author = u4
    db.session.add(cp84)

    cp85 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}100.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}100.pdf"),
    )
    cp85.rel_author = u4
    db.session.add(cp85)

    cp86 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}101.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}101.pdf"),
    )
    cp86.rel_author = u4
    db.session.add(cp86)

    cp87 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}102.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}102.pdf"),
    )
    cp87.rel_author = u4
    db.session.add(cp87)

    cp88 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}103.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}103.pdf"),
    )
    cp88.rel_author = u4
    db.session.add(cp88)

    cp89 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}104.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}104.pdf"),
    )
    cp89.rel_author = u4
    db.session.add(cp89)

    cp90 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}105.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}105.pdf"),
    )
    cp90.rel_author = u4
    db.session.add(cp90)

    cp91 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}106.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}106.pdf"),
    )
    cp91.rel_author = u4
    db.session.add(cp91)

    cp92 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}107.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}107.pdf"),
    )
    cp92.rel_author = u4
    db.session.add(cp92)

    cp93 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}108.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}108.pdf"),
    )
    cp93.rel_author = u5
    db.session.add(cp93)

    cp94 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}109.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}109.pdf"),
    )
    cp94.rel_author = u5
    db.session.add(cp94)

    cp95 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}110.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}110.pdf"),
    )
    cp95.rel_author = u5
    db.session.add(cp95)

    cp96 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}111.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}111.pdf"),
    )
    cp96.rel_author = u5
    db.session.add(cp96)

    cp97 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}112.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}112.pdf"),
    )
    cp97.rel_author = u5
    db.session.add(cp97)

    cp98 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}113.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}113.pdf"),
    )
    cp98.rel_author = u5
    db.session.add(cp98)

    cp99 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}114.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}114.pdf"),
    )
    cp99.rel_author = u5
    db.session.add(cp99)

    cp100 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}115.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}115.pdf"),
    )
    cp100.rel_author = u5
    db.session.add(cp100)

    cp101 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}116.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}116.pdf"),
    )
    cp101.rel_author = u5
    db.session.add(cp101)

    cp102 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}117.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}117.pdf"),
    )
    cp102.rel_author = u5
    db.session.add(cp102)

    cp103 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}118.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}118.pdf"),
    )
    cp103.rel_author = u5
    db.session.add(cp103)

    cp104 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}119.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}119.pdf"),
    )
    cp104.rel_author = u5
    db.session.add(cp104)

    cp105 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}120.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}120.pdf"),
    )
    cp105.rel_author = u5
    db.session.add(cp105)

    cp106 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}121.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}121.pdf"),
    )
    cp106.rel_author = u5
    db.session.add(cp106)

    cp107 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}122.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}122.pdf"),
    )
    cp107.rel_author = u5
    db.session.add(cp107)

    cp108 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}123.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}123.pdf"),
    )
    cp108.rel_author = u5
    db.session.add(cp108)

    cp109 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}124.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}124.pdf"),
    )
    cp109.rel_author = u5
    db.session.add(cp109)

    cp110 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}125.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}125.pdf"),
    )
    cp110.rel_author = u5
    db.session.add(cp110)

    cp111 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}126.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}126.pdf"),
    )
    cp111.rel_author = u5
    db.session.add(cp111)

    cp112 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}127.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}127.pdf"),
    )
    cp112.rel_author = u5
    db.session.add(cp112)

    cp113 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}128.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}128.pdf"),
    )
    cp113.rel_author = u5
    db.session.add(cp113)

    cp114 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}129.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}129.pdf"),
    )
    cp114.rel_author = u5
    db.session.add(cp114)

    cp115 = CalibrationPaper(
        pdf_url=f"{app.config['PDFS_FOLDER_URL']}130.pdf",
        preprocessed_text=get_text(f"{app.config['PDFS_FOLDER_FULL_URL']}130.pdf"),
    )
    cp115.rel_author = u5
    db.session.add(cp115)

    # revision changes components
    rcc1 = RevisionChangesComponent(
        change_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus "
                           "augue a suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, "
                           "luctus sed nulla a, hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. "
                           "Vestibulum posuere imperdiet tincidunt. Pellentesque pellentesque nisi at velit dapibus, "
                           "vel blandit mi maximus. Cras diam sem, ultricies et quam vel, gravida sagittis dolor. Nam "
                           "eu nunc nec orci euismod tincidunt. Nulla nisl libero, aliquet ut ante sed, "
                           "auctor aliquet mauris. Donec vel dapibus sem. Morbi eget interdum felis, eu efficitur "
                           "mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam ante neque, "
                           "consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut massa "
                           "sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                           "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    rcc1.rel_paper_revision = pve1_2
    db.session.add(rcc1)

    rcc2 = RevisionChangesComponent(
        change_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus "
                           "augue a suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, "
                           "luctus sed nulla a, hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. "
                           "Vestibulum posuere imperdiet tincidunt. Pellentesque pellentesque nisi at velit dapibus, "
                           "vel blandit mi maximus. Cras diam sem, ultricies et quam vel, gravida sagittis dolor. Nam "
                           "eu nunc nec orci euismod tincidunt. Nulla nisl libero, aliquet ut ante sed, "
                           "auctor aliquet mauris. Donec vel dapibus sem. Morbi eget interdum felis, eu efficitur "
                           "mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam ante neque, "
                           "consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut massa "
                           "sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                           "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    rcc2.rel_paper_revision = pve1_2
    db.session.add(rcc2)

    rcc3 = RevisionChangesComponent(
        change_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus "
                           "augue a suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, "
                           "luctus sed nulla a, hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. "
                           "Vestibulum posuere imperdiet tincidunt. Pellentesque pellentesque nisi at velit dapibus, "
                           "vel blandit mi maximus. Cras diam sem, ultricies et quam vel, gravida sagittis dolor. Nam "
                           "eu nunc nec orci euismod tincidunt. Nulla nisl libero, aliquet ut ante sed, "
                           "auctor aliquet mauris. Donec vel dapibus sem. Morbi eget interdum felis, eu efficitur "
                           "mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam ante neque, "
                           "consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut massa "
                           "sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                           "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    rcc3.rel_paper_revision = pve1_2
    db.session.add(rcc3)

    rcc4 = RevisionChangesComponent(
        change_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus "
                           "augue a suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, "
                           "luctus sed nulla a, hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. "
                           "Vestibulum posuere imperdiet tincidunt. Pellentesque pellentesque nisi at velit dapibus, "
                           "vel blandit mi maximus. Cras diam sem, ultricies et quam vel, gravida sagittis dolor. Nam "
                           "eu nunc nec orci euismod tincidunt. Nulla nisl libero, aliquet ut ante sed, "
                           "auctor aliquet mauris. Donec vel dapibus sem. Morbi eget interdum felis, eu efficitur "
                           "mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam ante neque, "
                           "consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut massa "
                           "sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                           "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    rcc4.rel_paper_revision = pve1_3
    db.session.add(rcc4)

    rcc5 = RevisionChangesComponent(
        change_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus "
                           "augue a suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, "
                           "luctus sed nulla a, hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. "
                           "Vestibulum posuere imperdiet tincidunt. Pellentesque pellentesque nisi at velit dapibus, "
                           "vel blandit mi maximus. Cras diam sem, ultricies et quam vel, gravida sagittis dolor. Nam "
                           "eu nunc nec orci euismod tincidunt. Nulla nisl libero, aliquet ut ante sed, "
                           "auctor aliquet mauris. Donec vel dapibus sem. Morbi eget interdum felis, eu efficitur "
                           "mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam ante neque, "
                           "consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut massa "
                           "sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                           "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    rcc5.rel_paper_revision = pve1_3
    db.session.add(rcc5)

    rcc6 = RevisionChangesComponent(
        change_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus "
                           "augue a suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, "
                           "luctus sed nulla a, hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. "
                           "Vestibulum posuere imperdiet tincidunt. Pellentesque pellentesque nisi at velit dapibus, "
                           "vel blandit mi maximus. Cras diam sem, ultricies et quam vel, gravida sagittis dolor. Nam "
                           "eu nunc nec orci euismod tincidunt. Nulla nisl libero, aliquet ut ante sed, "
                           "auctor aliquet mauris. Donec vel dapibus sem. Morbi eget interdum felis, eu efficitur "
                           "mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam ante neque, "
                           "consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut massa "
                           "sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                           "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    rcc6.rel_paper_revision = pve1_3
    db.session.add(rcc6)

    rcc7 = RevisionChangesComponent(
        change_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus "
                           "augue a suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, "
                           "luctus sed nulla a, hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. "
                           "Vestibulum posuere imperdiet tincidunt. Pellentesque pellentesque nisi at velit dapibus, "
                           "vel blandit mi maximus. Cras diam sem, ultricies et quam vel, gravida sagittis dolor. Nam "
                           "eu nunc nec orci euismod tincidunt. Nulla nisl libero, aliquet ut ante sed, "
                           "auctor aliquet mauris. Donec vel dapibus sem. Morbi eget interdum felis, eu efficitur "
                           "mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam ante neque, "
                           "consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut massa "
                           "sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                           "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    rcc7.rel_paper_revision = pve15_2
    db.session.add(rcc7)

    rcc8 = RevisionChangesComponent(
        change_description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum imperdiet dapibus "
                           "augue a suscipit. Proin ullamcorper nunc in feugiat porttitor. Curabitur risus dolor, "
                           "luctus sed nulla a, hendrerit blandit tortor. Ut consectetur fermentum diam in egestas. "
                           "Vestibulum posuere imperdiet tincidunt. Pellentesque pellentesque nisi at velit dapibus, "
                           "vel blandit mi maximus. Cras diam sem, ultricies et quam vel, gravida sagittis dolor. Nam "
                           "eu nunc nec orci euismod tincidunt. Nulla nisl libero, aliquet ut ante sed, "
                           "auctor aliquet mauris. Donec vel dapibus sem. Morbi eget interdum felis, eu efficitur "
                           "mauris. Pellentesque faucibus et dolor tincidunt tincidunt. Etiam ante neque, "
                           "consequat in bibendum nec, pulvinar eget turpis. Integer dui tellus, lobortis ut massa "
                           "sed, ornare porta massa. Praesent a quam tristique, facilisis turpis eget, rhoncus nunc. "
                           "Etiam commodo tortor sit amet vulputate bibendum.",
        location="Page1"
    )
    rcc8.rel_paper_revision = pve15_2
    db.session.add(rcc8)

    # red flags
    rfc1 = RedFlagComment()
    rfc1.rel_creator = u1
    rfc1.rel_to_comment = c1
    db.session.add(rfc1)

    rfc2 = RedFlagComment()
    rfc2.rel_creator = u2
    rfc2.rel_to_comment = c2
    db.session.add(rfc2)

    rfc3 = RedFlagComment()
    rfc3.rel_creator = u3
    rfc3.rel_to_comment = c3
    db.session.add(rfc3)

    rfpv1 = RedFlagPaperRevision()
    rfpv1.rel_creator = u1
    rfpv1.rel_to_paper_revision = pve1_1
    db.session.add(rfpv1)

    rfpv2 = RedFlagPaperRevision()
    rfpv2.rel_creator = u2
    rfpv2.rel_to_paper_revision = pve1_2
    db.session.add(rfpv2)

    rfpv3 = RedFlagPaperRevision()
    rfpv3.rel_creator = u3
    rfpv3.rel_to_paper_revision = pve1_3
    db.session.add(rfpv3)

    rfr1 = RedFlagReview()
    rfr1.rel_creator = u1
    rfr1.rel_to_review = r1
    db.session.add(rfr1)

    rfr2 = RedFlagReview()
    rfr2.rel_creator = u2
    rfr2.rel_to_review = r2
    db.session.add(rfr2)

    rfr3 = RedFlagReview()
    rfr3.rel_creator = u3
    rfr3.rel_to_review = r3
    db.session.add(rfr3)

    rft1 = RedFlagTag()
    rft1.rel_creator = u1
    rft1.rel_to_tag = t1
    db.session.add(rft1)

    rft2 = RedFlagTag()
    rft2.rel_creator = u2
    rft2.rel_to_tag = t2
    db.session.add(rft2)

    rft3 = RedFlagTag()
    rft3.rel_creator = u3
    rft3.rel_to_tag = t3
    db.session.add(rft3)

    rfu1 = RedFlagUser()
    rfu1.rel_creator = u1
    rfu1.rel_to_user = u2
    db.session.add(rfu1)

    rfu3 = RedFlagUser()
    rfu3.rel_creator = u3
    rfu3.rel_to_user = u1
    db.session.add(rfu3)

    rfu4 = RedFlagUser()
    rfu4.rel_creator = u2
    rfu4.rel_to_user = u1
    db.session.add(rfu4)

    db.session.commit()

    return True
