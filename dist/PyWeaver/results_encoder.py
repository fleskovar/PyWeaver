import numpy as np

def encode(obj):

    encoders = dict()
    encoders[np.ndarray] = numpy_ndarray_encoder

    if type(obj) in encoders:
        enc_obj = encoders[type(obj)](obj)
    else:
        # If object type not in custom encoders, return it as is
        enc_obj = obj

    return enc_obj


def numpy_ndarray_encoder(obj):
    # Gets a numpy array and transforms it into a list
    return obj.tolist()
