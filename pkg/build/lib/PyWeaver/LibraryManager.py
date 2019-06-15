import os, inspect, shutil

from NodeTemplate import NodeTemplate

class LibraryManager(object):

    def __init__(self):
        templates, names, tree = self.build_templates()
        self.templates = templates
        self.names = names
        self.tree = tree


    def build_templates(self):
        cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        templates_cwd = os.path.join(cwd, 'lib')

        template_paths, tree = self.find_templates(templates_cwd)
        templates, names = self.compile_templates(template_paths)

        return templates, names, tree

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
                file_path = os.path.join(p, f)
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
        # TODO: refactor this... use os.walk()
        root_name = 'Node Library'
        queue = [root_name]
        queue = list(zip(queue, [lib_path]*len(queue)))
        child_folders = []
        template_paths = []
        tree = []
        lib_id = 0
        tree_id = 0
        tree_elements = dict()

        tree_obj = {}
        tree_obj['id'] = tree_id
        tree_obj['name'] = root_name
        tree_obj['children'] = []
        tree.append(tree_obj)
        tree_elements[lib_path] = tree_obj
        tree_id += 1

        while queue:

            d = queue.pop()
            cwd = d[1]
            current_tree = tree_elements[cwd]
            dir_list = os.listdir(cwd)

            for f in dir_list:
                tree_obj = {}
                tree_obj['name'] = f
                tree_obj['id'] = tree_id
                tree_id += 1

                #Check if the element of the dir is a calculation
                f_elements = os.listdir(os.path.join(d[1], f))
                has_files = True in map(lambda x: os.path.isfile(x), map(lambda x: os.path.join(d[1], f, x), f_elements))

                if has_files:
                    # We found files, this folder is a template this should break the  loop
                    template_paths.append(os.path.join(d[1], f))
                    tree_obj['lib_id'] = lib_id
                    lib_id += 1
                else:
                    tree_obj['children'] = []
                    tree_obj['path'] = os.path.join(d[1], f)
                    child_folders.append(f)

                current_tree['children'].append(tree_obj)
                tree_elements[os.path.join(d[1], f)] = tree_obj

            if child_folders:
                child_folders = list(zip(child_folders, map(lambda x: os.path.join(d[1], x), child_folders)))

            queue = queue + child_folders  # Add extra dirs to queue
            child_folders = []

        return template_paths, tree

    def get_render(self, lib_id):
        if lib_id in self.templates:
            return self.templates[lib_id].render_template()
        else:
            return None

    def get_template_names(self):
        return self.names

    def get_tree(self):
        return self.tree

    def save(self, path, node_data):
        name = node_data['name']

        # Validate that the name is nor already in use
        name = self.get_unique_name(path, name)  # If name is in use, append '_i' at the end

        cwd = os.path.join(path, name)

        os.mkdir(cwd)  # Creates the new folder

        python_file = os.path.join(cwd, 'code.py')
        f = open(python_file, "w+")
        f.write(node_data['code'])
        f.close()

        html_file = os.path.join(cwd, 'ui.html')
        f = open(html_file, "w+")
        f.write(node_data['display_code'])
        f.close()

        js_file = os.path.join(cwd, 'ui_script.js')
        f = open(js_file, "w+")
        f.write(node_data['display_act_code'])
        f.close()

    def new_folder(self, folder_path, folder_name):

        # Validate that the name is nor already in use
        folder_name = self.get_unique_name(folder_path, folder_name)  # If name is in use, append '_i' at the end
        os.mkdir(os.path.join(folder_path, folder_name))

    def delete_folder(self, path):
        shutil.rmtree(path, ignore_errors=True)

    def rename_folder(self, folder_path, folder_name):

        # Validate that the name is nor already in use
        folder_name = self.get_unique_name(folder_path, folder_name)  # If name is in use, append '_i' at the end

        os.rename(folder_path, os.path.join(os.path.dirname(folder_path), folder_name))  # Rename folder

    def get_unique_name(self, path, name):

        f_elements = os.listdir(path)

        if name in f_elements:
            count = 1
            new_name = name + '_' + str(count)
            while new_name in f_elements:
                count += 1
                new_name = name + '_' + str(count)

            name = new_name

        return name

    def import_package(self):
        pass

    def export_package(self):
        pass


class Package(object):

    def __init__(self):
        self.name = None
        self.author = None
        self.version = None
        self.description = None
        self.link = None
