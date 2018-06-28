import sys
sys.path.insert(0, '.')

import falcon
import werkzeug.serving
import urllib.parse

from query import query

class QueryEndpoint:

	def on_get(self, req, resp):
		resp.status = falcon.HTTP_200
		query_str = req.query_string
		query_dict = {
			one.split('=')[0]: urllib.parse.unquote(one.split('=')[1]).replace('&amp;', '&')
			for one in query_str.split('&')
		}
		print(query_dict)
		resp.append_header('Access-Control-Allow-Origin', '*')
		resp.body = query(query_dict['s'], query_dict.get('c'))

app = falcon.API()
app.add_route('/search', QueryEndpoint())

werkzeug.serving.run_simple('0.0.0.0', 7990, app)
