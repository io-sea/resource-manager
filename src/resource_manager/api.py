import json
from flask import Flask, jsonify
from flask_restx import Resource, Api, reqparse
from flask_restx import fields, marshal
from .resource_manager import resource_manager
from .logger import *

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
parser.add_argument("location", type=str, action='append')

global resourceManager
resourceManager = resource_manager();

@api.route('/v2.0.0/ephemeralservice/reserve')
class Allocation(Resource):  
    def post(self):
        name = None
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
            targets = mountpoint = location = None

            try:
                flavor = attributes['flavor']
            except:
                flavor = None
            try:
                targets = attributes['targets']
            except:
                targets = None
            try:
                mountpoint = attributes['mountpoint']
            except:
                mountpoint = None
            try:
                location = args['location']
            except:
                location = None
        except:
            logger.info('Allocation call - Error - Arguments parser (%s)', name)
            return {'message': 'Error - Arguments parser'}, 500

        if(name == None or user == None or user_slurm_token == None or es_type == None):
            logger.info('Allocation call - Error - Missing argument (%s)', name)
            return {'message': 'Error - Missing argument'}, 500

        print("location:" + str(location))
        
        try:
            print("Req:" + str(name) + "  " + str(user) + "  " + str(es_type) + "  " + str(servers) + "  " + str(attributes))

            if(flavor != None):
                flavor_property = resourceManager.getFlavorProperty(flavor)
                if(flavor_property == -1):
                    logger.info('Allocation call - Error - Flavor {%s} does not exist (%s)', flavor, name)
                    return {'message': 'Error - Flavor does not exist'}, 500

                cores = flavor_property['cores']
                msize = flavor_property['msize']
                ssize = flavor_property['ssize']

            res = resourceManager.allocRequest(name, user, user_slurm_token, es_type, servers, cores, msize, ssize, targets, mountpoint, location)
            if(res == -1):
                logger.info('Allocation call - Not enough space - added to Queue (%s)\n    Req: name:%s  user:%s  es_type:%s  servers:%s  attributes%s:', name, name, user, es_type, str(servers), str(attributes))
                return {'message': 'Not enough space - added to Queue'}, 404

            logger.info('Allocation call - Done (%s)\n    Req: name:%s  user:%s  es_type:%s  servers:%s  attributes:%s', name, user, es_type, str(servers), str(attributes))
            return {'name': res}, 200
        except Exception as ex:
            print(str(ex))
            logger.info('Allocation call - Error - Exp: %s (%s)', str(ex), name)
            return {'message': 'Error - AllocRequest'}, 500

@api.route('/v2.0.0/allocation/<delete_name>')
class Delete(Resource):
    def delete(self, delete_name):
        try:
            resourceManager.deleteSession(delete_name)
            return {}, 200
        except Exception as ex:
            print(str(ex))
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
        except Exception as ex:
            print(str(ex))
            return {'message': 'Error'}, 502

@api.route('/v2.0.0/server/resources/<server_name>')
class GetServerResources(Resource):
    def get(self, server_name):
        #try:
            if(server_name == 'all'):
                res = resourceManager.getAllServersResource()
                if (res == -1):
                    return {'message': 'Server does not exist'}, 500
                return res, 200
            else:
                res = resourceManager.getServerResource(server_name)
                if (res == -1):
                    return {'message': 'Server does not exist'}, 500
                return res, 200
        #except:
            return {'message': 'Error'}, 501

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
    