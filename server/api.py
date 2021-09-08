import pickle
from services.serialization import serialize
from flask import Flask
from services.storage import read
from flask_restx import Resource, Api
from werkzeug.datastructures import FileStorage
from services.training import train
import pandas as pd
import config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config.from_object(config)

upload_parser = api.parser()
upload_parser.add_argument(
    "file",
    location="files",
    type=FileStorage,
    required=True,
)


@api.route("/probe")
@api.hide
class Probe(Resource):
    def get(self):
        return {"status": 200, "message": "probe successful"}


@api.route("/model")
@api.expect(upload_parser)
class Model(Resource):
    def post(self):
        # parse the file in the request
        args = upload_parser.parse_args()
        file = args["file"]
        df = pd.read_csv(file)
        # remove Unnamed columns
        df = df.iloc[:, ~df.columns.str.contains("^Unnamed")]
        try:
            # train the model
            model = train(df, ["medv", "nox"])
            outfile = f"{file.filename.split('.')[0]}.mod"
            return serialize(model, outfile)
        except Exception as e:
            print(e)

            return {"message": "POST failed", "status": 500}


upload_parser = api.parser()
upload_parser.add_argument(
    "file",
    location="files",
    type=FileStorage,
    required=True,
)


@api.route("/predict/<string:key>")
@api.expect(upload_parser)
class Prediction(Resource):
    def post(self, key):
        args = upload_parser.parse_args()
        file = args["file"]
        inputs = pd.read_csv(file).to_numpy()

        try:
            model = pickle.loads(read(key))
            predictions = model.predict(inputs)
            return {
                "status": 200,
                "predictions": predictions.tolist(),
            }

        except Exception as e:
            print(e)
            return {"message": "GET failed", "status": 500}


if __name__ == "__main__":
    app.run(port=config.PORT)
