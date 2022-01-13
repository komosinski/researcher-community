from open_science.models import *
import datetime as dt
from flask import url_for


def create_test_data():
    create_essential_data()

    # check if the test data has been created
    if PaperRevision.query.all():
        return False

    c1 = Comment(
        text="text1",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime.utcnow()
    )
    db.session.add(c1)

    c2 = Comment(
        text="text2",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime.utcnow()
    )
    db.session.add(c2)

    c3 = Comment(
        text="text3",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime.utcnow()
    )
    db.session.add(c3)

    c4 = Comment(
        text="text4",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime.utcnow()
    )
    db.session.add(c4)

    c5 = Comment(
        text="text5",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime.utcnow()
    )
    db.session.add(c5)

    c6 = Comment(
        text="text6",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime.utcnow()
    )
    db.session.add(c6)

    c7 = Comment(
        text="text7",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime.utcnow()
    )
    db.session.add(c7)

    c8 = Comment(
        text="text8",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime.utcnow()
    )
    db.session.add(c8)

    c9 = Comment(
        text="text9",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime.utcnow()
    )
    db.session.add(c9)

    c10 = Comment(
        text="text10",
        votes_score=0,
        red_flags_count=0,
        level=1,
        date=dt.datetime.utcnow()
    )
    c10.rel_related_comment = [c1]
    db.session.add(c10)

    c11 = Comment(
        text="text11",
        votes_score=0,
        red_flags_count=0,
        level=1,
        date=dt.datetime.utcnow()
    )
    c11.rel_related_comment = [c2]
    db.session.add(c11)

    c12 = Comment(
        text="text12",
        votes_score=0,
        red_flags_count=0,
        level=1,
        date=dt.datetime.utcnow()
    )
    c12.rel_related_comment = [c2]
    db.session.add(c12)

    r1 = Review()
    r1.rel_comments_to_this_review = [c4, c5]
    db.session.add(r1)

    r2 = Review(
        weight=2.2,
        review_score=5,
        publication_datetime=dt.datetime.utcnow(),
        is_hidden = False,
        red_flags_count=0
    )
    r2.rel_comments_to_this_review = [c6]
    db.session.add(r2)

    r3 = Review(
        weight=3.3,
        review_score=5,
        publication_datetime=dt.datetime.utcnow(),
        is_hidden = False,
        red_flags_count=0
    )
    db.session.add(r3)

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

    pve1_1 = PaperRevision(
        version=1,
        pdf_url="https://paperurl1.com",
        title="title1.1",
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve1_1.rel_related_comments = [c1, c2]
    pve1_1.rel_related_reviews = [r1]
    pve1_1.rel_parent_paper = p1
    db.session.add(pve1_1)

    pve1_2 = PaperRevision(
        pdf_url="https://paperurl1_2.com",
        title="title1.2",
        version=2,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve1_2.rel_related_comments = [c3, c4]
    pve1_2.rel_related_reviews = [r2]
    pve1_2.rel_parent_paper = p1
    db.session.add(pve1_2)

    pve1_3 = PaperRevision(
        pdf_url="https://paperurl1_3.com",
        title="title1.3",
        version=3,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve1_3.rel_related_comments = [c5, c6, c7, c8, c9]
    pve1_3.rel_related_reviews = [r3]
    pve1_3.rel_parent_paper = p1
    db.session.add(pve1_3)

    pve2 = PaperRevision(
        pdf_url="https://paperurl2.com",
        title="title2",
        version=1,
        abstract="description2 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve2.rel_parent_paper = p2
    db.session.add(pve2)

    pve3 = PaperRevision(
        pdf_url="https://paperurl3.com",
        title="title3",
        version=1,
        abstract="description3 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=3,
        red_flags_count=0
    )
    pve3.rel_parent_paper = p3
    db.session.add(pve3)

    pve4 = PaperRevision(
        pdf_url="https://paperurl4.com",
        title="title4",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=3,
        red_flags_count=0
    )
    pve4.rel_parent_paper = p4
    db.session.add(pve4)

    pve5 = PaperRevision(
        pdf_url="https://paperurl5.com",
        title="title5",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve5.rel_parent_paper = p5
    db.session.add(pve5)

    pve6 = PaperRevision(
        pdf_url="https://paperurl6.com",
        title="title6",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve6.rel_parent_paper = p6
    db.session.add(pve6)

    pve7 = PaperRevision(
        pdf_url="https://paperurl7.com",
        title="title7",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve7.rel_parent_paper = p7
    db.session.add(pve7)

    pve8 = PaperRevision(
        pdf_url="https://paperurl8.com",
        title="title8",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve8.rel_parent_paper = p8
    db.session.add(pve8)

    pve9 = PaperRevision(
        pdf_url="https://paperurl9.com",
        title="title9",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve9.rel_parent_paper = p9
    db.session.add(pve9)

    pve10 = PaperRevision(
        pdf_url="https://paperurl10.com",
        title="title10",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve10.rel_parent_paper = p10
    db.session.add(pve10)

    pve11 = PaperRevision(
        pdf_url="https://paperurl11.com",
        title="title11",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve11.rel_parent_paper = p11
    db.session.add(pve11)

    pve12 = PaperRevision(
        pdf_url="https://paperurl12.com",
        title="title12",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve12.rel_parent_paper = p12
    db.session.add(pve12)

    pve13 = PaperRevision(
        pdf_url="https://paperurl13.com",
        title="title13",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve13.rel_parent_paper = p13
    db.session.add(pve13)

    pve14 = PaperRevision(
        pdf_url="https://paperurl14.com",
        title="title14",
        version=1,
        abstract="description14 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve14.rel_parent_paper = p14
    db.session.add(pve14)

    pve15 = PaperRevision(
        pdf_url="https://paperurl15.com",
        title="title15",
        version=1,
        abstract="description15 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow(),
        confidence_level=1,
        red_flags_count=0
    )
    pve15.rel_parent_paper = p15
    db.session.add(pve15)

    # to read Papers' id from autoincrement
    db.session.flush()

    t1 = Tag(
        name="tag1",
        description="description1",
        deadline=dt.datetime.utcnow(),
        red_flags_count=0
    )
    t1.rel_related_paper_revisions = [pve1_1, pve1_2]
    db.session.add(t1)

    t2 = Tag(
        name="tag2",
        description="Description2",
        deadline=dt.datetime.utcnow(),
        red_flags_count=0
    )
    db.session.add(t2)

    t3 = Tag(
        name="tag3",
        description="DEscription3",
        deadline=dt.datetime.utcnow(),
        red_flags_count=0
    )
    t3.rel_related_paper_revisions = [pve1_1, pve6, pve7, pve8]
    db.session.add(t3)

    u1 = User(
        first_name="first_name1",
        second_name="second_name1",
        email="email1@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime.utcnow(),
        affiliation="affiliation1",
        orcid="0000000218250097",
        google_scholar="https://scholar.google.com/profil1",
        about_me="about_me1",
        personal_website="https://personalwebsite1.com",
        review_mails_limit=1,
        notifications_frequency=7,
        last_seen=dt.datetime.utcnow(),
        weight=1.1,
        registered_on=dt.datetime.utcnow(),
        red_flags_count=0
    )
    u1.rel_created_paper_revisions = [pve1_1, pve1_2, pve4, pve5, pve6, pve7, pve8, pve9]
    u1.rel_tags_to_user = [t1, t2]
    u1.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.RESEARCHER_USER.value).first()
    u1.rel_created_tags = [t3]
    u1.rel_created_reviews = [r1, r2]
    u1.rel_created_comments = [c1, c4, c7, c10]
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
        first_name="first_name2",
        second_name="second_name2",
        email="email2@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime.utcnow(),
        affiliation="affiliation2",
        orcid="0000000218250097",
        google_scholar="https://scholar.google.com/profil2",
        about_me="about_me2",
        personal_website="https://personalwebsite2.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=2.2,
        registered_on=dt.datetime.utcnow(),
        red_flags_count=0
    )
    u2.rel_created_paper_revisions = [pve14, pve15, pve12, pve13, pve3, pve2, pve1_3, pve10, pve11, pve4, pve5]
    u2.rel_tags_to_user = [t3]
    u2.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.RESEARCHER_USER.value).first()
    u2.rel_created_tags = [t1, t2]
    u2.rel_created_reviews = [r3]
    u2.rel_created_comments = [c2, c5, c8, c11]
    db.session.add(u2)

    p3.rel_creators = [u2]
    p10.rel_creators = [u2]
    p11.rel_creators = [u1, u2]

    u3 = User(
        first_name="first_name3",
        second_name="second_name3",
        email="email3@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime.utcnow(),
        affiliation="affiliation3",
        orcid="0000000218250097",
        google_scholar="https://scholar.google.com/profil3",
        about_me="about_me3",
        personal_website="https://personalwebsite3.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=3.3,
        registered_on=dt.datetime.utcnow(),
        red_flags_count=0
    )
    u3.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.STANDARD_USER.value).first()
    u3.rel_created_comments = [c3, c6, c9, c12]
    db.session.add(u3)

    u4 = User(
        first_name="unconfirm_name4",
        second_name="unconfirm_name4",
        email="email4@email.com",
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
        registered_on=dt.datetime.utcnow(),
        red_flags_count=0
    )
    u4.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.STANDARD_USER.value).first()
    db.session.add(u4)

    u5 = User(
        first_name="admin_name",
        second_name="admin_second_name",
        email="email5@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime.utcnow(),
        affiliation="",
        orcid="",
        google_scholar="",
        about_me="",
        personal_website="",
        review_mails_limit=0,
        notifications_frequency=0,
        weight=5.5,
        registered_on=dt.datetime.utcnow(),
        red_flags_count=0
    )
    u5.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.ADMIN.value).first()
    db.session.add(u5)

    rr1 = ReviewRequest(
        creation_datetime=dt.datetime.utcnow()
    )

    rr1.rel_requested_user = u1
    rr1.rel_related_paper_version = pve1_1
    db.session.add(rr1)

    rr2 = ReviewRequest(
        creation_datetime=dt.datetime.utcnow()
    )
    rr2.rel_requested_user = u2
    rr2.rel_related_paper_version = pve1_1
    db.session.add(rr2)

    rr3 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime.utcnow(),
        acceptation_date=dt.datetime.utcnow().date(),
        deadline_date=dt.datetime.utcnow().date()
    )
    rr3.rel_requested_user = u3
    rr3.rel_related_paper_version = pve1_1
    db.session.add(rr3)

    # TODO: check logic. initially decision is None
    # rr4 = ReviewRequest(
    #     decision=False,
    #     creation_datetime=dt.datetime.utcnow(),
    #     acceptation_date=dt.datetime.utcnow().date(),
    #     deadline_date=dt.datetime.utcnow().date()
    # )

    # rr4.rel_requested_user = u4
    # rr4.rel_related_paper_version = pve4
    # db.session.add(rr4)

    # rr5 = ReviewRequest(
    #     decision=False,
    #     creation_datetime=dt.datetime.utcnow(),
    #     acceptation_date=dt.datetime.utcnow().date(),
    #     deadline_date=dt.datetime.utcnow().date()
    # )

    # rr5.rel_requested_user = u5
    # rr5.rel_related_paper_version = pve5
    # db.session.add(rr5)

    # rr6 = ReviewRequest(
    #     decision=False,
    #     creation_datetime=dt.datetime.utcnow(),
    #     acceptation_date=dt.datetime.utcnow().date(),
    #     deadline_date=dt.datetime.utcnow().date()
    # )

    # rr6.rel_requested_user = u1
    # rr6.rel_related_paper_version = pve6
    # db.session.add(rr6)

    # rr7 = ReviewRequest(
    #     decision=False,
    #     creation_datetime=dt.datetime.utcnow(),
    #     acceptation_date=dt.datetime.utcnow().date(),
    #     deadline_date=dt.datetime.utcnow().date()
    # )

    # rr7.rel_requested_user = u2
    # rr7.rel_related_paper_version = pve7
    # db.session.add(rr7)

    # rr8 = ReviewRequest(
    #     decision=True,
    #     creation_datetime=dt.datetime.utcnow(),
    #     acceptation_date=dt.datetime.utcnow().date(),
    #     deadline_date=dt.datetime.utcnow().date()
    # )
    # rr8.rel_requested_user = u3
    # rr8.rel_related_paper_version = pve8
    # db.session.add(rr8)

    # rr9 = ReviewRequest(
    #     decision=True,
    #     creation_datetime=dt.datetime.utcnow(),
    #     acceptation_date=dt.datetime.utcnow().date(),
    #     deadline_date=dt.datetime.utcnow().date()
    # )
    # rr9.rel_requested_user = u4
    # rr9.rel_related_paper_version = pve9
    # db.session.add(rr9)

    # rr10 = ReviewRequest(
    #     decision=True,
    #     creation_datetime=dt.datetime.utcnow(),
    #     acceptation_date=dt.datetime.utcnow().date(),
    #     deadline_date=dt.datetime.utcnow().date()
    # )
    # rr10.rel_requested_user = u5
    # rr10.rel_related_paper_version = pve10
    # db.session.add(rr10)

    vc1 = VoteComment(
        is_up=False
    )
    vc1.rel_creator = u1
    vc1.rel_to_comment = c2
    db.session.add(vc1)

    vc2 = VoteComment(
        is_up=True
    )
    vc2.rel_creator = u1
    vc2.rel_to_comment = c3
    db.session.add(vc2)

    vc3 = VoteComment(
        is_up=True
    )
    vc3.rel_creator = u1
    vc3.rel_to_comment = c5
    db.session.add(vc3)

    vc4 = VoteComment(
        is_up=True
    )
    vc4.rel_creator = u1
    vc4.rel_to_comment = c6
    db.session.add(vc4)

    vc5 = VoteComment(
        is_up=True
    )
    vc5.rel_creator = u1
    vc5.rel_to_comment = c8
    db.session.add(vc5)

    vc6 = VoteComment(
        is_up=True
    )
    vc6.rel_creator = u1
    vc6.rel_to_comment = c9
    db.session.add(vc6)

    vc7 = VoteComment(
        is_up=True
    )
    vc7.rel_creator = u1
    vc7.rel_to_comment = c11
    db.session.add(vc7)

    vc8 = VoteComment(
        is_up=True
    )
    vc8.rel_creator = u1
    vc8.rel_to_comment = c12
    db.session.add(vc8)

    vc9 = VoteComment(
        is_up=False
    )
    vc9.rel_creator = u2
    vc9.rel_to_comment = c1
    db.session.add(vc9)

    vc10 = VoteComment(
        is_up=False
    )
    vc10.rel_creator = u2
    vc10.rel_to_comment = c3
    db.session.add(vc10)

    vc11 = VoteComment(
        is_up=False
    )
    vc11.rel_creator = u2
    vc11.rel_to_comment = c4
    db.session.add(vc11)

    vc12 = VoteComment(
        is_up=True
    )
    vc12.rel_creator = u2
    vc12.rel_to_comment = c6
    db.session.add(vc12)

    vc13 = VoteComment(
        is_up=True
    )
    vc13.rel_creator = u2
    vc13.rel_to_comment = c7
    db.session.add(vc13)

    vc14 = VoteComment(
        is_up=True
    )
    vc14.rel_creator = u2
    vc14.rel_to_comment = c9
    db.session.add(vc14)

    vc15 = VoteComment(
        is_up=True
    )
    vc15.rel_creator = u2
    vc15.rel_to_comment = c10
    db.session.add(vc15)

    vc16 = VoteComment(
        is_up=True
    )
    vc16.rel_creator = u2
    vc16.rel_to_comment = c12
    db.session.add(vc16)

    vc17 = VoteComment(
        is_up=False
    )
    vc17.rel_creator = u3
    vc17.rel_to_comment = c1
    db.session.add(vc17)

    vc18 = VoteComment(
        is_up=False
    )
    vc18.rel_creator = u3
    vc18.rel_to_comment = c2
    db.session.add(vc18)

    vc19 = VoteComment(
        is_up=False
    )
    vc19.rel_creator = u3
    vc19.rel_to_comment = c4
    db.session.add(vc19)

    vc20 = VoteComment(
        is_up=False
    )
    vc20.rel_creator = u3
    vc20.rel_to_comment = c5
    db.session.add(vc20)

    vc21 = VoteComment(
        is_up=False
    )
    vc21.rel_creator = u3
    vc21.rel_to_comment = c7
    db.session.add(vc21)

    vc22 = VoteComment(
        is_up=False
    )
    vc22.rel_creator = u3
    vc22.rel_to_comment = c8
    db.session.add(vc22)

    vc23 = VoteComment(
        is_up=True
    )
    vc23.rel_creator = u3
    vc23.rel_to_comment = c10
    db.session.add(vc23)

    vc24 = VoteComment(
        is_up=True
    )
    vc24.rel_creator = u3
    vc24.rel_to_comment = c11
    db.session.add(vc24)

    mts1 = MessageToStaff(
        text="text1",
        date=dt.datetime.utcnow(),
        replied=True
    )
    mts1.rel_sender = u1
    mts1.rel_topic = MessageTopic.query.filter(MessageTopic.topic == 'Endorsement').first()
    db.session.add(mts1)

    mts2 = MessageToStaff(
        text="text2",
        date=dt.datetime.utcnow(),
        replied=False
    )
    mts2.rel_sender = u1
    mts2.rel_topic = MessageTopic.query.filter(MessageTopic.topic == 'Other').first()
    db.session.add(mts2)

    mts3 = MessageToStaff(
        text="text3",
        date=dt.datetime.utcnow(),
        replied=False
    )
    mts3.rel_sender = u2
    mts3.rel_topic = MessageTopic.query.filter(MessageTopic.topic == 'Technical issues, corrections').first()
    db.session.add(mts3)

    # notification types
    nt_review_request = NotificationType.query.get(NotificationTypeEnum.REVIEW_REQUEST.value)

    # notifications
    notification1 = Notification(
        datetime=dt.datetime.utcnow(),
        title=Notification.prepare_title(nt_review_request),
        text='New review request',
        action_url=url_for('review_request_page', request_id=1)
    )
    notification1.rel_notification_type = nt_review_request
    notification1.rel_user = u1
    db.session.add(notification1)

    notification2 = Notification(
        datetime=dt.datetime.utcnow(),
        title=Notification.prepare_title(nt_review_request),
        text='New review request',
        action_url=url_for('review_request_page', request_id=2)
    )
    notification2.rel_notification_type = nt_review_request
    notification2.rel_user = u2
    db.session.add(notification2)

    # licenses
    l1 = License(
        license="license1"
    )
    l1.rel_related_paper_revisions = [pve1_1, pve1_2, pve1_3, pve4, pve5, pve6, pve7]
    db.session.add(l1)

    l2 = License(
        license="license2"
    )
    l2.rel_related_paper_revisions = [pve8, pve9, pve10, pve11, pve12, pve13, pve14]
    db.session.add(l2)

    l3 = License(
        license="license3"
    )
    l3.rel_related_paper_revisions = [pve15, pve2, pve3]
    db.session.add(l3)

    # suggestions
    s1 = Suggestion(
        suggestion="suggestion1",
        location="location1"
    )
    s1.rel_review = r1
    db.session.add(s1)

    s2 = Suggestion(
        suggestion="suggestion2",
        location="location2"
    )
    s2.rel_review = r1
    db.session.add(s2)

    s3 = Suggestion(
        suggestion="suggestion3",
        location="location3"
    )
    s3.rel_review = r1
    db.session.add(s3)

    s4 = Suggestion(
        suggestion="suggestion4",
        location="location4"
    )
    s4.rel_review = r2
    db.session.add(s4)

    s5 = Suggestion(
        suggestion="suggestion5",
        location="location5"
    )
    s5.rel_review = r2
    db.session.add(s5)

    s6 = Suggestion(
        suggestion="suggestion6",
        location="location6"
    )
    s6.rel_review = r2
    db.session.add(s6)

    s7 = Suggestion(
        suggestion="suggestion7"
    )
    s7.rel_review = r3
    db.session.add(s7)

    s8 = Suggestion(
        suggestion="suggestion8",
        location="location8"
    )
    s8.rel_review = r3
    db.session.add(s8)

    s9 = Suggestion(
        suggestion="suggestion9"
    )
    s9.rel_review = r3
    db.session.add(s9)

    cp1 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl1.com",
        preprocessed_text="preprocessed_text1"
    )
    cp1.rel_author = u1
    db.session.add(cp1)

    cp2 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl2.com",
        preprocessed_text="preprocessed_text2"
    )
    cp2.rel_author = u1
    db.session.add(cp2)

    cp3 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl3.com",
        preprocessed_text="preprocessed_text3"
    )
    cp3.rel_author = u1
    db.session.add(cp3)

    cp4 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl4.com",
        preprocessed_text="preprocessed_text4"
    )
    cp4.rel_author = u2
    db.session.add(cp4)

    cp5 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl5.com",
        preprocessed_text="preprocessed_text5"
    )
    cp5.rel_author = u2
    db.session.add(cp5)

    cp6 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl6.com",
        preprocessed_text="preprocessed_text6"
    )
    cp6.rel_author = u2
    db.session.add(cp6)

    cp7 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl7.com",
        preprocessed_text="preprocessed_text7"
    )
    cp7.rel_author = u3
    db.session.add(cp7)

    cp8 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl8.com",
        preprocessed_text="preprocessed_text8"
    )
    cp8.rel_author = u3
    db.session.add(cp8)

    cp9 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl9.com",
        preprocessed_text="preprocessed_text9"
    )
    cp9.rel_author = u3
    db.session.add(cp9)

    cp10 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl10.com",
        preprocessed_text="preprocessed_text10"
    )
    cp10.rel_author = u4
    db.session.add(cp10)

    cp11 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl11.com",
        preprocessed_text="preprocessed_text11"
    )
    cp11.rel_author = u4
    db.session.add(cp11)

    cp12 = CalibrationPaper(
        pdf_url="https://calibrationpaperurl12.com",
        preprocessed_text="preprocessed_text12"
    )
    cp12.rel_author = u4
    db.session.add(cp12)

    # revision changes components
    rcc1 = RevisionChangesComponent(
        change_description="change_description1",
        location="location1"
    )
    rcc1.rel_paper_revision = pve1_2
    db.session.add(rcc1)

    rcc2 = RevisionChangesComponent(
        change_description="change_description2",
        location="location2"
    )
    rcc2.rel_paper_revision = pve1_2
    db.session.add(rcc2)

    rcc3 = RevisionChangesComponent(
        change_description="change_description3",
    )
    rcc3.rel_paper_revision = pve1_2
    db.session.add(rcc3)

    rcc4 = RevisionChangesComponent(
        change_description="change_description4",
        location="location4"
    )
    rcc4.rel_paper_revision = pve1_3
    db.session.add(rcc4)

    rcc5 = RevisionChangesComponent(
        change_description="change_description5",
        location="location5"
    )
    rcc5.rel_paper_revision = pve1_3
    db.session.add(rcc5)

    rcc6 = RevisionChangesComponent(
        change_description="change_description6",
    )
    rcc6.rel_paper_revision = pve1_3
    db.session.add(rcc6)

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
