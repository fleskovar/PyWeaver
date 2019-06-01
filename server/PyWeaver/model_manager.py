from flask_socketio import emit
import xmltodict


def load_xml(root, xml):

    results, scopes, cells, nodes, edges = parse_xml(xml)  # Parse xml
    generate_nodes(root, nodes)  # Generate nodes
    generate_edges(root, cells, edges)  # Generate connections

    if results is not None:
        emit('set_results', results)

    if results is not None:
        emit('set_scopes', scopes)


def create_node(graph_root, node_template):

    code = node_template['code'] if len(node_template['code']) > 0 else None
    node_id = node_template['id'] if 'id' in node_template else None

    node = graph_root.add_node(node_id=node_id, code=code)

    node_template['id'] = node.id
    node_template['input_port_names'] = node.input_vars
    node_template['out_port_names'] = node.output_vars

    emit('add_node', node_template)  # Create node in UI


def create_edge(graph_root, conn_data):

    source_id = conn_data['source_id']
    source_var = conn_data['source_var']
    target_id = conn_data['target_id']
    target_var = conn_data['target_var']

    graph_root.make_connection(source_id, source_var, target_id, target_var)

    emit('add_connection', conn_data)  # Create node in UI


def parse_xml(xml):

    doc = xmltodict.parse(xml)

    results_node = [c for c in doc['mxGraphModel']['root']['mxCell'] if '@results' in c]
    results = results_node[0]['@results'] if len(results_node) > 0 else None

    scopes_node = [c for c in doc['mxGraphModel']['root']['mxCell'] if '@scopes' in c]
    scopes = scopes_node[0]['@scopes'] if len(scopes_node) > 0 else None

    cells = dict((c_id, cell) for c_id, cell in [(c['@id'], c) for c in doc['mxGraphModel']['root']['mxCell']])
    nodes = [c for c in doc['mxGraphModel']['root']['mxCell'] if '@isNode' in c]
    edges = [c for c in doc['mxGraphModel']['root']['mxCell'] if '@edge' in c]

    return results, scopes, cells, nodes, edges


def generate_nodes(root, nodes):

    for node in nodes:

        node_id = node['@id']
        code = node['@code'] if '@code' in node else ''
        ui_code = node['@display_code'] if '@display_code' in node else ''
        ui_script = node['@display_act_code'] if '@display_act_code' in node else '{}'

        template = dict()

        template['id'] = node_id
        template['code'] = code
        template['display_code'] = ui_code
        template['display_act_code'] = ui_script

        template['x'] = float(node['mxGeometry']['@x'])
        template['y'] =  float(node['mxGeometry']['@y'])
        template['width'] = float(node['mxGeometry']['@width'])
        template['height'] = float(node['mxGeometry']['@height'])

        create_node(root, template)


def generate_edges(root, cells, edges):

    for edge in edges:
        conn_data = dict()

        port_source_id = edge['@source']
        port_target_id = edge['@target']

        conn_data['source_var'] = cells[port_source_id]['@value']
        conn_data['target_var'] = cells[port_target_id]['@value']

        conn_data['source_id'] = cells[port_source_id]['@parent']
        conn_data['target_id'] = cells[port_target_id]['@parent']

        create_edge(root, conn_data)
