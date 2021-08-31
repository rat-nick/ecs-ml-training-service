import base64
import pickle
from typing import Any

def serialize(model: Any) -> str:
    pickled_model = pickle.dumps(model)
    return base64.b64encode(pickled_model)

def deserialize(bytestring: str) -> Any:
    pickled_model = base64.b64decode(bytestring)
    return pickle.loads(pickled_model)

