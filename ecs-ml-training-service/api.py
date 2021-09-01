import pickle
from flask import Flask
from service.storage import write, read
from flask_restx import Resource, Api
from werkzeug.datastructures import FileStorage
from service.training import train
import pandas as pd

app = Flask(__name__)
api = Api(app)


upload_parser = api.parser()
upload_parser.add_argument(
    "file",
    location="files",
    type=FileStorage,
    required=True,
)


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
            write(model, outfile)
            return {"status": 200}
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
    app.run(debug=True)
