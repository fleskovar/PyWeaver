
class Graph(object):

    def __init__(self):
        self.scope = None  # TODO: Implement scope
        self.nodes = {}
        self.edges = []
        self.adjacency_dict = dict()
        self.terminal_nodes = []  # List of nodes that have no output

    def add_node(self, node):
        node_id = node.id
        self.nodes[node_id] = node
        self.adjacency_dict[node_id] = dict()

    def delete_node(self, node_id):
        # Should add a check here to clear all i/o in the node just in case UI does not
        # properly trigger the deletion of all variables
        del self.nodes[node_id]

    def update_adjacency(self, source_node, target_node):
        self.edges.append((source_node.id, target_node.id))
        # self.add_to_adjacency_dict(source_node.id, target_node.id)

        # By only storing these connections in the adjacency dict, the traversal algorithm doesn't go upstream.
        # This ensures that all nodes are computed in the correct order.
        self.add_to_adjacency_dict(target_node.id, source_node.id)

    def make_connection(self, source_id, source_var, target_id, target_var):
        print 'making conn'
        source_b = self.nodes[source_id]
        target_b = self.nodes[target_id]
        source_b.connect_output(source_var, target_b, target_var)

    def delete_connection(self, source_id, source_var, target_id, target_var):
        node = self.nodes[source_id]
        node.disconnect_output(source_var, target_id, target_var)

    def add_to_adjacency_dict(self, node_id, neighbor_id):
        if neighbor_id not in self.adjacency_dict[node_id]:
            self.adjacency_dict[node_id][neighbor_id] = 1
        else:
            self.adjacency_dict[node_id][neighbor_id] += 1

    def remove_fom_adjacency_dict(self, node_id, neighbor_id):
        if neighbor_id in self.adjacency_dict[node_id]:
            self.adjacency_dict[node_id][neighbor_id] -= 1

        if self.adjacency_dict[node_id][neighbor_id] <= 0:
            del self.adjacency_dict[node_id][neighbor_id]

    def get_var_value(self, node_id, var):
        node = self.nodes[node_id]
        return node.results[var]

    def execute(self, scope_data):

        node_ids = [self.nodes[b].id for b in self.nodes if self.nodes[b].has_downstream() == False]

        for b_id in node_ids:
            node_stack = [b_id]
            exec_list = []
            while node_stack:
                current = node_stack.pop()
                for neighbor in self.adjacency_dict[current]:
                    # If neighbor is a key of the adjacency dict of "current id"
                    if not neighbor in exec_list:
                        node_stack.append(neighbor)
                exec_list.append(current)

            exec_list = exec_list[::-1]  # Reverse list to get proper execution order

            for id in exec_list:
                exe_node = self.nodes[id]
                node_scope = scope_data[id]

                if exe_node.scope != node_scope:
                    # If the scope of the function changed, set dirty and propagate
                    exe_node.set_dirty()

                if exe_node.dirty:
                    exe_node.execute(node_scope)

    def build_adjacency_dict(self):
        # TODO: build adjacency dict from edges list
        pass

    def build_execution_order_list(self):
        # TODO: part of the execute method should be refactored here
        return None