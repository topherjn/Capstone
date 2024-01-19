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



			
	
	


	