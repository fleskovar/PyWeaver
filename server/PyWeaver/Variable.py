
class Variable(object):

    def __init__(self, id, parent_id, io, is_ref = False, var_type=None, default_value=None):
        self.id = id
        self.parent_id = parent_id
        self.var_type=var_type
        self.io = io
        self.default_value = default_value
        self.value = None
        self.is_ref = is_ref  # If the variable should be passed by value or reference

    def set_value(self, val):
        self.value = val
        self.var_type = type(val).__name__