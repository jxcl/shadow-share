drop table if exists users;
create table users (
   user_name text primary key,
   public_key text not null
);
