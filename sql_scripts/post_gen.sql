SELECT setval('movieswebapp_actor_id_seq', max(id) + 1) FROM movieswebapp_actor;
SELECT setval('movieswebapp_movie_id_seq', max(id) + 1) FROM movieswebapp_movie;
SELECT setval('movieswebapp_actormovie_id_seq', max(id) + 1) FROM movieswebapp_actormovie;
SELECT setval('movieswebapp_director_id_seq', max(id) + 1) FROM movieswebapp_director;

