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

-- Scenario: look at the tables.  What other information might we expect to collect?  
-- Create statements to add columns, specifying apropriate data types, and relationships if possible.
-- for people - maybe address information, phone number, dob, weight, weight, sex etc
-- for locations - this is pretty much a lookup table, so I would not add columns
-- for events - whatever we add should not violate 2NF (well technically 3NF since
-- we have a surrogate key), so it would be functionally dependent
-- on both the location and the person.  So type of event is out.  Any location data alone is out
-- I cannot think of any good candidates here except time-based info.  Maybe something like weather
-- or a description of the event maybe

alter table persons
add column street varchar(50),
add column city varchar(50),
add column state char(2),
add column phone char(10),
add column dob date,
add column weight int,
add column height int,
add column sex char(1);
-- reset persons data
delete from events where person_id > 12;
delete from persons where person_id > 12;
-- regenerated persons data with new columns
-- updated the addresses of the first 12 because
-- they seem to be Marvel characters - to one of the 
-- old addresses for Marvel in NYC
update persons set street = '387 Park Avenue South',
               city = 'New York',
               state = 'NY'
               where person_id < 13;

select * from persons limit 20;
-- 1	John Doe	missing	387 Park Avenue South	New York	NY					
-- 2	Jane Smith	found	387 Park Avenue South	New York	NY					
-- 3	Tony Stark	missing	387 Park Avenue South	New York	NY					
-- 4	Bruce Banner	found	387 Park Avenue South	New York	NY					
-- 5	Steve Warner	missing	387 Park Avenue South	New York	NY					
-- 6	Natasha Romanoff	found	387 Park Avenue South	New York	NY					
-- 7	Peter Parker	missing	387 Park Avenue South	New York	NY					
-- 8	Happy Hogan	found	387 Park Avenue South	New York	NY					
-- 9	Mary Baith	found	387 Park Avenue South	New York	NY					
-- 10	Stephen Strange	missing	387 Park Avenue South	New York	NY					
-- 11	Hank Pym	missing	387 Park Avenue South	New York	NY					
-- 12	Sam Wilson	found	387 Park Avenue South	New York	NY					
-- 13	Saunder Downey	found	14306 Monterey Avenue	Baltimore	MD	4107789096	1951-09-16	294	184	M
-- 14	Ruttger Coulbeck	found	3 Elka Road	Cincinnati	OH	5139230129	1913-10-24	58	23	M
-- 15	Teodorico Forstall	found	470 Warbler Terrace	Nashville	TN	6153783517	1920-05-07	836	416	M
-- 16	Elianora Pinckney	found	8 Northport Place	Vancouver	WA	3602770247	1975-12-27	839	368	F
-- 17	Cynthia Straughan	missing	17870 Kinsman Plaza	Alexandria	LA	3183168778	1986-03-12	126	498	M
-- 18	Nelle Jellybrand	found	186 Waxwing Place	Des Moines	IA	5158831967	2004-08-25	374	423	F
-- 19	Gilly Massen	found	9946 Sugar Avenue	Wilkes Barre	PA	5704187527	1978-03-21	1	94	M
-- 20	Lettie Woodard	found	704 Bunker Hill Plaza	Pasadena	CA	6265103143	1936-02-07	788	445	F

-- assinging sex
update persons set sex = 'M' 
where name in ('John Doe', 'Tony Stark', 'Bruce Banner', 'Steve Warner','Peter Parker', 'Happy Hogan', 'Stephen Strange', 'Hank Pym', 'Sam Wilson');

update persons set sex = 'F' 
where sex is null;

-- select * from persons limit 13;1	John Doe	found	387 Park Avenue South	New York	NY					M
-- 2	Jane Smith	missing	387 Park Avenue South	New York	NY					F
-- 3	Tony Stark	found	387 Park Avenue South	New York	NY					M
-- 4	Bruce Banner	found	387 Park Avenue South	New York	NY					M
-- 5	Steve Warner	missing	387 Park Avenue South	New York	NY					M
-- 6	Natasha Romanoff	missing	387 Park Avenue South	New York	NY					F
-- 7	Peter Parker	found	387 Park Avenue South	New York	NY					M
-- 8	Happy Hogan	missing	387 Park Avenue South	New York	NY					M
-- 9	Mary Baith	missing	387 Park Avenue South	New York	NY					F
-- 10	Stephen Strange	found	387 Park Avenue South	New York	NY					M
-- 11	Hank Pym	missing	387 Park Avenue South	New York	NY					M
-- 12	Sam Wilson	missing	387 Park Avenue South	New York	NY					M
-- 13	Saunder Downey	found	14306 Monterey Avenue	Baltimore	MD	4107789096	1951-09-16	294	184	M

-- seems like searches on dates would be common
create index idx_event_dates on events (event_date);
-- and people's names and status
create fulltext index idx_names on persons (name, status) ;
										
-- procedure to add a new person to db and an incident for them
DROP PROCEDURE IF EXISTS new_person_incident;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `new_person_incident`(new_person_name text,
                                 streetname varchar(50),
                                 cityname varchar(50),
                                 statename varchar(50),
                                 phonedigits char(10),
                                 bdate date,
                                 weight int,
                                 height int,
                                 sex char(1),
                                 place text,
                                 incident_date date)
BEGIN
	declare new_person_id int;
    declare this_location_id int;
    
	insert into persons (name, status, street, city, state, phone, dob, weight, height, sex)
			    values (new_person_name, 'missing', streetname, cityname, statename,
                        phonedigits, bdate, weight, height, sex);
                        
	SELECT 
    MAX(person_id)
FROM
    persons INTO new_person_id;
SELECT 
    l.location_id
FROM
    locations l
WHERE
    l.location_name = place INTO this_location_id;
    
    insert into events (person_id, location_id, event_date) 
                values (new_person_id, this_location_id, incident_date);

END$$

DELIMITER ;

-- test it
call new_person_incident('Tav', '1313 Mockingbird Lane', 'Boston', 'MA', '8678675309', '1776-07-04', 200, 76, 'M', 'Mall', '2019-04-04');

-- function to return the current number missing
USE `capstone`;
DROP function IF EXISTS `num_missing`;

DELIMITER $$
USE `capstone`$$
CREATE FUNCTION `num_missing` ()
RETURNS INTEGER
deterministic
BEGIN
	DECLARE nmissing INTEGER;
    
SELECT 
    COUNT(*)
FROM
    persons
WHERE
    status = 'missing' INTO nmissing;
    
RETURN nmissing;
END$$

DELIMITER ;

select num_missing(); -- 110 in my db
										
-- trigger to archive solved cases
-- based on person status going from
-- missing to found
drop table if exists closed_cases;
create table closed_cases (
    closed_case_id int primary key auto_increment,
    person_id int,
    closed_date date default (curdate()),
    CONSTRAINT `closed_fk1` FOREIGN KEY (`person_id`) REFERENCES `persons` (`person_id`)
);

-- trigger
drop trigger if exists close_case
delimiter $$
create trigger close_case
after update on persons
for each row
begin
    if old.status = 'missing' and new.status = 'found' then
        insert into closed_cases (person_id) values (new.person_id);
    end if;
end$$

delimiter ;

-- test
update persons set status = 'found' where person_id = 2;

select * from closed_cases;
-- closed_case_i   person_id  date
-- 1	2	2024-01-20

-- views
create view closed_case_info as
select p.name "Person's Name", concat(street, ' ', city, ' ', state) "Address", sex Sex, event_date 'Open Date', closed_date 'Closed Date'
from persons p inner join closed_cases c
     on p.person_id = c.person_id inner join
     events e on e.person_id = p.person_id;

--  test
select *
from closed_case_info;

-- results
-- Jane Smith	387 Park Avenue South New York NY	F	2023-02-01	2024-01-20









			
	
	


	