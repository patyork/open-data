from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import requests as r

import humboldt

app = Flask(__name__)
api = Api(app)

H = humboldt.assessor()

def isEmpty(x):
	if x is None or x == '': return True
	return False
	
def testClient():
	return app.test_client()

class Status(Resource):
	def get(self):
		return {'status':201, 'hello': 'world'}
		
class AssessorSearch(Resource):
	def get(self):
		parser = reqparse.RequestParser(bundle_errors=True)
		parser.add_argument('parcelNum', type=unicode, help="Parcel Number starting value")
		parser.add_argument('parcelNumRange', type=unicode, help="Parcel Number value range end")
		parser.add_argument('ownerName', type=unicode, help="Partial Owner Name")
		parser.add_argument('location', type=unicode, help="Parial Location")
		
		args = parser.parse_args()
		
		if sum([1 for x in args.values() if not isEmpty(x)]) == 0:
			abort(400, message='At least one search term is required.')
		elif not isEmpty(args['parcelNumRange']) and isEmpty(args['parcelNum']):
			abort(400, message='parcelNum must be included in a ranged search.')
		
		try:
			return {'results' : H.search(args)}
			return {'results' : H.search({'srchpar1' : args['parcelNum']})}
		except r.ConnectionError as e:
			abort(504, message='Underlying connection to the governmental data source is unavaiable (County or City website down!)')
		except r.Timeout as e:
			abort(504, message='Underlying connection to the governmental data source is unavaiable (County or City website down!)')

api.add_resource(Status, '/')
api.add_resource(AssessorSearch, '/search')

if __name__ == '__main__':
	app.run(debug=True)
