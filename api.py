from flask import Flask, jsonify
from flask_restx import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('servers', type=int)
parser.add_argument('cores', type=int)
parser.add_argument('msize', type=int)
parser.add_argument('ssize', type=int)

global id
global idMap
id = 0
idMap = {}


@api.route('/allocation')
class Allocation(Resource):  
    def post(self):
        global id
        global idMap
        args = parser.parse_args()
        servers = args['servers']
        cores = args['cores']
        msize = args['msize']
        ssize = args['ssize']
        
        print("Req:" + str(servers) + "  " + str(cores) + "  " + str(msize) + "  " + str(ssize))
        id += 1
        idMap[id] = "Up"
        
        #serverCoresInfo1 = [4, 5, 6, 7, 12, 13, 14, 15];
        #serverCoresInfo2 = [0, 1, 2, 3, 4, 5, 6, 7];
        
        #serverInfo1 = {"name": "server0", "cores": 8, "core_list": serverCoresInfo1, "msize": 4, "ssize": 6}
        #serverInfo2 = {"name": "server4", "cores": 8, "core_list": serverCoresInfo2, "msize": 6, "ssize": 6}
        
        #retProperties = [serverInfo1, serverInfo2]
        
        retId = id
        retServers = servers
        retProperties = self.getRetJSON()
        return {"id": retId, "servers": servers, "properties": retProperties}
        
    def getRetJSON(self):
        retProperties = []
        
        serverCoresInfo = [4, 5, 6, 7, 12, 13, 14, 15];
        serverName = "server0"
        coresCount = 8
        msizeAlloc = 6
        ssizeAlloc = 6
        
        serverInfo = {"name": serverName, "cores": coresCount, "core_list": serverCoresInfo, "msize": msizeAlloc, "ssize": ssizeAlloc}
        retProperties.append(serverInfo)
        return serverInfo
        
@api.route('/delete')
class Delete(Resource):
    def delete(self):
        global idMap
        del idMap[1]
        return {}, 200
 
@api.route('/sessions')
class Sessions(Resource):
    def get(self):
        global idMap
        print(idMap)
        return {'sessions': 'up'}

if __name__ == '__main__':
    app.run(debug=True)
    