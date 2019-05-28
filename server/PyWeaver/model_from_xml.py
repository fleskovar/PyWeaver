import xmltodict

def parse_xml(xml):

    doc = xmltodict.parse(xml)

    cells = dict((c_id, cell) for c_id, cell in [(c['@id'], c) for c in doc['mxGraphModel']['root']['mxCell']])
    nodes = [c for c in doc['mxGraphModel']['root']['mxCell'] if '@isNode' in c]
    edges = [c for c in doc['mxGraphModel']['root']['mxCell'] if '@edge' in c]

    return cells, nodes, edges



def generate_nodes(root, emit, cells, nodes):

    for node in nodes:

        code = node['@code'] if '@code' in node else None
        ui_code = node['@display_code'] if '@display_code' in node else None
        ui_script = node['@display_act_code'] if '@display_act_code' in node else None

        # TODO: Spawn every node
        # TODO: Process geometry data and pass it to the UI


def generate_edges(root, emit, cells, edges):

    for edge in edges:

        port_source_id = edge['@source']
        port_target_id = edge['@target']

        source_var = cells[port_source_id]['@value']
        target_var = cells[port_target_id]['@value']

        source_id = cells[port_source_id]['@parent']
        target_id = cells[port_target_id]['@parent']

        #TODO: Create every connection