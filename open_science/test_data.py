from open_science import db
from open_science.models import *
import datetime as dt
from flask import url_for

# TODO: move this somewhere else
def create_essential_data():

    PrivilegeSet.insert_types()
    DeclinedReason.insert_reasons()
    MessageTopic.insert_topics()
    EmailType.insert_types()
    NotificationType.insert_types()

    # site as user to log emails send from site and use ForeignKey in EmailLog model
    # confirmed=False hides user
    if not User.query.filter_by(User.id==0).first():
        
        user_0 = User(
            first_name="site",
            second_name="site",
            email="open.science.mail@gmail.com",
            plain_text_password="QWerty12#$%^&*()jumbo",
            confirmed=False,
            review_mails_limit=0,
            notifications_frequency=0,
        )
        user_0.rel_privileges_set =  PrivilegeSet.query.filter(PrivilegeSet.name=='standard_user').first()  
        user_0.id = 0
        db.session.add(user_0)

    db.session.commit()
    return True


def create_test_data():
    # check if the test data has been created
    existing_paper_version = db.session.query(PaperVersion.id).filter(PaperVersion.title == 'title1').first()
    if existing_paper_version:
        return False

 
    c1 = Comment(
        text="text1",
        votes_score=0
    )
    db.session.add(c1)

    c2 = Comment(
        text="text2",
        votes_score=0
    )
    db.session.add(c2)

    c3 = Comment(
        text="text3",
        votes_score=0
    )
    db.session.add(c3)

    c4 = Comment(
        text="text4",
        votes_score=0
    )
    db.session.add(c4)

    c5 = Comment(
        text="text5",
        votes_score=0
    )
    db.session.add(c5)

    c6 = Comment(
        text="text6",
        votes_score=0
    )
    db.session.add(c6)

    c7 = Comment(
        text="text7",
        votes_score=0
    )
    db.session.add(c7)

    c8 = Comment(
        text="text8",
        votes_score=0
    )
    db.session.add(c8)

    c9 = Comment(
        text="text9",
        votes_score=0
    )
    db.session.add(c9)

    r1 = Review(
        weight=1.1,
        text="comment1",
        votes_score=0,
        review_score=5,
        creation_datetime=dt.datetime.utcnow()
    )
    r1.rel_comments_to_this_review = [c4, c5]
    db.session.add(r1)

    r2 = Review(
        weight=2.2,
        text="comment2",
        votes_score=0,
        review_score=5,
        creation_datetime=dt.datetime.utcnow()
    )
    r2.rel_comments_to_this_review = [c6]
    db.session.add(r2)

    r3 = Review(
        weight=3.3,
        text="comment3",
        votes_score=0,
        review_score=5,
        creation_datetime=dt.datetime.utcnow()
    )
    db.session.add(r3)

    p1 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p1)

    p2 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p2)

    p3 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p3)

    p4 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p4)

    p5 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p5)

    p6 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p6)

    p7 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p7)

    p8 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p8)

    p9 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p9)

    p10 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p10)

    p11 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p11)

    p12 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p12)

    p13 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p13)

    p14 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p14)

    p15 = Paper(
        license="license1",
        confidence_level=1,
        votes_score=0
    )
    db.session.add(p15)



    pve1 = PaperVersion(
        pdf_url="https://paperurl1.com",
        title="title1",
        version = 1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve1.rel_related_comments = [c1, c2]
    pve1.rel_related_reviews = [r1]
    pve1.rel_parent_paper = p1
    db.session.add(pve1)

    pve2 = PaperVersion(
        pdf_url="https://paperurl2.com",
        title="title2",
        version = 2,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve2.rel_related_comments = [c3, c4]
    pve2.rel_related_reviews = [r2]
    pve2.rel_parent_paper = p1
    db.session.add(pve2)

    pve3 = PaperVersion(
        pdf_url="https://paperurl3.com",
        title="title3",
        version = 3,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve3.rel_related_comments = [c5, c6, c7, c8, c9]
    pve3.rel_related_reviews = [r3]
    pve3.rel_parent_paper = p1
    db.session.add(pve3)

    pve4 = PaperVersion(
        pdf_url="https://paperurl4.com",
        title="title4",
        version = 1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve4.rel_parent_paper = p4
    db.session.add(pve4)

    pve5 = PaperVersion(
        pdf_url="https://paperurl5.com",
        title="title5",
        version = 1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve5.rel_parent_paper = p5
    db.session.add(pve5)

    pve6 = PaperVersion(
        pdf_url="https://paperurl6.com",
        title="title6",
        version = 1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve6.rel_parent_paper = p6
    db.session.add(pve6)

    pve7 = PaperVersion(
        pdf_url="https://paperurl7.com",
        title="title7",
        version = 1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve7.rel_parent_paper = p7
    db.session.add(pve7)

    pve8 = PaperVersion(
        pdf_url="https://paperurl8.com",
        title="title8",
        version = 1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve8.rel_parent_paper = p8
    db.session.add(pve8)

    pve9 = PaperVersion(
        pdf_url="https://paperurl9.com",
        title="title9",
        version = 1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve9.rel_parent_paper = p9
    db.session.add(pve9)

    pve10 = PaperVersion(
        pdf_url="https://paperurl10.com",
        title="title10",
        version = 1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve10.rel_parent_paper = p10
    db.session.add(pve10)

    pve11 = PaperVersion(
        pdf_url="https://paperurl11.com",
        title="title11",
        version = 1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve11.rel_parent_paper = p11
    db.session.add(pve11)

    pve12 = PaperVersion(
        pdf_url="https://paperurl12.com",
        title="title12",
        version = 1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve12.rel_parent_paper = p12
    db.session.add(pve12)

    pve13 = PaperVersion(
        pdf_url="https://paperurl13.com",
        title="title13",
        version = 1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve13.rel_parent_paper = p13
    db.session.add(pve13)

    pve14 = PaperVersion(
        pdf_url="https://paperurl14.com",
        title="title14",
        version = 1,
        abstract="description14 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve14.rel_parent_paper = p14
    db.session.add(pve14)

    pve15 = PaperVersion(
        pdf_url="https://paperurl15.com",
        title="title15",
        version = 1,
        abstract="description15 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve15.rel_parent_paper = p15
    db.session.add(pve15)

    # p2 p3
    pve2_ = PaperVersion(
        pdf_url="https://paperurl2.com",
        title="title2",
        version = 1,
        abstract="description2 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve2_.rel_parent_paper = p2
    db.session.add(pve2_)
   

    pve3_ = PaperVersion(
        pdf_url="https://paperurl3.com",
        title="title3",
        version = 1,
        abstract="description3 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime.utcnow()
    )
    pve3_.rel_parent_paper = p3
    db.session.add(pve3_)

    #to read Papers' id from autoincrement
    db.session.flush()

    # p1.newest_version_id=pve3.id
    # p4.newest_version_id=pve4.id
    # p5.newest_version_id=pve5.id
    # p6.newest_version_id=pve6.id
    # p7.newest_version_id=pve7.id
    # p8.newest_version_id=pve8.id
    # p9.newest_version_id=pve9.id
    # p10.newest_version_id=pve10.id
    # p11.newest_version_id=pve11.id
    # p12.newest_version_id=pve12.id
    # p13.newest_version_id=pve13.id
    # p14.newest_version_id=pve14.id
    # p15.newest_version_id=pve15.id
    # p2.newest_version_id=pve2_.id
    # p3.newest_version_id=pve3_.id

    t1 = Tag(
        name="tag1",
        description="description1",
        deadline=dt.datetime.utcnow()
    )
    t1.rel_related_paper_versions = [pve1, pve2]
    db.session.add(t1)

    t2 = Tag(
        name="tag2",
        description="Description2",
        deadline=dt.datetime.utcnow()
    )
    db.session.add(t2)

    t3 = Tag(
        name="tag3",
        description="DEscription3",
        deadline=dt.datetime.utcnow()
    )
    t3.rel_related_paper_versions = [pve1, pve6, pve7, pve8]
    db.session.add(t3)

    po1 = Post(
        text="text1",
        votes_score=0,
        red_flags_count=1
    )
    po1.rel_comments_to_this_post = [c7, c8]
    db.session.add(po1)

    po2 = Post(
        text="text2",
        votes_score=0,
        red_flags_count=2
    )
    po2.rel_comments_to_this_post = [c9]
    db.session.add(po2)

    po3 = Post(
        text="text3",
        votes_score=0,
        red_flags_count=3
    )
    db.session.add(po3)

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
        votes_score=0,
        last_seen=dt.datetime.utcnow(),
        weight=1.1,
        registered_on = dt.datetime.utcnow()
    )
    u1.rel_created_papers = [p1, p2, p4, p5, p6, p7, p8, p9]
    u1.rel_tags_to_user = [t1, t2]
    u1.rel_privileges_set = ps_standard_user
    u1.rel_created_tags = [t3]
    u1.rel_created_reviews = [r1, r2]
    u1.rel_created_comments = [c1, c2, c3, c4, c5, c6, c7, c8]
    u1.rel_created_posts = [po1, po2]
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
        votes_score=0,
        weight=2.2,
        registered_on = dt.datetime.utcnow()
    )
    u2.rel_created_papers = [p3, p10, p11]
    u2.rel_tags_to_user = [t3]
    u2.rel_privileges_set = ps_standard_user
    u2.rel_created_tags = [t1, t2]
    u2.rel_created_reviews = [r3]
    u2.rel_created_comments = [c9]
    u2.rel_created_posts = [po3]
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
        votes_score=0,
        weight=3.3,
        registered_on = dt.datetime.utcnow()
    )
    u3.rel_privileges_set = ps_scientific_user
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
        votes_score=0,
        weight=4.4,
        registered_on = dt.datetime.utcnow()
    )
    u4.rel_privileges_set = ps_standard_user
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
        votes_score=0,
        weight=5.5,
        registered_on = dt.datetime.utcnow()
    )
    u5.rel_privileges_set = ps_admin
    db.session.add(u5)

    rr1 = ReviewRequest(
        decision=False,
        creation_datetime=dt.datetime.utcnow()
    )
 
    rr1.rel_requested_user = u1
    rr1.rel_related_paper_version = pve1
    db.session.add(rr1)

    rr2 = ReviewRequest(
        decision=False,
        creation_datetime=dt.datetime.utcnow()
    )
    rr2.rel_requested_user = u2
    rr2.rel_related_paper_version = pve1
    db.session.add(rr2)

    rr3 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime.utcnow(),
        acceptation_date=dt.datetime.utcnow().date(),
        deadline_date=dt.datetime.utcnow().date()
    )
    rr3.rel_requested_user = u3
    rr3.rel_related_paper_version = pve1
    db.session.add(rr3)

    rr4 = ReviewRequest(
        decision=False,
        creation_datetime=dt.datetime.utcnow(),
        acceptation_date=dt.datetime.utcnow().date(),
        deadline_date=dt.datetime.utcnow().date()
    )

    rr4.rel_requested_user = u4
    rr4.rel_related_paper_version = pve4
    db.session.add(rr4)

    rr5 = ReviewRequest(
        decision=False,
        creation_datetime=dt.datetime.utcnow(),
        acceptation_date=dt.datetime.utcnow().date(),
        deadline_date=dt.datetime.utcnow().date()
    )
  
    rr5.rel_requested_user = u5
    rr5.rel_related_paper_version = pve5
    db.session.add(rr5)

    rr6 = ReviewRequest(
        decision=False,
        creation_datetime=dt.datetime.utcnow(),
        acceptation_date=dt.datetime.utcnow().date(),
        deadline_date=dt.datetime.utcnow().date()
    )

    rr6.rel_requested_user = u1
    rr6.rel_related_paper_version = pve6
    db.session.add(rr6)

    rr7 = ReviewRequest(
        decision=False,
        creation_datetime=dt.datetime.utcnow(),
        acceptation_date=dt.datetime.utcnow().date(),
        deadline_date=dt.datetime.utcnow().date()
    )

    rr7.rel_requested_user = u2
    rr7.rel_related_paper_version = pve7
    db.session.add(rr7)

    rr8 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime.utcnow(),
        acceptation_date=dt.datetime.utcnow().date(),
        deadline_date=dt.datetime.utcnow().date()
    )
    rr8.rel_requested_user = u3
    rr8.rel_related_paper_version = pve8
    db.session.add(rr8)

    rr9 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime.utcnow(),
        acceptation_date=dt.datetime.utcnow().date(),
        deadline_date=dt.datetime.utcnow().date()
    )
    rr9.rel_requested_user = u4
    rr9.rel_related_paper_version = pve9
    db.session.add(rr9)

    rr10 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime.utcnow(),
        acceptation_date=dt.datetime.utcnow().date(),
        deadline_date=dt.datetime.utcnow().date()
    )
    rr10.rel_requested_user = u5
    rr10.rel_related_paper_version = pve10
    db.session.add(rr10)

    vu1 = VoteUser(
        is_up=True
    )
    vu1.rel_creator = u1
    vu1.rel_to_user = u3
    db.session.add(vu1)

    vu2 = VoteUser(
        is_up=True
    )
    vu2.rel_creator = u2
    vu2.rel_to_user = u3
    db.session.add(vu2)

    vu3 = VoteUser(
        is_up=False
    )
    vu3.rel_creator = u3
    vu3.rel_to_user = u1
    db.session.add(vu3)

    vp1 = VotePaper(
        is_up=True
    )
    vp1.rel_creator = u1
    vp1.rel_to_paper = p3
    db.session.add(vp1)

    vp2 = VotePaper(
        is_up=True
    )
    vp2.rel_creator = u2
    vp2.rel_to_paper = p3
    db.session.add(vp2)

    vp3 = VotePaper(
        is_up=True
    )
    vp3.rel_creator = u3
    vp3.rel_to_paper = p1
    db.session.add(vp3)

    vr1 = VoteReview(
        is_up=True
    )
    vr1.rel_creator = u1
    vr1.rel_to_review = r3
    db.session.add(vr1)

    vr2 = VoteReview(
        is_up=True
    )
    vr2.rel_creator = u2
    vr2.rel_to_review = r3
    db.session.add(vr2)

    vr3 = VoteReview(
        is_up=True
    )
    vr3.rel_creator = u3
    vr3.rel_to_review = r1
    db.session.add(vr3)

    vc1 = VoteComment(
        is_up=True
    )
    vc1.rel_creator = u1
    vc1.rel_to_comment = c3
    db.session.add(vc1)

    vc2 = VoteComment(
        is_up=True
    )
    vc2.rel_creator = u2
    vc2.rel_to_comment = c3
    db.session.add(vc2)

    vc3 = VoteComment(
        is_up=True
    )
    vc3.rel_creator = u3
    vc3.rel_to_comment = c1
    db.session.add(vc3)

    vpo1 = VotePost(
        is_up=True
    )
    vpo1.rel_creator = u1
    vpo1.rel_to_post = po3
    db.session.add(vpo1)

    vpo2 = VotePost(
        is_up=True
    )
    vpo2.rel_creator = u2
    vpo2.rel_to_post = po3
    db.session.add(vpo2)

    vpo3 = VotePost(
        is_up=True
    )
    vpo3.rel_creator = u3
    vpo3.rel_to_post = po1
    db.session.add(vpo3)

    mts1 = MessageToStaff(
        text="text1",
        date=dt.datetime.utcnow(),
        replied=True
    )
    mts1.rel_sender = u1
    mts1.rel_topic = t_endorsement
    db.session.add(mts1)

    mts2 = MessageToStaff(
        text="text2",
        date=dt.datetime.utcnow(),
        replied=False
    )
    mts2.rel_sender = u1
    mts2.rel_topic = t_other
    db.session.add(mts2)

    mts3 = MessageToStaff(
        text="text3",
        date=dt.datetime.utcnow(),
        replied=False
    )
    mts3.rel_sender = u2
    mts3.rel_topic = t_technical_issues
    db.session.add(mts3)

    #notifications
    notification1 = Notification(1,dt.datetime.utcnow(),'New review request',url_for('review_request_page',request_id=1),'review_request')
    notification2 = Notification(1,dt.datetime.utcnow(),'New review request',url_for('review_request_page',request_id=2),'review_request')
    db.session.add(notification1)
    db.session.add(notification2)
    
    db.session.commit()

    return True
