from flask import Flask, jsonify
from flask_restx import Resource, Api, reqparse
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


@api.route('/allocation')
class Allocation(Resource):  
    def post(self):
        global resourceManager
        resourceManager.control()
        
        args = parser.parse_args()
        servers = args['servers']
        cores = args['cores']
        msize = args['msize']
        ssize = args['ssize']
        
        print("Req:" + str(servers) + "  " + str(cores) + "  " + str(msize) + "  " + str(ssize))

        return resourceManager.allocRequest(servers, cores, msize, ssize)
        
@api.route('/delete')
class Delete(Resource):
    def delete(self):

        return {}, 200
 
@api.route('/sessions')
class Sessions(Resource):
    def get(self):

        return {'sessions': 'up'}

if __name__ == '__main__':
    app.run(debug=True)
    