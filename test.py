# for testing purpose
# supposing real estate data
# each multipoint is a kind of real esate property
# each multipolygon is collection of cities


import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# 2BHK property locations as MultiPoint GeoJSON
multipoint_2bhk = {
    "name": "2BHK Properties",
    "geojson": {
        "type": "MultiPoint",
        "coordinates": [
            [77.5946, 12.9716],  # MG Road, Bangalore
            [77.6200, 12.9352],  # Koramangala, Bangalore
            [72.8777, 19.0760],  # South Mumbai
            [72.8245, 19.1320]   # Bandra, Mumbai
        ]
    }
}

# 3BHK property locations as MultiPoint GeoJSON
multipoint_3bhk = {
    "name": "3BHK Properties",
    "geojson": {
        "type": "MultiPoint",
        "coordinates": [
            [77.5645, 12.9260],  # Jayanagar, Bangalore
            [77.6476, 12.9784],  # Indiranagar, Bangalore
            [72.8679, 19.2288],  # Andheri, Mumbai
            [72.8057, 19.1550]   # Powai, Mumbai
        ]
    }
}

# Multiple city regions in Bangalore as MultiPolygon
# Multiple city regions in Bangalore as MultiPolygon (Fixed)
multipolygon_bangalore = {
    "name": "Cities in Bangalore",
    "geojson": {
        "type": "MultiPolygon",
        "coordinates": [
            [  # Whitefield
                [[77.7300, 12.9600], [77.7800, 12.9600], 
                 [77.7800, 13.0100], [77.7300, 13.0100], 
                 [77.7300, 12.9600]]
            ],
            [  # Electronic City
                [[77.6600, 12.8300], [77.7100, 12.8300], 
                 [77.7100, 12.8800], [77.6600, 12.8800], 
                 [77.6600, 12.8300]]
            ],
            [  # Jayanagar
                [[77.5500, 12.9000], [77.6000, 12.9000], 
                 [77.6000, 12.9500], [77.5500, 12.9500], 
                 [77.5500, 12.9000]]
            ]
        ]
    }
}

# Multiple city regions in Mumbai as MultiPolygon (Fixed)
multipolygon_mumbai = {
    "name": "Cities in Mumbai",
    "geojson": {
        "type": "MultiPolygon",
        "coordinates": [
            [  # Bandra
                [[72.8200, 19.0400], [72.8700, 19.0400], 
                 [72.8700, 19.0900], [72.8200, 19.0900], 
                 [72.8200, 19.0400]]
            ],
            [  # Andheri
                [[72.8300, 19.1100], [72.8800, 19.1100], 
                 [72.8800, 19.1600], [72.8300, 19.1600], 
                 [72.8300, 19.1100]]
            ],
            [  # Powai
                [[72.9000, 19.1200], [72.9500, 19.1200], 
                 [72.9500, 19.1700], [72.9000, 19.1700], 
                 [72.9000, 19.1200]]
            ]
        ]
    }
}


def test_add_multipoints():
    print("\n🟢 Adding 2BHK Properties...")
    response = requests.post(f"{BASE_URL}/add_multipoint", json=multipoint_2bhk)
    print(response.json())

    print("\n🟢 Adding 3BHK Properties...")
    response = requests.post(f"{BASE_URL}/add_multipoint", json=multipoint_3bhk)
    print(response.json())


def test_add_multipolygons():
    print("\n🟢 Adding Cities in Bangalore...")
    response = requests.post(f"{BASE_URL}/add_multipolygon", json=multipolygon_bangalore)
    print(response.json())

    print("\n🟢 Adding Cities in Mumbai...")
    response = requests.post(f"{BASE_URL}/add_multipolygon", json=multipolygon_mumbai)
    print(response.json())


def test_get_multipoints():
    print("\n🟢 Fetching MultiPoints (Properties)...")
    response = requests.get(f"{BASE_URL}/get_multipoints")
    print(json.dumps(response.json(), indent=4))


def test_get_multipolygons():
    print("\n🟢 Fetching MultiPolygons (Cities)...")
    response = requests.get(f"{BASE_URL}/get_multipolygons")
    print(json.dumps(response.json(), indent=4))


def test_find_properties_in_bangalore():
    print("\n🟢 Finding Properties inside Bangalore Cities...")
    # Assuming Bangalore Cities MultiPolygon has ID 1 in DB
    response = requests.get(f"{BASE_URL}/find_multipoints_inside/1")
    print(json.dumps(response.json(), indent=4))


if __name__ == "__main__":
    test_add_multipoints()
    test_add_multipolygons()
    test_get_multipoints()
    test_get_multipolygons()
    test_find_properties_in_bangalore()
