from pandas.core.frame import DataFrame
from sklearn.neural_network import MLPRegressor
from typing import List


def train(data: DataFrame, response_vars: List[str]) -> MLPRegressor:
    # split response and predictor vars
    y = data[response_vars]
    predictor_vars = data.columns.difference(response_vars)
    X = data[predictor_vars]
    # create and fit the model to the data
    model = MLPRegressor()
    model.fit(X, y)

    return model
