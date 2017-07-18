-- purge the app from the database DEVELOPMENT ONLY!!

-- delete migrations from the migrations table
DELETE FROM django_migrations WHERE app="simulation";

--generate a drop script containing all the tables in simulation
SELECT 'DROP TABLE IF EXISTS '||tbl_name||';'  AS statement
FROM SQLITE_MASTER
WHERE tbl_name like 'simulation_%' AND type="table";

--now delete the migrations in simulation/migrations
--now run the script you generated in step 2