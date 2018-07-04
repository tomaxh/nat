create database nat;
\c nat;
drop table names_and_terms;
drop table categories;

create table categories (
	id serial primary key,
	name varchar(100) not null,
	keywords varchar(800),
	parent_id integer references categories(id)
);

create table names_and_terms (
	id serial primary key,
	verified varchar(800) not null,
	verified_plaintext varchar(800) not null,
	verified_alternates varchar(800),
	verification_source varchar(1000),
	description text,
	description_plaintext text,
	comments text,
	relationship text,
	location text,
	alpha_order varchar(320) not null,
	created_time timestamp not null, 
	created_by varchar(320) not null,
	modified_time timestamp,
	modified_by varchar(320),
	revised_time timestamp,
	category_id integer references categories (id)
);
