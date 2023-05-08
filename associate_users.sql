UPDATE movieswebapp_movie SET added_by_id = floor(random() * 10000 + 1)::integer;
UPDATE movieswebapp_actor SET added_by_id = floor(random() * 10000 + 1)::integer;
UPDATE movieswebapp_director SET added_by_id = floor(random() * 10000 + 1)::integer;
UPDATE movieswebapp_actormovie SET added_by_id = floor(random() * 10000 + 1)::integer;
