drop table if exists users;
create table users (
  id integer primary key autoincrement,
  name text not null,
  email text not null,
  password text not null
);

drop table if exists movies;
create table movies (
  id integer primary key autoincrement,
  title text not null,
  description text not null
);

drop table if exists ratings;
create table ratings (
	id integer primary key autoincrement,
	userid integer,
	movieid integer,
	rating integer default 0,
	has_whatched boolean,
	watch_again_rating integer
);

drop table if exists friends;
create table friends (
	user_id_a integer,
	user_id_b integer
);