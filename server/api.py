import pickle
import numpy as np
from services.serialization import serialize
from flask import Flask
from flask_restx import Resource, Api
from werkzeug.datastructures import FileStorage
from services.training import train
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pandas as pd
import config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config.from_object(config)

train_parser = api.parser()
train_parser.add_argument(
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


@api.route("/train")
@api.expect(train_parser)
class Model(Resource):
    def post(self):
        # parse the file in the request
        args = train_parser.parse_args()
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


predict_parser = api.parser()
predict_parser.add_argument(
    "var_file",
    location="files",
    type=FileStorage,
    required=True,
)

predict_parser.add_argument(
    "model_file",
    location="files",
    type=FileStorage,
    required=True,
)


@api.route("/predict")
@api.expect(predict_parser)
class Prediction(Resource):
    def post(self):
        args = predict_parser.parse_args()
        var_file = args["var_file"]
        model_file = args["model_file"]
        # split data into input and response vars
        inputs = pd.read_csv(var_file, index_col=0)
        medv = inputs["medv"]
        nox = inputs["nox"]
        predictor_cols = inputs.columns.difference(["medv", "nox"])
        inputs = inputs[predictor_cols].to_numpy()

        try:
            model = pickle.load(model_file)
            predictions = model.predict(inputs).tolist()
            y_true = np.array([medv, nox]).transpose()

            mae = mean_absolute_error(
                y_true,
                predictions,
                multioutput=[1, 0],
            )

            mse = mean_squared_error(
                y_true,
                predictions,
                multioutput=[1, 0],
            )

            return {
                "status": 200,
                "predictions": predictions,
                "MAE": mae,
                "MSE": mse,
            }

        except Exception as e:
            print(e)
            return {"message": "GET failed", "status": 500}


if __name__ == "__main__":
    app.run(port=config.PORT, host=config.HOST)
