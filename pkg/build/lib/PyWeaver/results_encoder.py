from flask.json import JSONEncoder
import numpy as np

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif obj is None:
                return 'null'
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        
        try:
            result = JSONEncoder.default(self, obj)
        except:
            result = str(obj)
        return result

