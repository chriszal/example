import falcon
import json


class Cors:

    def process_request(self, req, resp):
        # print("In req")
        resp.set_header('Access-Control-Allow-Origin', 'http://0.0.0.0:3000')
        resp.set_header('Access-Control-Allow-Methods', 'DELETE, PUT, POST, GET')
        resp.set_header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type,Authorization, Accept, apisid, publickey, sessionid')
        resp.set_header('Access-Control-Expose-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)
        if req.method == 'OPTIONS':
            raise falcon.HTTPStatus(falcon.HTTP_200, body='\n')

    def process_response(self, req, resp, resource, req_succeeded):
        if 'result' not in resp.context:
            return
        resp.body = json.dumps(resp.context['result'])