select count(*) as 'total' from cookies;
select count(*) as 'with' from cookies where banner_exists = 1;
select count(*) as 'without' from cookies where banner_exists = 0;