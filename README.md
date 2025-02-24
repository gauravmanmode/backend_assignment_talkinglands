# Backend Assignment
This repo provides a REST API for storing, updating and retrieving the spatial 
based multiple point data and multiple polygon data .
Backend: Flask, Flask-SQLAlchemy, GeoAlchemy2
Database: PostgreSQL + PostGIS

set up
pip install -r requirements.txt

Set up database
$sudo -u postgres psql
CREATE USER test WITH PASSWORD '123';
ALTER ROLE test WITH SUPERUSER;
CREATE DATABASE spatial_db1;
\c spatial_db
CREATE EXTENSION postgis;

for password based auth with user test
sudo nano /etc/postgresql/15/main/pg_hba.conf
change local   all   all   peer to 
       local   all   all   md5


create database
python3 db_init.py

start the server
python3 app.py

testing 
python3 test.py
