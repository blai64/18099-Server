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

        poi_id = args['poi_id']
        print("Poi id found: " + poi_id)
        # connect to mysql server
        
        # run sql queries
        
        # Query poi table
        query = ('select id,heroImage,description,locationId from pois where id='+str(poi_id))
        print('query: '+query+'\n')
        cursor.execute(query)
        poi_row = cursor.fetchone()
        
        #query content table
        images = []
        query_images = ('select pathToMedia from content where poiId='+str(poi_id))
        cursor.execute(query_images)

        for row in cursor:
            images.append('http://52.27.55.252/' + row[0].strip('"').lstrip('/var/www/html/'))
            

        # row_images = cursor.fetchone()
        # while (row_images != None):
        #     images.append(row_images[0])
        #     row_images = cursor.fetchone()

        #query location table
        #query_location = ("select lat,longi,locationCode,name,description from locations where id="+str(poi_row[1]))
        #cursor.execute(query_images);
        #location_row = cursor.fetchone()

        
        if (not (poi_row == None)):
            print ("POI found: "+str(poi_id)+".\n")
            # ID number (starting from 0) corresponds to columns passed to select above

            for path in images:
                print path
            
            return_value = {
                "success": True,
                "data": [{
                    "poi_id": poi_id,
                    "poi_data": {
                        "description" : poi_row[2],
                        "images" : images,
                        "heroImage" : poi_row[1]
                        #"location" : {
                        #    "lat" : location_row[0],
                        #    "longi" : location_row[1],
                        #    "locationCode" : location_row[2],
                        #    "name" : location_row[3],
                        #}

                    }
                    }]
                }
        else:
            print ("POI not found: "+str(poi_id)+".\n")
            return_value = { "success": False,
                             "data": []
                             }

        return return_value

class GetEventDataFromDB(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('event_id')
        args = parser.parse_args()
        cursor = cnx.cursor()

        event_id = args["event_id"]
        print(event_id)
        # connect to mysql server
        
        # run sql queries
        
        # Query poi table
        query = ("select id,locationId,startDateTime,fbLink,description from events where id="+str(event_id))
        print("query: "+query+"\n")
        cursor.execute(query)
        event_row = cursor.fetchone()
        

        #query location table
        query_location = ("select lat,longi,locationCode,name,description from locations where id="+str(event_row[1]))
        cursor.execute(query_images);
        location_row = cursor.fetchone()

        
        if (not (event_row == None)):
            print ("Event found: "+str(event_id)+".\n")
            # ID number (starting from 0) corresponds to columns passed to select above
            
            return_value = {
                "success": True,
                "data": [{
                    "event_id": event_id,
                    "event_data": {
                        "description" : event_row[4],
                        "startDateTime" : event_row[2],
                        "fbLink" : event_row[3],

                        "location" : {
                            "lat" : location_row[0],
                            "longi" : location_row[1],
                            "locationCode" : location_row[2],
                            "name" : location_row[3],
                        }

                    }
                    }]
                }
        else:
            print ("Event not found: "+str(event_id)+".\n")
            return_value = { "success": False,
                             "data": []
                             }

        return return_value


class GetMap(Resource):
    def get(self):   
        cursor = cnx.cursor()
        cursorL = cnx.cursor()
        # run sql queries
        
        # Query poi table
        pois = []
        query = ("select id,locationId,description from pois")
        print("query: "+query+"\n")
        cursor.execute(query)
        pois_row = cursor.fetchone()
        while (pois_row != None):
            query_location = ("select lat,longi,locationCode,name,description from locations where id="+str(pois_row[1]))
            cursorL.execute(query)
            location_row = cursorL.fetchone()
            pois.append({"poi_id" : pois_row[0],
                         "description" : pois_row[2],
                         "location" : {
                            "lat" : location_row[0],
                            "longi" : location_row[1],
                            "locationCode" : location_row[2],
                            "name" : location_row[3]
                            }
                        })

            pois_row = cursor.fetchone()

        if (not (pois.length == 0)):
            return_value = {
                "success": True,
                "pois" : pois
                }
        else:
            return_value = { "success": False,
                             "data": []
                             }
        return return_value



api.add_resource(GetPOIData, '/test/cmu-campus-app/')
api.add_resource(GetPOIDataFromDB, '/cmu-campus-app/pois/')
api.add_resource(GetEventDataFromDB, '/cmu-campus-app/events/')
api.add_resource(GetMap, '/cmu-campus-app/map/')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
