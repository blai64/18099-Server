from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
import mysql.connector

# GET /cmu-campus-app/?poi_id=2 HTTP/1.1

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
        query = ("select exp_id,location,pathToMedia from content where exp_id="+str(poi_id))
        print("query: "+query+"\n")
        cursor.execute(query)

        row = cursor.fetchone()
        if (not (row == None)):
            print ("POI found: "+str(poi_id)+".\n")
            # ID number (starting from 0) corresponds to columns passed to select above
            print ("path to media: "+row[2]+".\n")
            
            return_value = {
                "success": True,
                "data": [{
                    "poi_id": poi_id,
                    "poi_data": {}
                    }]
                }
        else:
            print ("POI not found: "+str(poi_id)+".\n")
            return_value = { "success": False,
                             "data": []
                             }

        return return_value
                
        # get the data as a python variable
#        return {
#            "success": True,
#            "data": [{
#                "poi_id": 5,
#                "poi_data": {
#                    "hero_image": "http://127.0.0.1/~vinays/cmu-campus-app/assets/hero_images/img_001",
#                    "description": "Gates Hall",
#                    "images": [
#                        "http://127.0.0.1/~vinays/cmu-campus-app/assets/img_001",
#                        "http://127.0.0.1/~vinays/cmu-campus-app/assets/img_002",
#                        "http://127.0.0.1/~vinays/cmu-campus-app/assets/img_003"
#                    ]
#                }
#            }]
#        }

api.add_resource(GetPOIData, '/cmu-campus-app/')

if __name__ == '__main__':
    app.run(debug=True,port=4999)
