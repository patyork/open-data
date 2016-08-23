from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import requests as r

import humboldt

app = Flask(__name__)
api = Api(app)

H = humboldt.assessor()

class Status(Resource):
	def get(self):
		return {'status':201, 'hello': 'world'}
		
class AssessorSearch(Resource):
	def get(self):
		parser = reqparse.RequestParser(bundle_errors=True)
		parser.add_argument('parcelNum', required=True, type=unicode, help="Parcel Number")
		
		args = parser.parse_args()
		
		try:
			return {'results' : H.search({'srchpar1' : args['parcelNum']})}
		except r.ConnectionError as e:
			abort(503, 'Underlying connection to the governmental data source is unavaiable (County or City website down!)')

api.add_resource(Status, '/')
api.add_resource(AssessorSearch, '/search')

if __name__ == '__main__':
	app.run(debug=True)
