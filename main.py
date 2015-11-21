from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import mysql.connector

app = Flask(__name__)
api = Api(app)

cnx = mysql.connector.connect(user="root",password="cmu18099",host="127.0.0.1",database="18099db")

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

class GetPOIData(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('poi_id')
        args = parser.parse_args()
        cursor = cnx.cursor()

        poi_id = args["poi_id"]
        print(poi_id)
        # connect to mysql server
        # run sql queries
        # get the data as a python variable
        return {
            "success": True,
            "data": [{
                "poi_id": 5,
                "poi_data": {
                    "hero_image": "http://127.0.0.1/~vinays/cmu-campus-app/assets/hero_images/img_001",
                    "description": "Gates Hall",
                    "images": [
                        "http://52.27.55.252/content/buggy/media/photos/regular/buggy1.jpg",
                        "http://52.27.55.252/content/buggy/media/photos/regular/buggy2.jpg",
                        "http://52.27.55.252/content/buggy/media/photos/regular/buggy3.jpeg"
                    ]
                }
            }]
        }

class GetPOIDataFromDB(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('poi_id')
        args = parser.parse_args()
        cursor = cnx.cursor()

        poi_id = args["poi_id"]
        print(poi_id)
        # connect to mysql server
        # run sql queries
        query = ("select id,location,heroImage,description from content where id="+str(poi_id))
        print("query: "+query+"\n")
        cursor.execute(query)
        row = cursor.fetchone()
        
        images = []
        query_images = ("select pathToMedia from contentTable where poiId="+str(poi_id))
        cursor.execute(query_images)
        row_images = cursor.fetchone()
        while (row_images != None):
            images.append(row_images[0])
            row_images = cursor.fetchone()

        
        if (not (row == None)):
            print ("POI found: "+str(poi_id)+".\n")
            # ID number (starting from 0) corresponds to columns passed to select above
            print ("path to media: "+row[2]+".\n")
            
            return_value = {
                "success": True,
                "data": [{
                    "poi_id": poi_id,
                    "poi_data": {
                        "description" : row[3],
                        "images" : images,
                        "heroImage" : row[2]
                    }
                    }]
                }
        else:
            print ("POI not found: "+str(poi_id)+".\n")
            return_value = { "success": False,
                             "data": []
                             }

        return return_value

api.add_resource(GetPOIData, '/test/cmu-campus-app/')
api.add_resource(GetPOIDataFromDB, '/cmu-campus-app/')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')