drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  descr text not null,
  done integer not null,
  dline datetime,
  finish timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
);