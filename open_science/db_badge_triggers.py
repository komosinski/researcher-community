b_first_article_award_function = '''
CREATE OR REPLACE FUNCTION award_first_article_badge()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM paper_revisions WHERE uploader_id = NEW.uploader_id) = 1 THEN
        IF NOT EXISTS (SELECT 1 FROM user_badges WHERE user_id = NEW.uploader_id AND badge_id = 
                       (SELECT id FROM badges WHERE name = 'First Article')) THEN
            INSERT INTO user_badges(user_id, badge_id, earned_at)
            VALUES (NEW.uploader_id, (SELECT id FROM badges WHERE name = 'First Article'), NOW());
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
'''
b_first_article_award_trigger = '''
CREATE TRIGGER after_article_insert
AFTER INSERT ON paper_revisions
FOR EACH ROW
EXECUTE FUNCTION award_first_article_badge();
'''

b_first_comment_award_function = '''
CREATE OR REPLACE FUNCTION award_first_comment_badge()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM comments WHERE creator = NEW.creator) = 1 THEN
        IF NOT EXISTS (SELECT 1 FROM user_badges WHERE user_id = NEW.creator AND badge_id = 
                       (SELECT id FROM badges WHERE name = 'First Comment')) THEN
            INSERT INTO user_badges(user_id, badge_id, earned_at)
            VALUES (NEW.creator, (SELECT id FROM badges WHERE name = 'First Comment'), NOW());
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
'''

b_first_comment_award_trigger = '''
CREATE TRIGGER after_comment_insert
AFTER INSERT ON comments
FOR EACH ROW
EXECUTE FUNCTION award_first_comment_badge();
'''