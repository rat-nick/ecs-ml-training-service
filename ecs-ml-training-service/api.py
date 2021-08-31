from service.serialization import serialize
from flask import Flask
from flask_restx import Resource, Api
from pandas.core.frame import DataFrame
from werkzeug.datastructures import FileStorage
from service.training import train
import pandas as pd
app = Flask(__name__)
api = Api(app)

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)

@api.route('/model')
@api.expect(upload_parser)
class Model(Resource):
    def post(self):
        
        # parse the file in the request
        args = upload_parser.parse_args()
        file = args['file']
        df = pd.read_csv(file)
        #remove Unnamed columns
        df = df.iloc[: , ~df.columns.str.contains('^Unnamed')]
        try:
            model = train(df, ['medv', 'nox'])
            serialized_model = serialize(model)
            return {
                'message': 'POST success',
                'serializedModel' : serialized_model,
                'status': 201,
            }
        except Exception as e:
            print(e)
            return {
                'message': 'POST failed',
                'status': 500
                
            }

@api.route('/predict/<int:id>')
class Prediction(Resource):
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

if __name__ == '__main__':
    app.run(debug=True)