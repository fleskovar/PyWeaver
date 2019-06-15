from collections import defaultdict
from Nodes import Node
import sys, os
from flask_socketio import emit

import uuid


class Graph(object):

    def __init__(self, session_id=None):
        self.scope = None  # TODO: Implement scope
        self.nodes = {}
        self.edges = []
        self.adjacency_dict = dict()
        self.terminal_nodes = []  # List of nodes that have no output
        self.xmlModel = None
        self.node_count = 0
        self.node_ids = []

        if session_id is None:
            self.session_id = str(uuid.uuid4())
        else:
            self.session_id = session_id

    def add_node(self, node_id=None, code=None):
        self.node_count += 1

        if node_id is None or node_id in self.node_ids:
            # Come up with a valid node id
            local_count = self.node_count
            node_id = 'n_'+str(local_count)

            while node_id in self.node_ids:
                local_count += 1
                node_id = 'n_'+str(local_count)

        node = Node(self, node_id, code=code)

        self.nodes[node_id] = node
        self.adjacency_dict[node_id] = dict()

        return node

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

        exec_list = self.sort_graph(self.nodes)

        for id in exec_list:
            exe_node = self.nodes[id]
            node_scope = scope_data[id]

            if exe_node.scope != node_scope:
                # If the scope of the function changed, set dirty and propagate
                exe_node.set_dirty()

            if exe_node.dirty:

                overlay_data = {}
                overlay_data['node_id'] = id
                overlay_data['overlay_type'] = 'exec'
                emit('set_node_overlay', overlay_data)

                sucess_run = exe_node.execute(node_scope)
                
                if sucess_run == False:                    
                    break
                else:
                    overlay_data = {}
                    overlay_data['node_id'] = id
                    overlay_data['overlay_type'] = 'ok'
                    emit('set_node_overlay', overlay_data)

    def build_adjacency_dict(self):
        # TODO: build adjacency dict from edges list
        pass

    def build_execution_order_list(self):
        # TODO: part of the execute method should be refactored here
        return None

    def sort_graph(self, nodes):
        exec_list = []

        in_degree = dict()
        graph = defaultdict(list)
        n_nodes = len(nodes)  # Total number of vertices

        # TODO: Investigate if this could be done in a more pythonic way
        for node_id in nodes:
            in_degree[node_id] = 0

        # TODO: Investigate if this could be done in a more pythonic way with output_vars_data
        for node_id in nodes:
            node = nodes[node_id]
            # Tracks if two nodes are already connected. Helps to keep into account multi-conns
            already_connected = []
            for var in node.output_vars_data:
                for edge in node.output_vars_data[var]:
                    if edge[0] not in already_connected:
                        in_degree[edge[0]] += 1  # Count the inner connection
                        already_connected.append(edge[0])  # Store the connection in case it appears again.
            graph[node_id] = already_connected

        # Initialize count of visited vertices
        cnt = 0

        # Create an queue and enqueue all vertices with
        # indegree 0
        queue = [n for n in in_degree if in_degree[n] == 0]

        # One by one dequeue vertices from queue and enqueue
        # adjacents if indegree of adjacent becomes 0
        while queue:

            # Extract front of queue (or perform dequeue)
            # and add it to topological order
            u = queue.pop(0)
            exec_list.append(u)

            # Iterate through all neighbouring nodes
            # of dequeued node u and decrease their in-degree
            # by 1
            for i in graph[u]:
                in_degree[i] -= 1
                # If in-degree becomes zero, add it to queue
                if in_degree[i] == 0:
                    queue.append(i)

            cnt += 1

        # Check if there was a cycle
        if cnt != n_nodes:
            return None
        else:
            # Print topological order
            return exec_list
