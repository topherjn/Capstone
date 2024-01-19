use capstone;

show tables;
-- events
-- locations
-- persons

-- So far it looks like the database holds data on individuals
-- who go missing, where they went missing, and when. 
-- Every table has an auto-increment primary key, and
-- the events table is a junction table between the persons
-- table and the location table

-- "YES" and "NO" represent whether or not a column in nullable

describe events;
-- event_id	int	NO	PRI		auto_increment
-- person_id	int	YES	MUL		
-- location_id	int	YES	MUL		
-- event_date	date	YES

describe locations;	
-- event_id	int	NO	PRI		auto_increment
-- person_id	int	YES	MUL		
-- location_id	int	YES	MUL		
-- event_date	date	YES		

describe persons;		
-- person_id	int	NO	PRI		auto_increment
-- name	text	NO			
-- status	text	YES			

-- are there any stored procedures?
show procedure status
where db = 'capstone';
-- no results

-- triggers?
show triggers;
-- no triggers

-- any views?
SHOW FULL TABLES IN capstone WHERE TABLE_TYPE LIKE 'VIEW';
-- no views

-- Basic queries
select * from locations;
-- 1	Park
-- 2	Street
-- 3	Mall
-- 4	Home
-- these are the basic locations.  no need to add more till instructed

select * from persons limit 10;
-- 1	John Doe	found
-- 2	Jane Smith	missing
-- 3	Tony Stark	found
-- 4	Bruce Banner	missing
-- 5	Steve Warner	found
-- 6	Natasha Romanoff	missing
-- 7	Peter Parker	found
-- 8	Happy Hogan	missing
-- 9	Mary Baith	missing
-- 10	Stephen Strange	found
-- first 10 persons with status
-- I added 1000 more with mock data but might change that later

select * from events limit 10;
-- 1	1	1	2023-01-01
-- 2	2	2	2023-02-01
-- 3	3	3	2023-03-01
-- 4	4	4	2023-04-01
-- 5	365	2	1928-09-01
-- 6	360	3	1918-11-29
-- 7	621	1	1949-08-07
-- 8	998	4	1921-09-08
-- 9	873	1	1939-01-15
-- 10	256	1	1968-11-23
-- first 10 of over 1000 events
-- every event after 4 is my mock data
-- might need to modify later - for one
-- thing we have over 1 century of dates

-- show the names and statuses, event dates, and locations
-- for all persons (results set to limit 10)
select p.name, p.status, e.event_date, l.location_name
from persons p inner join events e on 
     p.person_id = e.person_id inner join
     locations l on l.location_id = e.location_id
     order by p.name, e.event_date desc;
     
-- results
-- Abram Dumbelton	found	1984-08-28	Home
-- Abramo Lidgley	found	1996-05-01	Home
-- Abran Setterington	found	1948-02-16	Home
-- Addie Nuton	missing	2017-11-14	Home
-- Adele Gribbon	missing	1972-03-23	Street
-- Adele Gribbon	missing	1952-01-27	Park
-- Adena MacCoughen	missing	1997-06-17	Mall
-- Agace Corns	found	1992-12-08	Mall
-- Aida Tomaskunas	missing	1911-03-25	Home
-- Aigneis Simeone	found	1950-07-28	Home

-- show names and dates for people missing from home
select p.name, e.event_date
from persons p inner join events e
     on p.person_id = e.person_id
     where e.location_id = (select location_id
                            from locations
                            where location_name = 'Home');
-- results
-- Bruce Banner	2023-04-01
-- Bastien Schole	1921-09-08
-- Jamey Pentycost	2000-07-10
-- Ida Jillett	1997-02-19
-- Glynda Voase	1962-05-20
-- Virgie Lowcock	1952-09-26
-- Daveta Bramstom	1991-02-01
-- Wallache Kinkead	1957-01-17
-- Stacee Valintine	1973-10-05
-- Myriam Goddman	1991-05-30    

-- show the persons with the most events
-- i.e. the most irksome persons
-- defined as having more than 3 events
select p.name, count(e.person_id) Incidents
from persons p inner join events e
     on p.person_id = e.person_id
group by p.person_id
having Incidents> 3
order by Incidents desc, p.name;
-- results
-- Danell Austwick	5
-- Nadya Rumford	5
-- Queenie Ayshford	5
-- Sidnee Hayward	5
-- Bambi Descroix	4
-- Bastien Mattheus	4
-- Clayborne Coolson	4
-- Dorolice Barwack	4
-- Elaina Dovinson	4
-- Gwendolen Tidbald	4

-- which location is the most problematic?
select l.location_name, count(e.location_id) 'Number of Incidents'
from locations l inner join events e 
     on l.location_id = e.location_id
group by l.location_id
order by count(e.location_id) desc;
-- results
-- Mall	258
-- Home	254
-- Street	250
-- Park	238

-- which year had the most incidents
select year(e.event_date), l.location_name,count(e.event_id)
from `events` e inner join locations l 
      on l.location_id = e.location_id
group by  year(e.event_date), e.location_id
order by count(e.event_id) desc, year(e.event_date) desc;
-- results
-- 2011	Mall	7
-- 1972	Street	7
-- 1952	Home	7
-- 1924	Mall	7
-- 2016	Street	6
-- 2002	Mall	6
-- 1998	Mall	6
-- 1991	Home	6
-- 1977	Park	6
-- 1959	Street	6

--  - Scenario: Add 5 new records to each table (yea, just make stuff up that matches the existing data.
-- locations
-- Cinema
-- Restaurant
-- Road
-- Store
-- Festival
insert into locations (location_name) values ('Cinema');
insert into locations (location_name) values ('Restaurant');
insert into locations (location_name) values ('Road');
insert into locations (location_name) values ('Store');
insert into locations (location_name) values ('Festival');
select * from locations;
-- 1	Park
-- 2	Street
-- 3	Mall
-- 4	Home
-- 5	Cinema
-- 6	Restaurant
-- 7	Road
-- 8	Store
-- 9	Festival

-- persons
insert into persons (person_id, name, status) values (1, 'Birch Lindenstrauss', 'missing');
insert into persons (person_id, name, status) values (2, 'Victoir Spores', 'missing');
insert into persons (person_id, name, status) values (3, 'Joeann Roderigo', 'missing');
insert into persons (person_id, name, status) values (4, 'Joel Dupey', 'found');
insert into persons (person_id, name, status) values (5, 'Libbey Roblin', 'missing');

-- events
insert into events (event_id, person_id, location_id, event_date) values (1, 370, 4, '1964-12-20');
insert into events (event_id, person_id, location_id, event_date) values (2, 535, 2, '1973-12-07');
insert into events (event_id, person_id, location_id, event_date) values (3, 551, 2, '1961-07-21');
insert into events (event_id, person_id, location_id, event_date) values (4, 837, 3, '1965-08-23');
insert into events (event_id, person_id, location_id, event_date) values (5, 365, 2, '1928-09-01');



	







			
	
	


	