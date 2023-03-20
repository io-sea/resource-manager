import json
from flask import Flask, jsonify
from flask_restx import Resource, Api, reqparse
from flask_restx import fields, marshal
from .resource_manager import resource_manager

app = Flask('Resource Manager')
api = Api(app)

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('servers', type=int)
parser.add_argument('cores', type=int)
parser.add_argument('msize', type=int)
parser.add_argument('ssize', type=int)

global resourceManager
resourceManager = resource_manager();

@api.route('/v1.0.0/servers/allocation')
class Allocation(Resource):  
    def post(self):
        try:
            args = parser.parse_args()
            servers = args['servers']
            cores = args['cores']
            msize = args['msize']
            ssize = args['ssize']
        
            #print("Req:" + str(servers) + "  " + str(cores) + "  " + str(msize) + "  " + str(ssize))
            res = resourceManager.allocRequest(servers, cores, msize, ssize)
            if(res == -1):
                return {'message': 'Error - not enough space'}, 404

            return res, 201
        except:
            return {'message': 'Error'}, 500

@api.route('/v1.0.0/allocation/<int:delete_id>')
class Delete(Resource):
    def delete(self, delete_id):
        try:
            resourceManager.deleteSession(delete_id)
            return {}, 200
        except:
            return {'message': 'Error'}, 500

@api.route('/v1.0.0/allocation/delete/all/yes')
class Delete(Resource):
    def delete(self):
        try:
            resourceManager.deleteAllSessions()
            return {}, 200
        except:
            return {'message': 'Error'}, 500

def run_api():
    app.run(host="0.0.0.0", port=5000, debug=True)
    