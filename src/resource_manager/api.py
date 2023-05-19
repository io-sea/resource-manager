import json
from flask import Flask, jsonify
from flask_restx import Resource, Api, reqparse
from flask_restx import fields, marshal
from resource_manager import resource_manager

app = Flask('Resource Manager')
api = Api(app)

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('user', type=str)
parser.add_argument('user_slurm_token', type=str)
parser.add_argument('type', type=str)
parser.add_argument('servers', type=int)
parser.add_argument("attributes", type=dict)

global resourceManager
resourceManager = resource_manager();

@api.route('/v2.0.0/ephemeralservice/reserve')
class Allocation(Resource):  
    def post(self):
        try:
            args = parser.parse_args()
            name = args['name']
            user = args['user']
            user_slurm_token = args['user_slurm_token']
            es_type = args['type']
            servers = args['servers']
            attributes = args['attributes']

            cores = attributes['cores']
            msize = attributes['msize']
            ssize = attributes['ssize']
            try:
                flavor = attributes['flavor']
            except:
                flavor = None
        except:
            return {'message': 'Error - Arguments parser'}, 500

        if(name == None or user == None or user_slurm_token == None or es_type == None):
            return {'message': 'Error - Missing argument'}, 500
        
        try:
            print("Req:" + str(name) + "  " + str(user) + "  " + str(es_type) + "  " + str(servers) + "  " + str(attributes))
            print("Req:" + str(servers) + "  " + str(cores) + "  " + str(msize) + "  " + str(ssize))

            if(flavor != None):
                flavor_property = resourceManager.getFlavorProperty(flavor)
                if(flavor_property == -1):
                    return {'message': 'Error - Flavor does not exist'}, 500

                cores = flavor_property['cores']
                msize = flavor_property['msize']
                ssize = flavor_property['ssize']

            res = resourceManager.allocRequest(name, user, user_slurm_token, es_type, servers, cores, msize, ssize)
            if(res == -1):
                return {'message': 'Error - not enough space'}, 404

            return {'name': res}, 200
        except:
            return {'message': 'Error - AllocRequest'}, 500

@api.route('/v2.0.0/allocation/<int:delete_id>')
class Delete(Resource):
    def delete(self, delete_id):
        try:
            resourceManager.deleteSession(delete_id)
            return {}, 200
        except:
            return {'message': 'Error'}, 500

@api.route('/v2.0.0/server/allocation/<service_name>')
class GetAllocation(Resource):
    def get(self, service_name):
        try:
            res = resourceManager.getAssignedResource(service_name)
            if (res == -1):
                return {'message': 'Allocation request failed because the reservation is missing'}, 500
            if (res == -2):
                return {'message': 'Allocation request failed because the reservation is ALLOCATED'}, 501
            return res, 200
        except:
            return {'message': 'Error'}, 502

@api.route('/v2.0.0/allocation/delete/all/yes')
class Delete(Resource):
    def delete(self):
        try:
            resourceManager.deleteAllSessions()
            return {}, 200
        except:
            return {'message': 'Error'}, 500

def run_api():
    app.run(host="0.0.0.0", port=5000, debug=True)
    