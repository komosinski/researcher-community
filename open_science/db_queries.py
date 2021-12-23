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