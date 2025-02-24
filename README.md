# Backend Assignment
This repo provides a REST API for storing, updating and retrieving the spatial 
based multiple point data and multiple polygon data .  
Backend: Flask, Flask-SQLAlchemy, GeoAlchemy2.  
Database: PostgreSQL + PostGIS.  

## REST API 

### MultiPoint (Properties)  
- **Add:** `POST /add_multipoint`  
- **Get All:** `GET /get_multipoints`  
- **Update:** `PUT /update_multipoint/<id>`  
- **Delete:** `DELETE /delete_multipoint/<id>`  

### MultiPolygon (Cities)  
- **Add:** `POST /add_multipolygon`  
- **Get All:** `GET /get_multipolygons`  
- **Update:** `PUT /update_multipolygon/<id>`  
- **Delete:** `DELETE /delete_multipolygon/<id>`  

### Queries  
- **Find multipoint in a multipolygon:** `GET /find_multipoints_inside/<multipolygon_id>`


## set up
```

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
make sure postgresql is up and running and postgis is installed using
sudo apt update
sudo apt install postgresql postgresql-contrib postgis postgresql-postgis

```

## for password based auth with user test
```
sudo nano /etc/postgresql/16/main/pg_hba.conf
change local   all   all   peer to 
       local   all   all   md5
```

## set up database
```
$sudo -u postgres psql
CREATE USER test WITH PASSWORD '123';
ALTER ROLE test WITH SUPERUSER;
CREATE DATABASE spatial_db1;
\c spatial_db
CREATE EXTENSION postgis;
```


## create database
python3 db_init.py

## start the server
python3 app.py

## testing 
python3 test.py
