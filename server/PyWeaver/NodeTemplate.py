class NodeTemplate(object):
    """
    Class that stores the information (logic, ui, ui logic, metadata and documentation) for the nodes of the library
    """

    def __init__(self, lib_id=None, code_path=None, ui_code_path=None, ui_script_path=None, meta_path=None, doc_path=None):
        self.lib_id = lib_id
        self.code_path = code_path
        self.ui_code_path = ui_code_path
        self.ui_script_path = ui_script_path
        self.meta_path = meta_path
        self.doc_path = doc_path

    def render_template(self):
        render = dict()

        render['lib_id'] = self.lib_id
        render['code'] = self.read_file(self.code_path)
        render['display_code'] = self.read_file(self.ui_code_path)
        render['display_act_code'] = self.read_file(self.ui_script_path)
        render['meta'] = self.read_file(self.meta_path)
        render['doc'] = self.read_file(self.doc_path)

        return render

    def read_file(self, path):

        if path is None:
            content = None
        else:
            f = open(path)
            content = f.read()
            f.close()

        return content
