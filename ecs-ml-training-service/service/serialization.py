import base64
import pickle

def serialize(model):
    pickled_model = pickle.dumps(model)
    return base64.b64encode(pickled_model)

def deserialize(bytestring: str):
    pickled_model = base64.b64decode(bytestring)
    return pickle.loads(pickled_model)

