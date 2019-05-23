import os, imp, sys, inspect
from NodeTemplate import NodeTemplate

class LibraryManager(object):

    def __init__(self):
        templates, names = self.build_templates()
        self.templates = templates
        self.names = names

    def build_templates(self):
        cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        templates_cwd = os.path.join(cwd, 'lib')

        template_paths = self.find_templates(templates_cwd)
        templates, names = self.compile_templates(template_paths)

        return templates, names

    def compile_templates(self, paths):

        n_temps = dict()
        lib_id = 0
        names = dict()

        for p in paths:
            files = [f for f in os.listdir(p) if os.path.isfile(os.path.join(p, f))]

            code_path = None
            ui_code_path = None
            ui_script_path = None
            meta_path = None
            doc_path = None
            name = os.path.basename(p)

            for f in files:
                file_path = os.path.isfile(os.path.join(p, f))
                if f.endswith('.py'):
                    code_path = file_path
                elif f.endswith('.html'):
                    ui_code_path = file_path
                elif f.endswith('.js'):
                    ui_script_path = file_path
                elif f.endswith('.xml'):
                    meta_path = file_path
                elif f.endswith('.txt'):
                    doc_path = file_path

            nt = NodeTemplate(lib_id, code_path, ui_code_path, ui_script_path, meta_path, doc_path)
            n_temps[lib_id] = nt
            names[name] = lib_id
            lib_id += 1

        return n_temps, names


    def find_templates(self, lib_path):
        # Gets the paths of all templates based on a DFS of the lib folder

        queue = ['root']
        queue = zip(queue, [lib_path]*len(queue))
        child_folders = []
        template_paths = []

        while queue:
            d = queue.pop()
            cwd = d[1]
            dir_list = os.listdir(cwd)

            for f in dir_list:
                if os.path.isfile(os.path.join(d[1], f)):
                    # We found files, this folder is a template this should break the  loop
                    template_paths.append(d[1])
                    break
                else:
                    child_folders.append(f)
            if child_folders:
                child_folders = zip(child_folders, map(lambda x: os.path.join(d[1], x), child_folders))
            queue = queue + child_folders # Add extra dirs to queue
            child_folders = []

        return template_paths

    def get_render(self, lib_id):
        return self.templates[lib_id].render_template()

    def get_template_names(self):
        return self.names
