#this code is for the backend assignment from talkinglands
# using geoJSON format for spatial data as it can store attributes also

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2.functions import ST_GeomFromText
from models import db, MultiPointModel, MultiPolygonModel 
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# multipoint
# implemented store, retrieve, update, delete
from geoalchemy2.functions import ST_GeomFromGeoJSON

@app.route("/add_multipoint", methods=["POST"])
def add_multipoint():
    try:
        data = request.get_json()
        name = data.get("name")
        geojson = data.get("geojson") 

        if not name or not geojson:
            return jsonify({"error": "Name and GeoJSON are required"}), 400

        multipoint_geom = ST_GeomFromGeoJSON(str(geojson))


        multipoint = MultiPointModel(name=name, location=multipoint_geom)
        db.session.add(multipoint)
        db.session.commit()

        return jsonify({"message": "MultiPoint added successfully!", "id": multipoint.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


from geoalchemy2.functions import ST_AsGeoJSON

@app.route("/get_multipoints", methods=["GET"])
def get_multipoints():
    try:
        multipoints = MultiPointModel.query.all()
        result = []
        for multipoint in multipoints:
            geojson = db.session.scalar(ST_AsGeoJSON(multipoint.location)) 

            result.append({
                "id": multipoint.id,
                "name": multipoint.name,
                "geojson": geojson  
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update_multipoint/<int:id>", methods=["PUT"])
def update_multipoint(id):
    try:
        data = request.get_json()
        name = data.get("name")
        geojson = data.get("geojson")

        multipoint = MultiPointModel.query.get(id)
        if not multipoint:
            return jsonify({"error": "MultiPoint not found"}), 404

        if name:
            multipoint.name = name

        if geojson:
            multipoint.location = ST_GeomFromGeoJSON(str(geojson))

        db.session.commit()
        return jsonify({"message": "MultiPoint updated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete_multipoint/<int:id>", methods=["DELETE"])
def delete_multipoint(id):
    try:
        multipoint = MultiPointModel.query.get(id)
        if not multipoint:
            return jsonify({"error": "MultiPoint not found"}), 404

        db.session.delete(multipoint)
        db.session.commit()
        return jsonify({"message": "MultiPoint deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


from geoalchemy2.shape import from_shape
from shapely.geometry import MultiPolygon


# multipolygon
# implemented store, retrieve, update, delete
@app.route("/add_multipolygon", methods=["POST"])
def add_multipolygon():
    try:
        data = request.get_json()
        name = data.get("name")
        geojson = data.get("geojson")  

        if not name or not geojson:
            return jsonify({"error": "Name and GeoJSON are required"}), 400

 
        shapely_multipolygon = MultiPolygon(geojson["coordinates"])
   #     shapely_multipolygon = MultiPolygon([tuple(polygon) for polygon in geojson["coordinates"]])

        multipolygon_geom = from_shape(shapely_multipolygon, srid=4326)


        multipolygon = MultiPolygonModel(name=name, shape=multipolygon_geom)
        db.session.add(multipolygon)
        db.session.commit()

        return jsonify({"message": "MultiPolygon added successfully!", "id": multipolygon.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

from geoalchemy2.functions import ST_AsGeoJSON

@app.route("/get_multipolygons", methods=["GET"])
def get_multipolygons():
    try:
        multipolygons = MultiPolygonModel.query.all()
        result = []
        for multipolygon in multipolygons:
            geojson = db.session.scalar(ST_AsGeoJSON(multipolygon.shape)) 

            result.append({
                "id": multipolygon.id,
                "name": multipolygon.name,
                "geojson": geojson  
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_multipolygon/<int:id>", methods=["PUT"])
def update_multipolygon(id):
    try:
        data = request.get_json()
        name = data.get("name")
        geojson = data.get("geojson")

        multipolygon = MultiPolygonModel.query.get(id)
        if not multipolygon:
            return jsonify({"error": "MultiPolygon not found"}), 404

        if name:
            multipolygon.name = name

        if geojson:
            multipolygon.shape = ST_GeomFromGeoJSON(str(geojson))

        db.session.commit()
        return jsonify({"message": "MultiPolygon updated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/delete_multipolygon/<int:id>", methods=["DELETE"])
def delete_multipolygon(id):
    try:
        multipolygon = MultiPolygonModel.query.get(id)
        if not multipolygon:
            return jsonify({"error": "MultiPolygon not found"}), 404

        db.session.delete(multipolygon)
        db.session.commit()
        return jsonify({"message": "MultiPolygon deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

from geoalchemy2.functions import ST_Contains, ST_Intersects

# for finding multipoints in multipolygons
@app.route("/find_multipoints_inside/<int:multipolygon_id>", methods=["GET"])
def find_multipoints_inside(multipolygon_id):
    try:
        multipolygon = MultiPolygonModel.query.get(multipolygon_id)
        if not multipolygon:
            return jsonify({"error": "MultiPolygon not found"}), 404

        multipoints_inside = (
            db.session.query(MultiPointModel)
            .filter(ST_Intersects(multipolygon.shape, MultiPointModel.location)) 
            .all()
        )

        result = []
        for point in multipoints_inside:
            geojson = db.session.scalar(ST_AsGeoJSON(point.location))
            result.append({
                "id": point.id,
                "name": point.name,
                "geojson": geojson
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True) 
