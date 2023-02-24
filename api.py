import json
from flask import Flask, jsonify
from flask_restx import Resource, Api, reqparse
from flask_restx import fields, marshal
from RM import ResourceManager

app = Flask(__name__)
api = Api(app)

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('servers', type=int)
parser.add_argument('cores', type=int)
parser.add_argument('msize', type=int)
parser.add_argument('ssize', type=int)

global resourceManager
resourceManager = ResourceManager();

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
                return {'Error - not enough space'}, 500

            return res, 201
        except:
            return {'Error'}, 500

@api.route('/v1.0.0/allocation/<int:delete_id>')
class Delete(Resource):
    def delete(self, delete_id):
        try:
            resourceManager.deleteSession(delete_id)
            return {}, 200
        except:
            return {'Error'}, 500

@api.route('/v1.0.0/allocation/delete/all/yes')
class Delete(Resource):
    def delete(self):
        try:
            resourceManager.deleteAllSessions()
            return {}, 200
        except:
            return {'Error'}, 500
 
@api.route('/sessions')
class Sessions(Resource):
    def get(self):
        sessions = resourceManager.getSessions()
        sessions_fields = {'sessions_up': fields.List(fields.String)}

        data = {'sessions_up' : sessions}
        json.dumps(marshal(data, sessions_fields))
        
        return (marshal(data, sessions_fields))

if __name__ == '__main__':
    app.run(debug=True)
    