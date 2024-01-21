-- create the database named cap_evidence
create database cap_evidence;
use cap_evidence;

-- create evidence table
create table evidence (
    evidence_id INTEGER PRIMARY KEY auto_increment,
    description TEXT
);

-- create evidence changes table
create table evidence_changes(
    change_id integer primary key auto_increment,
    evidence_id integer,
    action varchar(10),
    change_date TIMESTAMP,
    foreign key (evidence_id) references evidence (evidence_id)
);

-- dummy data
insert into evidence (description) values ('Document A'), ('Photograph B'), ('Audio Recording C');

