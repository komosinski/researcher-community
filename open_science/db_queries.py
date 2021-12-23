q_update_user_score = '''
    create or replace
    function public.update_user_score()
     returns trigger
     language plpgsql
    as $function$
    begin
        if not exists (select * from votes_users where creator = new.creator) then
            if new.is_up then
                update users set votes_score = votes_score + 1 where id = new.to_user;
            else
                update users set votes_score = votes_score - 1 where id = new.to_user;
            end if;
        elsif (select is_up from votes_users where creator = new.creator) then
            if new.is_up then
                delete from votes_users where creator = new.creator;
            else
                delete from votes_users where creator = new.creator;
                update users set votes_score = votes_score - 2 where id = new.to_user;
            end if;
        else
            if new.is_up then
                delete from votes_users where creator = new.creator;
                update users set votes_score = votes_score + 2 where id = new.to_user;
            else
                delete from votes_users where creator = new.creator;
            end if;
        end if;
    return new;
    end;

    $function$;
'''

qt_update_user_score = '''
    do $$
    begin
        if not exists (
    select
        1
    from
        pg_trigger
    where
        tgname = 'update_user_score') then
        create trigger update_user_score  
            before
    insert
        on
        votes_users
            for each row execute function update_user_score();
    end if;
    end
    $$;
'''

q_update_paper_score = '''
    create or replace
    function public.update_paper_score()
     returns trigger
     language plpgsql
    as $function$
    begin
        if not exists (select * from votes_papers where creator = new.creator) then
            if new.is_up then
                update papers set votes_score = votes_score + 1 where id = new.to_paper;
            else
                update papers set votes_score = votes_score - 1 where id = new.to_paper;
            end if;
        elsif (select is_up from votes_papers where creator = new.creator) then
            if new.is_up then
                delete from votes_papers where creator = new.creator;
            else
                delete from votes_papers where creator = new.creator;
                update papers set votes_score = votes_score - 2 where id = new.to_paper;
            end if;
        else
            if new.is_up then
                delete from votes_papers where creator = new.creator;
                update papers set votes_score = votes_score + 2 where id = new.to_paper;
            else
                delete from votes_papers where creator = new.creator;
            end if;
        end if;
    return new;
    end;

    $function$;
'''

qt_update_paper_score = '''
    do $$
    begin
        if not exists (
    select
        1
    from
        pg_trigger
    where
        tgname = 'update_paper_score') then
        create trigger update_paper_score  
            before
    insert
        on
        votes_papers
            for each row execute function update_paper_score();
    end if;
    end
    $$;
'''

q_update_review_score = '''
    create or replace
    function public.update_review_score()
     returns trigger
     language plpgsql
    as $function$
    begin
        if not exists (select * from votes_reviews where creator = new.creator) then
            if new.is_up then
                update reviews set votes_score = votes_score + 1 where id = new.to_review;
            else
                update reviews set votes_score = votes_score - 1 where id = new.to_review;
            end if;
        elsif (select is_up from votes_reviews where creator = new.creator) then
            if new.is_up then
                delete from votes_reviews where creator = new.creator;
            else
                delete from votes_reviews where creator = new.creator;
                update reviews set votes_score = votes_score - 2 where id = new.to_review;
            end if;
        else
            if new.is_up then
                delete from votes_reviews where creator = new.creator;
                update reviews set votes_score = votes_score + 2 where id = new.to_review;
            else
                delete from votes_reviews where creator = new.creator;
            end if;
        end if;
    return new;
    end;

    $function$;
'''

qt_update_review_score = '''
    do $$
    begin
        if not exists (
    select
        1
    from
        pg_trigger
    where
        tgname = 'update_review_score') then
        create trigger update_review_score  
            before
    insert
        on
        votes_reviews
            for each row execute function update_review_score();
    end if;
    end
    $$;
'''

q_update_comment_score = '''
    create or replace
    function public.update_comment_score()
     returns trigger
     language plpgsql
    as $function$
    begin
        if not exists (select * from votes_comments where creator = new.creator) then
            if new.is_up then
                update comments set votes_score = votes_score + 1 where id = new.to_comment;
            else
                update comments set votes_score = votes_score - 1 where id = new.to_comment;
            end if;
        elsif (select is_up from votes_comments where creator = new.creator) then
            if new.is_up then
                delete from votes_comments where creator = new.creator;
            else
                delete from votes_comments where creator = new.creator;
                update comments set votes_score = votes_score - 2 where id = new.to_comment;
            end if;
        else
            if new.is_up then
                delete from votes_comments where creator = new.creator;
                update comments set votes_score = votes_score + 2 where id = new.to_comment;
            else
                delete from votes_comments where creator = new.creator;
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

q_update_post_score = '''
    create or replace
    function public.update_post_score()
     returns trigger
     language plpgsql
    as $function$
    begin
        if not exists (select * from votes_posts where creator = new.creator) then
            if new.is_up then
                update posts set votes_score = votes_score + 1 where id = new.to_post;
            else
                update posts set votes_score = votes_score - 1 where id = new.to_post;
            end if;
        elsif (select is_up from votes_posts where creator = new.creator) then
            if new.is_up then
                delete from votes_posts where creator = new.creator;
            else
                delete from votes_posts where creator = new.creator;
                update posts set votes_score = votes_score - 2 where id = new.to_post;
            end if;
        else
            if new.is_up then
                delete from votes_posts where creator = new.creator;
                update posts set votes_score = votes_score + 2 where id = new.to_post;
            else
                delete from votes_posts where creator = new.creator;
            end if;
        end if;
    return new;
    end;

    $function$;
'''

qt_update_post_score = '''
    do $$
    begin
        if not exists (
    select
        1
    from
        pg_trigger
    where
        tgname = 'update_post_score') then
        create trigger update_post_score  
            before
    insert
        on
        votes_posts
            for each row execute function update_post_score();
    end if;
    end
    $$;
'''