from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)

@api.route('/model')
class Model(Resource):
    def get(self):
        try:
            return {
                'message': 'GET invoked',
                'status': 200
            }
            
        except Exception as e:
            print(e)
            return {
                'message': 'GET failed',
                'status': 500
            }

    def post(self):
        try:
            return {
                'message': 'POST invoked',
                'status': 200
            }
            
        except Exception as e:
            print(e)
            return {
                'message': 'POST failed',
                'status': 500
            }
if __name__ == '__main__':
    app.run(debug=True)