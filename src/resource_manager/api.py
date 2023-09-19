import json
from flask import Flask, jsonify
from flask_restx import Resource, Api, reqparse
from flask_restx import fields, marshal
from resource_manager import resource_manager
from logger import *
from settings import settings

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
global sett
resourceManager = resource_manager()
sett = settings()

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
            rm_logger.info('Allocation call - Error - Arguments parser (%s)', name)
            return {'message': 'Error - Arguments parser'}, 500

        if(name == None or user == None or user_slurm_token == None or es_type == None):
            rm_logger.info('Allocation call - Error - Missing argument (%s)', name)
            return {'message': 'Error - Missing argument'}, 500

        print("location:" + str(location))
        
        try:
            print("Req:" + str(name) + "  " + str(user) + "  " + str(es_type) + "  " + str(servers) + "  " + str(attributes))

            if(flavor != None):
                flavor_property = resourceManager.getFlavorProperty(flavor)
                if(flavor_property == -1):
                    rm_logger.info('Allocation call - Error - Flavor {%s} does not exist (%s)', flavor, name)
                    return {'message': 'Error - Flavor does not exist'}, 500

                cores = flavor_property['cores']
                msize = flavor_property['msize']
                ssize = flavor_property['ssize']

            rm_logger.info('Allocation call - Start (%s)\n       Req: name:%s  user:%s  es_type:%s  servers:%s  attributes:%s', name, name, user, es_type, str(servers), str(attributes))
            res = resourceManager.allocRequest(name, user, user_slurm_token, es_type, servers, cores, msize, ssize, targets, mountpoint, location)
            if(res == -1):
                rm_logger.info('Allocation call - Not enough space - added to Queue (%s)\n       Req: name:%s  user:%s  es_type:%s  servers:%s  attributes:%s', name, name, user, es_type, str(servers), str(attributes))
                return {'message': 'Not enough space - added to Queue'}, 200

            if(res == 10):
                rm_logger.info('Allocation call - Already in queue (%s)\n       Req: name:%s  user:%s  es_type:%s  servers:%s  attributes:%s', name, name, user, es_type, str(servers), str(attributes))
                return {'message': 'Already in queue'}, 500

            if(res == 11):
                rm_logger.info('Allocation call - Reservation already done (%s)\n       Req: name:%s  user:%s  es_type:%s  servers:%s  attributes:%s', name, name, user, es_type, str(servers), str(attributes))
                return {'message': 'Reservation already done'}, 500

            rm_logger.info('Allocation call - Done (%s)', name)
            return {'name': res}, 200
        except Exception as ex:
            print(str(ex))
            rm_logger.info('Allocation call - Error - Exp: %s (%s)', str(ex), name)
            return {'message': 'Error - AllocRequest'}, 500

@api.route('/v2.0.0/server/allocation/<delete_name>')
class Delete(Resource):
    def delete(self, delete_name):
        try:
            ret = resourceManager.deleteSession(delete_name)
            if(ret == 0):
                rm_logger.info('Delete call - Done (%s)', delete_name)
            if(ret == 1):
                rm_logger.info('Delete call - Done - from Queue (%s)', delete_name)
            if(ret == -1):
                rm_logger.info('Delete call - Error - Reservation does not exist (%s)', delete_name)
                return {'message': 'Error - Reservation does not exist'}, 500
            return {}, 200
        except Exception as ex:
            print(str(ex))
            rm_logger.info('Delete call - Error - Exp: %s (%s)', str(ex), delete_name)
            return {'message': 'Error'}, 500

@api.route('/v2.0.0/server/allocation/<service_name>')
class GetAllocation(Resource):
    def get(self, service_name):
        try:
            res = resourceManager.getAssignedResource(service_name)
            if (res == -1):
                rm_logger.info('GetAllocation call - Allocation request failed because the reservation is missing (%s)', service_name)
                return {'message': 'Allocation request failed because the reservation is missing'}, 500
            #if (res == -2):
            #    rm_logger.info('GetAllocation call - Allocation request failed because the reservation is ALLOCATED (%s)', service_name)
            #    return {'message': 'Allocation request failed because the reservation is ALLOCATED'}, 500
            if (res == 409):
                rm_logger.info('GetAllocation call - Reservation exists but no resources available yet - In Queue (%s)', service_name)
                return {'message': 'Reservation exists but no resources available yet - In Queue'}, 409
            
            rm_logger.info('GetAllocation call - Done (%s)', service_name)
            return res, 200
        except Exception as ex:
            print(str(ex))
            rm_logger.info('GetAllocation call - Error - Exp: %s (%s)', str(ex), service_name)
            return {'message': 'Error'}, 502

@api.route('/v2.0.0/server/resources/<server_name>')
class GetServerResources(Resource):
    def get(self, server_name):
        try:
            if(server_name == 'all'):
                res = resourceManager.getAllServersResource()
                if (res == -1):
                    rm_logger.info('GetServerResources call - Error - Server does not exist(%s)', server_name)
                    return {'message': 'Server does not exist'}, 500
                rm_logger.info('GetServerResources call - Done (%s)', server_name)
                return res, 200
            else:
                res = resourceManager.getServerResource(server_name)
                if (res == -1):
                    rm_logger.info('GetServerResources call - Error - Server does not exist(%s)', server_name)
                    return {'message': 'Server does not exist'}, 500
                rm_logger.info('GetServerResources call - Done (%s)', server_name)
                return res, 200
        except Exception as ex:
            rm_logger.info('GetServerResources call - Error - Exp: %s (%s)', str(ex), server_name)
            return {'message': 'Error'}, 500

@api.route('/v2.0.0/allocation/delete/all/yes')
class Delete(Resource):
    def delete(self):
        try:
            resourceManager.deleteAllSessions()
            return {}, 200
        except:
            return {'message': 'Error'}, 500

@api.route('/v2.0.0/server/init_db')
class InitDB(Resource):
    def get(self):
        try:
            res = resourceManager.initDB(sett.getSettings())
            if(res != 0):
                return {'message': 'DB init problem - test'}, 200
            return {'message': 'DB is ready'}, 200
        except Exception as ex:
            rm_logger.info('InitDB call - Error - Exp: %s', str(ex))
            return {'message': 'Error'}, 500

def run_api():
    print("Starting...")
    ret = sett.loadConfig()

    if(ret == -1):
        print("loadConfig - Error - config.txt does not exist")
        rm_logger.info('loadConfig - Error - config.txt does not exist')
        return -1

    config = sett.getSettings()
    rm_logger.info('loadConfig - [Key, Value] - ' + str(config))
    sett.printSettings()

    
    try:
        res = resourceManager.initDB(sett.getSettings())
        if(res == -1):
            print("DB Init already done")
        if(res != 0 and res !=-1):
            print('DB init problem - test')
        print('DB is ready')
    except Exception as ex:
        rm_logger.info('InitDB call - Error - Exp: %s', str(ex))

    #app.run(host="0.0.0.0", port=5000, debug=True)
    #app.run(host=sett.getDicValue("api_adress"), port= int(sett.getDicValue("api_port")), debug=True)

   
        
    