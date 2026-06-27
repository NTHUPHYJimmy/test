create database fastapi;
use fastapi;
create table message(
	id bigint unsigned not null primary key auto_increment,
    author varchar(255) not null,
    content varchar(255) not null,
    create_time datetime default current_timestamp 
);
select * from message;
truncate table message;