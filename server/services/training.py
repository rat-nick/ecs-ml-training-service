from pandas.core.frame import DataFrame
from sklearn.tree import DecisionTreeRegressor
from typing import List


def train(data: DataFrame, response_vars: List[str]) -> DecisionTreeRegressor:
    # split response and predictor vars
    y = data[response_vars]
    predictor_vars = data.columns.difference(response_vars)
    X = data[predictor_vars]
    # create and fit the model to the data
    model = DecisionTreeRegressor()
    model.fit(X, y)

    return model
