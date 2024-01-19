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



	