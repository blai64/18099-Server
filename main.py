from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

app = Flask(__name__)
api = Api(app)

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

api.add_resource(GetPOIData, '/cmu-campus-app/')

if __name__ == '__main__':
    app.run(debug=True)