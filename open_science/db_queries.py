q_update_comment_score = '''
    create or replace
    function public.update_comment_score()
     returns trigger
     language plpgsql
    as $function$
    begin
        if not exists (select * from votes_comments where creator = new.creator and to_comment = new.to_comment) then
            if new.is_up then
                update comments set votes_score = votes_score + 1 where id = new.to_comment;
            else
                update comments set votes_score = votes_score - 1 where id = new.to_comment;
            end if;
        elsif (select is_up from votes_comments where creator = new.creator and to_comment = new.to_comment) then
            if new.is_up then
                delete from votes_comments where creator = new.creator and to_comment = new.to_comment;
            else
                delete from votes_comments where creator = new.creator and to_comment = new.to_comment;
                update comments set votes_score = votes_score - 2 where id = new.to_comment;
            end if;
        else
            if new.is_up then
                delete from votes_comments where creator = new.creator and to_comment = new.to_comment;
                update comments set votes_score = votes_score + 2 where id = new.to_comment;
            else
                delete from votes_comments where creator = new.creator and to_comment = new.to_comment;
            end if;
        end if;
        return new;
    end;
    $function$;
'''

qt_update_comment_score = '''
    do $$
    begin
        if not exists (
    select
        1
    from
        pg_trigger
    where
        tgname = 'update_comment_score') then
        create trigger update_comment_score  
            before
    insert
        on
        votes_comments
            for each row execute function update_comment_score();
    end if;
    end
    $$;
'''

q_update_user_reputation = '''
    create or replace
    function public.update_user_reputation()
     returns trigger
     language plpgsql
    as $function$
    begin
        if new.votes_score != old.votes_score then
            update users set reputation = reputation + new.votes_score - old.votes_score where id = new.creator;
        end if;
        return new;
    end;
    $function$;
'''

qt_update_user_reputation = '''
    do $$
    begin
        if not exists (
    select
        1
    from
        pg_trigger
    where
        tgname = 'update_user_reputation') then
        create trigger update_user_reputation  
            after
    update
        on
        comments
            for each row execute function update_user_reputation();
    end if;
    end
    $$;
'''

q_update_user_red_flags_count = '''
    create or replace
    function public.update_user_red_flags_count()
     returns trigger
     language plpgsql
    as $function$
    begin
        if not exists (select * from red_flags_user where creator = new.creator and to_user = new.to_user) then
            update users set red_flags_count = red_flags_count + 1 where id = new.to_user;
        else
            delete from red_flags_user where creator = new.creator and to_user = new.to_user;
        end if;
        return new;
    end;
    $function$;
'''

qt_update_user_red_flags_count = '''
    do $$
    begin
        if not exists (
    select
        1
    from
        pg_trigger
    where
        tgname = 'update_user_red_flags_count') then
        create trigger update_user_red_flags_count  
            before
    insert
        on
        red_flags_user
            for each row execute function update_user_red_flags_count();
    end if;
    end
    $$;
'''

q_update_tag_red_flags_count = '''
    create or replace
    function public.update_tag_red_flags_count()
     returns trigger
     language plpgsql
    as $function$
    begin
        if not exists (select * from red_flags_tag where creator = new.creator and to_tag = new.to_tag) then
            update tags set red_flags_count = red_flags_count + 1 where id = new.to_tag;
        else
            delete from red_flags_tag where creator = new.creator and to_tag = new.to_tag;
        end if;
        return new;
    end;
    $function$;
'''

qt_update_tag_red_flags_count = '''
    do $$
    begin
        if not exists (
    select
        1
    from
        pg_trigger
    where
        tgname = 'update_tag_red_flags_count') then
        create trigger update_tag_red_flags_count  
            before
    insert
        on
        red_flags_tag
            for each row execute function update_tag_red_flags_count();
    end if;
    end
    $$;
'''

q_update_review_red_flags_count = '''
    create or replace
    function public.update_review_red_flags_count()
     returns trigger
     language plpgsql
    as $function$
    begin
        if not exists (select * from red_flags_review where creator = new.creator and to_review = new.to_review) then
            update reviews set red_flags_count = red_flags_count + 1 where id = new.to_review;
        else
            delete from red_flags_review where creator = new.creator and to_review = new.to_review;
        end if;
        return new;
    end;
    $function$;
'''

qt_update_review_red_flags_count = '''
    do $$
    begin
        if not exists (
    select
        1
    from
        pg_trigger
    where
        tgname = 'update_review_red_flags_count') then
        create trigger update_review_red_flags_count  
            before
    insert
        on
        red_flags_review
            for each row execute function update_review_red_flags_count();
    end if;
    end
    $$;
'''

q_update_revision_red_flags_count = '''
    create or replace
    function public.update_revision_red_flags_count()
     returns trigger
     language plpgsql
    as $function$
    begin
        if not exists (select * from red_flags_paper_revision where creator = new.creator and to_paper_revision = new.to_paper_revision) then
            update paper_revisions set red_flags_count = red_flags_count + 1 where id = new.to_paper_revision;
        else
            delete from red_flags_paper_revision where creator = new.creator and to_paper_revision = new.to_paper_revision;
        end if;
        return new;
    end;
    $function$;
'''

qt_update_revision_red_flags_count = '''
    do $$
    begin
        if not exists (
    select
        1
    from
        pg_trigger
    where
        tgname = 'update_revision_red_flags_count') then
        create trigger update_revision_red_flags_count  
            before
    insert
        on
        red_flags_paper_revision
            for each row execute function update_revision_red_flags_count();
    end if;
    end
    $$;
'''

q_update_comment_red_flags_count = '''
    create or replace
    function public.update_comment_red_flags_count()
     returns trigger
     language plpgsql
    as $function$
    begin
        if not exists (select * from red_flags_comment where creator = new.creator and to_comment = new.to_comment) then
            update comments set red_flags_count = red_flags_count + 1 where id = new.to_comment;
        else
            delete from red_flags_comment where creator = new.creator and to_comment = new.to_comment;
        end if;
        return new;
    end;
    $function$;
'''

qt_update_comment_red_flags_count = '''
    do $$
    begin
        if not exists (
    select
        1
    from
        pg_trigger
    where
        tgname = 'update_comment_red_flags_count') then
        create trigger update_comment_red_flags_count  
            before
    insert
        on
        red_flags_comment
            for each row execute function update_comment_red_flags_count();
    end if;
    end
    $$;
'''
