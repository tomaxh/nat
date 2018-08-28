import sys
sys.path.insert(0, '.')

import falcon
import werkzeug.serving
import urllib.parse
import json
import psycopg2

import query

class QueryEndpointDelete:

	def on_get(self,req,resp):
		resp.append_header('Access-Control-Allow-Origin', '*')

		resp.status = falcon.HTTP_200
		itemID=req.query_string
		resp.body=query.queryDelete(itemID)
	
class QueryEndpointSearch:

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		query_str = req.query_string
		query_dict = {
			one.split('=')[0]: urllib.parse.unquote(one.split('=')[1]).replace('&amp;', '&')
			for one in query_str.split('&')
		}
		print(query_dict)
		resp.append_header('Access-Control-Allow-Origin', '*')
		resp.body = query.query(query_dict['s'], query_dict.get('c'))


class QueryEndpointGetOne():

	def on_get(self, req,resp):
		resp.append_header('Access-Control-Allow-Origin', '*')

		resp.status=falcon.HTTP_200
		itemID=req.query_string
		resp.body =  query.queryGetAllInfo(itemID)


class QueryEndpointSearchVerified:

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		query_str = req.query_string
		query_dict = {
			one.split('=')[0]: urllib.parse.unquote(one.split('=')[1]).replace('&amp;', '&')
			for one in query_str.split('&')
		}
		print(query_dict)
		resp.append_header('Access-Control-Allow-Origin', '*')
		resp.body = query.queryVerified(query_dict['s'], query_dict.get('c'))



class QueryEndpointInsert():

	def on_post(self, req, resp):
		resp.append_header('Access-Control-Allow-Origin', '*')
		resp.append_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
		
		data = json.loads(req.stream.read())
		resp.status = falcon.HTTP_200

		query.queryInsert(data)
		print(data)

	def on_options(self, req, resp):
		resp.append_header('Access-Control-Allow-Origin', '*')
		resp.append_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
		resp.append_header('Access-Control-Allow-Headers', 'Content-Type')
		


class QueryEndpointUpdate():
	def on_post(self, req, resp):
		resp.append_header('Access-Control-Allow-Origin', '*')
		resp.append_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
		
		data = json.loads(req.stream.read())
		resp.status = falcon.HTTP_200
		print("here")
		query.queryUpdates(data)
		print(data)

	def on_options(self, req, resp):
		resp.append_header('Access-Control-Allow-Origin', '*')
		resp.append_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
		resp.append_header('Access-Control-Allow-Headers', 'Content-Type')
	

'''
optional api
'''

app = falcon.API()
app.add_route('/vsearch', QueryEndpointSearchVerified())
app.add_route('/search',QueryEndpointSearch())
app.add_route('/insert',QueryEndpointInsert())
app.add_route('/delete',QueryEndpointDelete())
app.add_route('/get',QueryEndpointGetOne())
app.add_route('/update',QueryEndpointUpdate())
werkzeug.serving.run_simple('0.0.0.0', 7990, app)
