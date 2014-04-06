drop table if exists users;
drop table if exists files;

create table users (
   user_name text primary key,
   public_key text not null
);

create table files (
   user_name text primary key,
   target_user_name text,
   date_uploaded text
);