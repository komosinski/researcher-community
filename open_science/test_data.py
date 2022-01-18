from open_science.models import *
import datetime as dt
from flask import url_for

from text_processing.similarity_matrix import create_tfidf_matrix, create_similarities_matrix, save_tfidf_matrix, \
    save_similarities_matrix

from open_science.enums import UserTypeEnum

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
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.STANDARD_USER.value
    )
    db.session.add(c1)

    c2 = Comment(
        text="text2",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.RESEARCHER_USER.value
    )
    db.session.add(c2)

    c3 = Comment(
        text="text3",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.STANDARD_USER.value
    )
    db.session.add(c3)

    c4 = Comment(
        text="text4",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.RESEARCHER_USER.value
    )
    db.session.add(c4)

    c5 = Comment(
        text="text5",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.STANDARD_USER.value
    )
    db.session.add(c5)

    c6 = Comment(
        text="text6",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.STANDARD_USER.value
    )
    db.session.add(c6)

    c7 = Comment(
        text="text7",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.STANDARD_USER.value
    )
    db.session.add(c7)

    c8 = Comment(
        text="text8",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.RESEARCHER_USER.value
    )
    db.session.add(c8)

    c9 = Comment(
        text="text9",
        votes_score=0,
        red_flags_count=0,
        level=0,
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.STANDARD_USER.value
    )
    db.session.add(c9)

    c10 = Comment(
        text="text10",
        votes_score=0,
        red_flags_count=0,
        level=1,
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.STANDARD_USER.value
    )
    c10.rel_related_comment = [c1]
    db.session.add(c10)

    c11 = Comment(
        text="text11",
        votes_score=0,
        red_flags_count=0,
        level=1,
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.RESEARCHER_USER.value
    )
    c11.rel_related_comment = [c2]
    db.session.add(c11)

    c12 = Comment(
        text="text12",
        votes_score=0,
        red_flags_count=0,
        level=1,
        date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        creator_role = UserTypeEnum.RESEARCHER_USER.value
    )
    c12.rel_related_comment = [c2]
    db.session.add(c12)

    # reviews
    r1 = Review(
        publication_datetime=dt.datetime(2020, 9, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.1,
        evaluation_conclusion=0.1,
        evaluation_error=0.1,
        evaluation_organize=0.1,
        evaluation_accept=False,
        confidence=0.1,
    )
    r1.rel_comments_to_this_review = [c4, c5]
    db.session.add(r1)

    r2 = Review(
        publication_datetime=dt.datetime(2020, 9, 2, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.2,
        evaluation_conclusion=0.2,
        evaluation_error=0.2,
        evaluation_organize=0.2,
        evaluation_accept=True,
        confidence=0.2,
    )
    r2.rel_comments_to_this_review = [c6]
    db.session.add(r2)

    r3 = Review(
        publication_datetime=dt.datetime(2020, 9, 3, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.3,
        evaluation_conclusion=0.3,
        evaluation_error=0.3,
        evaluation_organize=0.3,
        evaluation_accept=True,
        confidence=0.3,
    )
    db.session.add(r3)

    r4 = Review(
        publication_datetime=dt.datetime(2020, 9, 4, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.4,
        evaluation_conclusion=0.4,
        evaluation_error=0.4,
        evaluation_organize=0.4,
        evaluation_accept=True,
        confidence=0.4,
    )
    db.session.add(r4)

    r5 = Review(
        publication_datetime=dt.datetime(2020, 9, 5, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.1,
        evaluation_conclusion=0.1,
        evaluation_error=0.1,
        evaluation_organize=0.1,
        evaluation_accept=False,
        confidence=0.5,
    )
    db.session.add(r5)

    r6 = Review(
        publication_datetime=dt.datetime(2020, 9, 6, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.6,
        evaluation_conclusion=0.6,
        evaluation_error=0.6,
        evaluation_organize=0.6,
        evaluation_accept=True,
        confidence=0.6,
    )
    db.session.add(r6)

    r7 = Review(
        publication_datetime=dt.datetime(2020, 9, 7, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.7,
        evaluation_conclusion=0.7,
        evaluation_error=0.7,
        evaluation_organize=0.7,
        evaluation_accept=True,
        confidence=0.7,
    )
    db.session.add(r7)

    r8 = Review(
        publication_datetime=dt.datetime(2020, 9, 8, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.1,
        evaluation_conclusion=0.1,
        evaluation_error=0.1,
        evaluation_organize=0.1,
        evaluation_accept=False,
        confidence=0.8,
    )
    db.session.add(r8)

    r9 = Review(
        publication_datetime=dt.datetime(2020, 9, 9, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.9,
        evaluation_conclusion=0.9,
        evaluation_error=0.9,
        evaluation_organize=0.9,
        evaluation_accept=True,
        confidence=0.9,
    )
    db.session.add(r9)

    r10 = Review(
        publication_datetime=dt.datetime(2020, 9, 10, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.1,
        evaluation_conclusion=0.1,
        evaluation_error=0.1,
        evaluation_organize=0.1,
        evaluation_accept=True,
        confidence=0.1,
    )
    db.session.add(r10)

    r11 = Review(
        publication_datetime=dt.datetime(2020, 9, 11, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.2,
        evaluation_conclusion=0.2,
        evaluation_error=0.2,
        evaluation_organize=0.2,
        evaluation_accept=True,
        confidence=0.2,
    )
    db.session.add(r11)

    r12 = Review(
        publication_datetime=dt.datetime(2020, 9, 12, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.3,
        evaluation_conclusion=0.3,
        evaluation_error=0.3,
        evaluation_organize=0.3,
        evaluation_accept=True,
        confidence=0.3,
    )
    db.session.add(r12)

    r13 = Review(
        publication_datetime=dt.datetime(2020, 9, 13, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.1,
        evaluation_conclusion=0.1,
        evaluation_error=0.1,
        evaluation_organize=0.1,
        evaluation_accept=False,
        confidence=0.4,
    )
    db.session.add(r13)

    r14 = Review(
        publication_datetime=dt.datetime(2020, 9, 14, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.1,
        evaluation_conclusion=0.1,
        evaluation_error=0.1,
        evaluation_organize=0.1,
        evaluation_accept=False,
        confidence=0.5,
    )
    db.session.add(r14)

    r15 = Review(
        publication_datetime=dt.datetime(2020, 9, 15, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.6,
        evaluation_conclusion=0.6,
        evaluation_error=0.6,
        evaluation_organize=0.6,
        evaluation_accept=True,
        confidence=0.6,
    )
    db.session.add(r15)

    r16 = Review(
        publication_datetime=dt.datetime(2020, 9, 16, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.7,
        evaluation_conclusion=0.7,
        evaluation_error=0.7,
        evaluation_organize=0.7,
        evaluation_accept=True,
        confidence=0.7,
    )
    db.session.add(r16)

    r17 = Review(
        publication_datetime=dt.datetime(2020, 9, 17, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.8,
        evaluation_conclusion=0.8,
        evaluation_error=0.8,
        evaluation_organize=0.8,
        evaluation_accept=True,
        confidence=0.8,
    )
    db.session.add(r17)

    r18 = Review(
        publication_datetime=dt.datetime(2020, 9, 18, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.1,
        evaluation_conclusion=0.1,
        evaluation_error=0.1,
        evaluation_organize=0.1,
        evaluation_accept=False,
        confidence=0.9,
    )
    db.session.add(r18)

    r19 = Review(
        publication_datetime=dt.datetime(2020, 9, 19, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.1,
        evaluation_conclusion=0.1,
        evaluation_error=0.1,
        evaluation_organize=0.1,
        evaluation_accept=True,
        confidence=0.1,
    )
    db.session.add(r19)

    r20 = Review(
        publication_datetime=dt.datetime(2020, 9, 20, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.2,
        evaluation_conclusion=0.2,
        evaluation_error=0.2,
        evaluation_organize=0.2,
        evaluation_accept=True,
        confidence=0.2,
    )
    db.session.add(r20)

    r21 = Review(
        publication_datetime=dt.datetime(2020, 9, 21, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.3,
        evaluation_conclusion=0.3,
        evaluation_error=0.3,
        evaluation_organize=0.3,
        evaluation_accept=True,
        confidence=0.3,
    )
    db.session.add(r21)

    r22 = Review(
        publication_datetime=dt.datetime(2020, 9, 22, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.4,
        evaluation_conclusion=0.4,
        evaluation_error=0.4,
        evaluation_organize=0.4,
        evaluation_accept=True,
        confidence=0.4,
    )
    db.session.add(r22)

    r23 = Review(
        publication_datetime=dt.datetime(2020, 9, 23, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.5,
        evaluation_conclusion=0.5,
        evaluation_error=0.5,
        evaluation_organize=0.5,
        evaluation_accept=True,
        confidence=0.5,
    )
    db.session.add(r23)

    r24 = Review(
        publication_datetime=dt.datetime(2020, 9, 24, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.6,
        evaluation_conclusion=0.6,
        evaluation_error=0.6,
        evaluation_organize=0.6,
        evaluation_accept=True,
        confidence=0.6,
    )
    db.session.add(r24)

    r25 = Review(
        publication_datetime=dt.datetime(2020, 9, 25, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.7,
        evaluation_conclusion=0.7,
        evaluation_error=0.7,
        evaluation_organize=0.7,
        evaluation_accept=True,
        confidence=0.7,
    )
    db.session.add(r25)

    r26 = Review(
        publication_datetime=dt.datetime(2020, 9, 26, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.8,
        evaluation_conclusion=0.8,
        evaluation_error=0.8,
        evaluation_organize=0.8,
        evaluation_accept=True,
        confidence=0.8,
    )
    db.session.add(r26)

    r27 = Review(
        publication_datetime=dt.datetime(2020, 9, 27, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.9,
        evaluation_conclusion=0.9,
        evaluation_error=0.9,
        evaluation_organize=0.9,
        evaluation_accept=True,
        confidence=0.9,
    )
    db.session.add(r27)

    r28 = Review(
        publication_datetime=dt.datetime(2020, 9, 28, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.1,
        evaluation_conclusion=0.1,
        evaluation_error=0.1,
        evaluation_organize=0.1,
        evaluation_accept=True,
        confidence=0.1,
    )
    db.session.add(r28)

    r29 = Review(
        publication_datetime=dt.datetime(2020, 9, 29, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.2,
        evaluation_conclusion=0.2,
        evaluation_error=0.2,
        evaluation_organize=0.2,
        evaluation_accept=True,
        confidence=0.2,
    )
    db.session.add(r29)

    r30 = Review(
        publication_datetime=dt.datetime(2020, 9, 30, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.3,
        evaluation_conclusion=0.3,
        evaluation_error=0.3,
        evaluation_organize=0.3,
        evaluation_accept=True,
        confidence=0.3,
    )
    db.session.add(r30)

    r31 = Review(
        publication_datetime=dt.datetime(2020, 10, 1, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.4,
        evaluation_conclusion=0.4,
        evaluation_error=0.4,
        evaluation_organize=0.4,
        evaluation_accept=True,
        confidence=0.4,
    )
    db.session.add(r31)

    r32 = Review(
        publication_datetime=dt.datetime(2020, 10, 2, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.5,
        evaluation_conclusion=0.5,
        evaluation_error=0.5,
        evaluation_organize=0.5,
        evaluation_accept=True,
        confidence=0.5,
    )
    db.session.add(r32)

    r33 = Review(
        publication_datetime=dt.datetime(2020, 10, 3, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.6,
        evaluation_conclusion=0.6,
        evaluation_error=0.6,
        evaluation_organize=0.6,
        evaluation_accept=True,
        confidence=0.6,
    )
    db.session.add(r33)

    r34 = Review(
        publication_datetime=dt.datetime(2020, 10, 4, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.7,
        evaluation_conclusion=0.7,
        evaluation_error=0.7,
        evaluation_organize=0.7,
        evaluation_accept=True,
        confidence=0.7,
    )
    db.session.add(r34)

    r35 = Review(
        publication_datetime=dt.datetime(2020, 10, 5, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.8,
        evaluation_conclusion=0.8,
        evaluation_error=0.8,
        evaluation_organize=0.8,
        evaluation_accept=True,
        confidence=0.8,
    )
    db.session.add(r35)

    r36 = Review(
        publication_datetime=dt.datetime(2020, 10, 6, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.9,
        evaluation_conclusion=0.9,
        evaluation_error=0.9,
        evaluation_organize=0.9,
        evaluation_accept=True,
        confidence=0.9,
    )
    db.session.add(r36)

    r37 = Review(
        publication_datetime=dt.datetime(2020, 10, 7, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.1,
        evaluation_conclusion=0.1,
        evaluation_error=0.1,
        evaluation_organize=0.1,
        evaluation_accept=True,
        confidence=0.1,
    )
    db.session.add(r37)

    r38 = Review(
        publication_datetime=dt.datetime(2020, 10, 8, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.2,
        evaluation_conclusion=0.2,
        evaluation_error=0.2,
        evaluation_organize=0.2,
        evaluation_accept=True,
        confidence=0.2,
    )
    db.session.add(r38)

    r39 = Review(
        publication_datetime=dt.datetime(2020, 10, 9, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.3,
        evaluation_conclusion=0.3,
        evaluation_error=0.3,
        evaluation_organize=0.3,
        evaluation_accept=True,
        confidence=0.3,
    )
    db.session.add(r39)

    r40 = Review(
        publication_datetime=dt.datetime(2020, 10, 10, 2, 2, 2, 2),
        is_hidden=False,
        evaluation_novel=0.4,
        evaluation_conclusion=0.4,
        evaluation_error=0.4,
        evaluation_organize=0.4,
        evaluation_accept=True,
        confidence=0.4,
    )
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
        pdf_url="https://paperurl1.com",
        title="title1.1",
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve1_1.rel_related_comments = [c1, c2]
    pve1_1.rel_parent_paper = p1
    pve1_1.rel_related_reviews = [r1, r2, r3, r4]
    db.session.add(pve1_1)

    pve1_2 = PaperRevision(
        pdf_url="https://paperurl1_2.com",
        title="title1.2",
        version=2,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve1_2.rel_related_comments = [c3, c4]
    pve1_2.rel_parent_paper = p1
    pve1_2.rel_related_reviews = [r5, r6, r7, r8]
    db.session.add(pve1_2)

    pve1_3 = PaperRevision(
        pdf_url="https://paperurl1_3.com",
        title="title1.3",
        version=3,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve1_3.rel_related_comments = [c5, c6, c7, c8, c9]
    pve1_3.rel_parent_paper = p1
    pve1_3.rel_related_reviews = [r9, r10, r11, r12]
    db.session.add(pve1_3)

    pve2 = PaperRevision(
        pdf_url="https://paperurl2.com",
        title="title2",
        version=1,
        abstract="description2 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve2.rel_parent_paper = p2
    pve2.rel_related_reviews = [r13, r14]
    db.session.add(pve2)

    pve3 = PaperRevision(
        pdf_url="https://paperurl3.com",
        title="title3",
        version=1,
        abstract="description3 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=3,
        red_flags_count=0
    )
    pve3.rel_parent_paper = p3
    pve3.rel_related_reviews = [r15, r16]
    db.session.add(pve3)

    pve4 = PaperRevision(
        pdf_url="https://paperurl4.com",
        title="title4",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=3,
        red_flags_count=0
    )
    pve4.rel_parent_paper = p4
    pve4.rel_related_reviews = [r17, r18]
    db.session.add(pve4)

    pve5 = PaperRevision(
        pdf_url="https://paperurl5.com",
        title="title5",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve5.rel_parent_paper = p5
    pve5.rel_related_reviews = [r19, r20]
    db.session.add(pve5)

    pve6 = PaperRevision(
        pdf_url="https://paperurl6.com",
        title="title6",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve6.rel_parent_paper = p6
    pve6.rel_related_reviews = [r21, r22]
    db.session.add(pve6)

    pve7 = PaperRevision(
        pdf_url="https://paperurl7.com",
        title="title7",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve7.rel_parent_paper = p7
    pve7.rel_related_reviews = [r23, r24]
    db.session.add(pve7)

    pve8 = PaperRevision(
        pdf_url="https://paperurl8.com",
        title="title8",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve8.rel_parent_paper = p8
    pve8.rel_related_reviews = [r25, r26]
    db.session.add(pve8)

    pve9 = PaperRevision(
        pdf_url="https://paperurl9.com",
        title="title9",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve9.rel_parent_paper = p9
    pve9.rel_related_reviews = [r27, r28]
    db.session.add(pve9)

    pve10 = PaperRevision(
        pdf_url="https://paperurl10.com",
        title="title10",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve10.rel_parent_paper = p10
    pve10.rel_related_reviews = [r29, r30]
    db.session.add(pve10)

    pve11 = PaperRevision(
        pdf_url="https://paperurl11.com",
        title="title11",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve11.rel_parent_paper = p11
    pve11.rel_related_reviews = [r31, r32]
    db.session.add(pve11)

    pve12 = PaperRevision(
        pdf_url="https://paperurl12.com",
        title="title12",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve12.rel_parent_paper = p12
    pve12.rel_related_reviews = [r33, r34]
    db.session.add(pve12)

    pve13 = PaperRevision(
        pdf_url="https://paperurl13.com",
        title="title13",
        version=1,
        abstract="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve13.rel_parent_paper = p13
    pve13.rel_related_reviews = [r35, r36]
    db.session.add(pve13)

    pve14 = PaperRevision(
        pdf_url="https://paperurl14.com",
        title="title14",
        version=1,
        abstract="description14 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve14.rel_parent_paper = p14
    pve14.rel_related_reviews = [r37, r38]
    db.session.add(pve14)

    pve15 = PaperRevision(
        pdf_url="https://paperurl15.com",
        title="title15",
        version=1,
        abstract="description15 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        preprocessed_text="description1 In orci lectus, convallis et velit at, ultrices rhoncus ante. ",
        publication_date=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        confidence_level=1,
        red_flags_count=0
    )
    pve15.rel_parent_paper = p15
    pve15.rel_related_reviews = [r39, r40]
    db.session.add(pve15)

    # to read Papers' id from autoincrement
    db.session.flush()

    t1 = Tag(
        name="tag1",
        description="description1",
        deadline=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        red_flags_count=0
    )
    t1.rel_related_paper_revisions = [pve1_1, pve1_2]
    db.session.add(t1)

    t2 = Tag(
        name="tag2",
        description="Description2",
        deadline=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        red_flags_count=0
    )
    db.session.add(t2)

    t3 = Tag(
        name="tag3",
        description="DEscription3",
        deadline=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        red_flags_count=0
    )
    t3.rel_related_paper_revisions = [pve1_1, pve6, pve7, pve8]
    db.session.add(t3)

    # users
    u1 = User(
        first_name="Shayla",
        second_name="Jackson",
        email="shayla.jackson@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        affiliation="affiliation1",
        orcid="0000000218250097",
        google_scholar="https://scholar.google.com/profil1",
        about_me="about_me1",
        personal_website="https://personalwebsite1.com",
        review_mails_limit=1,
        notifications_frequency=7,
        last_seen=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        weight=1.1,
        registered_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        red_flags_count=0
    )
    u1.rel_created_paper_revisions = [pve1_1, pve1_2, pve1_3, pve2, pve6, pve11]
    u1.rel_tags_to_user = [t1, t2]
    u1.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.RESEARCHER_USER.value).first()
    u1.rel_created_tags = [t3]
    u1.rel_created_reviews = [r15, r20, r25, r30, r35, r40]
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
        first_name="Oakley",
        second_name="Muir",
        email="oakley.muir@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        affiliation="affiliation2",
        orcid="0000000218250097",
        google_scholar="https://scholar.google.com/profil2",
        about_me="about_me2",
        personal_website="https://personalwebsite2.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=2.2,
        registered_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        red_flags_count=0
    )
    u2.rel_created_paper_revisions = [pve2, pve7, pve12]
    u2.rel_tags_to_user = [t3]
    u2.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.RESEARCHER_USER.value).first()
    u2.rel_created_tags = [t1, t2]
    u2.rel_created_reviews = [r1, r5, r9, r16, r21, r26, r31, r36]
    u2.rel_created_comments = [c2, c5, c8, c11]
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
        confirmed_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        affiliation="affiliation3",
        orcid="0000000218250097",
        google_scholar="https://scholar.google.com/profil3",
        about_me="about_me3",
        personal_website="https://personalwebsite3.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=3.3,
        registered_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        red_flags_count=0
    )
    u3.rel_created_paper_revisions = [pve2, pve3, pve8, pve13]
    u3.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.RESEARCHER_USER.value).first()
    u3.rel_created_reviews = [r2, r6, r10, r17, r22, r27, r32, r37]
    u3.rel_created_comments = [c3, c6, c9, c12]
    db.session.add(u3)

    u4 = User(
        first_name="Sylvia",
        second_name="Osborne",
        email="sylvia.osborne@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        affiliation="affiliation4",
        orcid="0000000218250097",
        google_scholar="https://scholar.google.com/profil4",
        about_me="about_me4",
        personal_website="https://personalwebsite4.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=3.3,
        registered_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        red_flags_count=0
    )
    u4.rel_created_paper_revisions = [pve4, pve9, pve14]
    u4.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.RESEARCHER_USER.value).first()
    u4.rel_created_reviews = [r3, r7, r11, r13, r19, r23, r29, r33, r39]
    db.session.add(u4)

    u5 = User(
        first_name="Kerys",
        second_name="Campbell",
        email="kerys.campbell@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        affiliation="affiliation5",
        orcid="0000000218250097",
        google_scholar="https://scholar.google.com/profil5",
        about_me="about_me5",
        personal_website="https://personalwebsite5.com",
        review_mails_limit=1,
        notifications_frequency=7,
        weight=3.3,
        registered_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        red_flags_count=0
    )
    u5.rel_created_paper_revisions = [pve5, pve10, pve15]
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
        registered_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        red_flags_count=0
    )
    u6.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.STANDARD_USER.value).first()
    db.session.add(u6)

    u7 = User(
        first_name="admin_name",
        second_name="admin_second_name",
        email="email7@email.com",
        plain_text_password="QWerty12#$%",
        confirmed=True,
        confirmed_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        affiliation="",
        orcid="",
        google_scholar="",
        about_me="",
        personal_website="",
        review_mails_limit=0,
        notifications_frequency=0,
        weight=5.5,
        registered_on=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        red_flags_count=0
    )
    u7.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == UserTypeEnum.ADMIN.value).first()
    db.session.add(u7)

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
    rr13.rel_related_paper_version = pve2
    db.session.add(rr13)

    rr14 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 8, 14, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 8, 15),
        deadline_date=dt.date(2020, 9, 14),
    )
    rr14.rel_requested_user = u5
    rr14.rel_related_paper_version = pve2
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
        acceptation_date=dt.date(2020, 9, 6),
        deadline_date=dt.date(2020, 10, 5),
    )
    rr36.rel_requested_user = u2
    rr36.rel_related_paper_version = pve13
    db.session.add(rr36)

    rr37 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 6, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 9, 7),
        deadline_date=dt.date(2020, 10, 6),
    )
    rr37.rel_requested_user = u3
    rr37.rel_related_paper_version = pve14
    db.session.add(rr37)

    rr38 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 7, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 9, 8),
        deadline_date=dt.date(2020, 10, 7),
    )
    rr38.rel_requested_user = u5
    rr38.rel_related_paper_version = pve14
    db.session.add(rr38)

    rr39 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 8, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 9, 9),
        deadline_date=dt.date(2020, 10, 8),
    )
    rr39.rel_requested_user = u4
    rr39.rel_related_paper_version = pve15
    db.session.add(rr39)

    rr40 = ReviewRequest(
        decision=True,
        creation_datetime=dt.datetime(2020, 9, 9, 2, 2, 2, 2),
        acceptation_date=dt.date(2020, 9, 10),
        deadline_date=dt.date(2020, 10, 9),
    )
    rr40.rel_requested_user = u1
    rr40.rel_related_paper_version = pve15
    db.session.add(rr40)

    rr41 = ReviewRequest(
        decision=False,
        creation_datetime=dt.datetime(2020, 9, 10, 2, 2, 2, 2),
        deadline_date=dt.date(2020, 10, 10),
        reason_conflict_interest=True,
        reason_lack_expertise=True,
    )
    rr41.rel_requested_user = u1
    rr41.rel_related_paper_version = pve15
    db.session.add(rr41)

    # comments votes
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
    notification1 = Notification(
        datetime=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
        title=Notification.prepare_title(nt_review_request),
        text='New review request',
        action_url=url_for('review_request_page', request_id=1)
    )
    notification1.rel_notification_type = nt_review_request
    notification1.rel_user = u1
    db.session.add(notification1)

    notification2 = Notification(
        datetime=dt.datetime(2022, 1, 17, 1, 1, 1, 1),
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

    # matrices
    tfidf = create_tfidf_matrix()
    similarities = create_similarities_matrix()

    save_tfidf_matrix(tfidf)
    save_similarities_matrix(similarities)

    return True
