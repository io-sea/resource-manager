from flask import Flask, jsonify
from flask_restx import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('servers', type=int)
parser.add_argument('cores', type=int)

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
        
        print(str(servers) + "  " + str(cores))
        id += 1
        idMap[id] = "Up"
        return {'id': "'" + str(id) + "'"}

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
    