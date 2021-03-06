import Vue from 'vue'
import Vuex from 'vuex'

import CodeNode from './NodeEditor/CodeNode';
import socket from './socket.js'

import NodeDisplay from './components/NodeDisplay.vue'
import EventBus from './EventBus.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    canvas: {},
    selected_node: {}, //Cell/Node we double-clicked and is being edited
    open_code_editor: false,
    code: '',
    display_code: '',
    display_act_code: '',
    code_nodes: {},
    document_name: 'Untitled',
    node_displays: {},
    results: {},
    config:{
      auto_exec: true,
      sync_model: true,
      dark_mode: false,
      options_show_node_id: false,
    },    
    run_id: 0,
    libraryTree: [],
    save_dialog: false,
    session_id: null,
    code_error_dict: {},
    code_parse_error_list: [],
    calcs_list: [],
    show_refactor_func_dialog: false,
    refactor_func_options: [],
    refactor_node_id: '',
    canvas_views: {},
    copied_cell_id: '',
    console_text: 'PyWeaver Console \n',
    connection_inspector_connections: [],   
    connection_inspector_id: {},  
    explorer_menu_open: true,
    explorer_menu_tab: null,
  },
  mutations: {
    set_connection_inspector_id: function(state, data){
      state.connection_inspector_id = data;
    },
    set_explorer_menu_open: function(state, val){
      state.explorer_menu_open = val;
    },
    set_explorer_menu_tab: function(state, tab_name){
      state.explorer_menu_tab = tab_name;
    },
    set_refactor_node_id: function(state, id){
      state.refactor_node_id = id;
    },
    set_copied_cell_id: function(state, id){
      state.copied_cell_id = id;
    },
    set_refactor_func_options: function(state, val){
      state.refactor_func_options = val;
    },
    calc_list_change: function(state, calcs){
      state.calcs_list = calcs;
    },
    add_code_error: function(state, e){
      state.code_error_dict[e.id] = {line: e.line, type: e.error_tyoe, error: e.error};
    },
    clear_code_error_list: function(state){
      state.code_error_dict = {};
    },
    set_dark_mode: function(state, val){
      state.config.dark_mode = val;
    },
    set_auto_exec: function(state, val){
      state.config.auto_exec = val;
    },
    set_sync_model: function(state, val){
      state.config.sync_model = val;
    },
    set_node_id_display: function(state, val){
      state.config.options_show_node_id = val;
    },
    tree_change: function(state, libraryTree){
      state.libraryTree = libraryTree;
    },
    set_selected_node: function(state, node){      
      state.selected_node = node;
    },
    open_editor: function(state, val){
      //bugHighlight
      state.open_code_editor = val;
    },
    set_dialog_open: function(state, val){
      state.save_dialog = val;
    },
    set_canvas: function(state, canvas){
      state.canvas = canvas;
    },
    set_code: function(state, code){
      state.code = code;
    },
    set_display_code: function(state, code){
      state.display_code = code;
    },
    set_show_refactor_func_dialog: function(state, val){
      state.show_refactor_func_dialog = val;
    },
    set_display_act_code: function(state, code){
      state.display_act_code = code;
    },
    set_document_name: function(state, name){
      state.document_name = name;
    },
    set_session_id: function(state, session_id){
      state.session_id = session_id;
    },
    set_connection_inspector_connections: function(state, var_list){
      state.connection_inspector_connections = var_list;
    }
  },
  actions: {

    sort_connection: function(context, sort_data){
      socket.emit('sort_connection_data', sort_data, 
        (data) => {
          var var_data = context.state.connection_inspector_id;
          context.dispatch('get_connection_data', var_data);
        });
    },

    get_connection_data: function(context, var_data){

      context.commit('set_connection_inspector_id', var_data);

      socket.emit('get_input_connection_data', var_data,
        (data) => {
          context.commit('set_connection_inspector_connections', data);
          context.commit('set_explorer_menu_open', false); //Open left side panel
          context.commit('set_explorer_menu_tab', 1) //Navigate to explorer tab
        }      
      );
    },

    execute_console: function(context, code){
      socket.emit('execute_console', code);
      context.dispatch('socket_printToConsole', '>>'+code+'\n');
    },
    socket_printToConsole: function(context, text){
      this.state.console_text += text;
    },
    update_all_cells: function(context){
      
      let graph = context.state.canvas.graph;

      for(var node_id in context.state.code_nodes){
        var cell = context.state.code_nodes[node_id].cell;
        graph.updateCellSize(cell, true);
      }           
    },
    push_server_model: function(context){
      
      if(context.state.config.sync_model){
        context.dispatch('sync_model_with_server');
      }
    },
    sync_model_with_server: function(context){
      var model_data = {};
      model_data.session_id = context.state.session_id;
      model_data.xml = context.state.canvas.GetModelXML();    

      socket.emit('sync_model', model_data);
    },
    open_code_editor: function(context, node){      
      context.commit('set_selected_node', node);
      context.commit('set_code', node.code);
      context.commit('set_display_code', node.display_code);
      context.commit('set_display_act_code', node.display_act_code);
      context.commit('open_editor', true);
    },    
    attach_nodes: function(context){
      
      for(let node_id in context.state.node_displays){
        let instance = context.state.node_displays[node_id];
        let div_el = document.getElementById('node_'+node_id);
        if(div_el)
          div_el.appendChild(instance.$el); //Insert display into DOM
      }
    },
    socket_addNode: function(context, node_data){
      //TODO:      
      //set selected_node and others

      let canvas = context.state.canvas;      
      
      var id = node_data['id'];

      var node =  new CodeNode('Node', context.state.canvas, context, id);
      node.inputs = node_data['input_port_names']
      node.outputs = node_data['out_port_names']

      //If geometry data is available, use it
      if(node_data['x'] && node_data['y'] && node_data['width'] && node_data['height']){
        node.x = node_data['x'];
        node.y = node_data['y'];
        node.width = node_data['width'];
        node.height = node_data['height'];
      }

      var node_cell = canvas.addNode(node);
      var node_id = node_cell.id;
      console.log("new id: "+node_id);

      //Insert component into node
      var ComponentClass = Vue.extend(NodeDisplay);
      var instance = new ComponentClass({
        propsData: {
          _node: node,
          store: context,          
        }
      });
      
      node.setCell(node_cell); //Save reference in CodeNode object to the mxgraph cell object

      node.setCode(node_data.code);

      instance.changeCode(node_data.display_code);
      node.setDisplayCode(node_data.display_code);

      instance.changeAct(node_data.display_act_code);
      node.setDisplayActCode(node_data.display_act_code);

      instance.setID(node_id);
      instance.setDisplayID(node_id);

      instance.$mount(); // pass nothing
      document.getElementById('node_'+node_id).appendChild(instance.$el); //Insert display into DOM
      
      //Check if needed
      //instance.updateDisplay();
      //EventBus.$emit('update_displays');      
      
      context.state.node_displays[node_cell.id] = instance; //Save reference to display. Unify with below?      
      context.state.code_nodes[node_cell.id] = node; //Save reference to the CodeNode object

      //Once everything is rendered, update the cell
      Vue.nextTick()
        .then( () => {
          canvas.updateCellSize(node_cell);
        });       
      
      //context.commit('set_selected_node', node); //This is required by the 'save_node_code' action
      //socket.emit('new_node', node_cell.id); //This could be combined with the line below
      //context.dispatch('save_node_code', node_data) //Change the code.
    },
    socket_syncSession: function(context, session_id){
      if(context.state.session_id != session_id){
        context.commit('set_session_id', session_id);
        socket.emit('request_model');
      }
    },
    socket_setNodeClientCode: function(context, server_data){
      var node_id = server_data['node_id'];
      var code = server_data['code'];
      context.state.code_nodes[node_id].code = code;
    },
    socket_setNodeClientUi: function(context, server_data){},
    socket_setNodeClientUiScript: function(context, server_data){},
    socket_forceSessionId: function(context, session_id){      
        context.commit('set_session_id', session_id);      
    },
    socket_addError: function(context, error_data){      
         context.commit('add_code_error', error_data);   
    },
    socket_addConnection: function(context, conn_data){
      context.state.canvas.addEdge(conn_data);
      context.state.code_nodes[conn_data.target_id].inputs[conn_data.target_var] = {id: conn_data.source_id, var_name: conn_data.source_var};
    },
    socket_setLibraryTree(context, data){
      context.commit('tree_change', data.tree);
      context.commit('calc_list_change', data.calcs);      
    },
    socket_changeNodeInputPorts(context, port_names){      
      let canvas = context.state.canvas;
      //let cell = context.state.selected_node.cell;
      let cell_id = context.state.selected_node.cell.id;
      let cell = context.state.code_nodes[cell_id].cell;
      
      //TODO: check what happens with dirtyness
      //Reset port names in node

      //TODO: this is killing input connections
      context.state.code_nodes[cell_id].inputs = {}
      for(var i in port_names){
        context.state.code_nodes[cell_id].inputs[port_names[i]] = null;        
      }
      
      canvas.changePorts(cell, port_names, 0, 'input');
    },
    socket_changeNodeOutputPorts: function(context, port_names){      
      let canvas = context.state.canvas;
      //let cell = context.state.selected_node.cell
      let cell_id = context.state.selected_node.cell.id;
      let cell = context.state.code_nodes[cell_id].cell;

      //Reset port names in node
      //TODO: this is killing output connections
      //Server should send "delete connection"
      context.state.code_nodes[cell_id].outputs = {}
      for(var i in port_names){
        context.state.code_nodes[cell_id].outputs[port_names[i]] = null;        
      }

      canvas.changePorts(cell, port_names, 1, 'output');
    },
    save_node_code: function(context, editor_data){
      context.state.selected_node.setCode(editor_data.code);
            
      var node_id = context.state.selected_node.id;
      context.state.node_displays[node_id].changeCode(editor_data.display_code);
      context.state.selected_node.setDisplayCode(editor_data.display_code);

      context.state.node_displays[node_id].changeAct(editor_data.display_act_code);
      context.state.selected_node.setDisplayActCode(editor_data.display_act_code);     
      
      context.state.node_displays[node_id].updateDisplay();
      EventBus.$emit('update_displays');

      Vue.nextTick()
        .then( () => {
          var data = {};
          data.code = editor_data.code;
          data.ui_code = editor_data.display_code;
          data.ui_script = editor_data.display_act_code;
          data.id = context.state.selected_node.cell.id;      
          socket.emit('edit_node_code', data);
          context.dispatch('auto_execute');
        });

      //This is sent to the server to update i/o connections and save code
      
    },
    paste_cell(context){
      var node_id = context.state.copied_cell_id;

      var node_data = {};

      node_data.code = context.state.code_nodes[node_id].code;
      node_data.display_code = context.state.code_nodes[node_id].display_code;
      node_data.display_act_code = context.state.code_nodes[node_id].display_act_code;

      socket.emit('new_node_from_code', node_data);

    },
    add_connection(context, data){
      socket.emit('make_connection', data);

      //Makes a reference in the target node's input to the output of the source
      context.state.code_nodes[data.target_id].inputs[data.target_var] = {id: data.source_id, var_name: data.source_var};
      context.dispatch('auto_execute');
    },
    remove_connection(context, data){
      socket.emit('delete_connection', data);
      context.dispatch('auto_execute');
    },
    rename_connection(context, data){
      socket.emit('rename_connection', data);
      context.dispatch('auto_execute');
    },
    set_output_type(context, data){
      socket.emit('set_output_type', data);
    },
    open_refactor_dialog(context, node_id){
      context.commit('set_refactor_node_id', node_id);

      //Extract the name of the input variables so that the user can decide
      //which of them should be paramters and which should be inner inputs
      //var keys = Object.keys(context.state.code_nodes[node_id].inputs);
      var keys = context.state.code_nodes[node_id].inputs;
      context.commit('set_refactor_func_options', keys);
      context.commit('set_show_refactor_func_dialog', true);
    },
    refactor_to_function(context, refactor_data){

      var server_data = {};
      var node_id = refactor_data['node_id']
      server_data['id'] = node_id;
      server_data['code'] = context.state.code_nodes[node_id].code;
      server_data['ui_code'] = context.state.code_nodes[node_id].display_code;
      server_data['ui_script'] = context.state.code_nodes[node_id].display_act_code;
      server_data['inner_vars'] = refactor_data['inner_vars'];

      socket.emit('refactor_to_function', server_data);
    },
    execute_server(context){

      //Compiles the scope data of each display and passes it to the serve
      context.commit('clear_code_error_list');
      var scope_data = {}
      let ds = context.state.node_displays;
      for(var key in ds){
        scope_data[key] = ds[key].scope;
      }

      socket.emit('execute', scope_data, (data) => {        
        context.state.results = data;
        context.state.run_id += 1;
        context.state.canvas.addResults(data);

        var scopes = {}
        for(var node in context.state.node_displays){
          let node_display = context.state.node_displays[node];
          scopes[node] = node_display.scope;
        }

        context.state.canvas.addScopes(scopes);
        EventBus.$emit('update_displays');
        context.dispatch('update_all_cells');
      });
    },  
    socket_setResults(context, data){
      data = JSON.parse(data);
      context.state.results = data;
      context.state.run_id += 1;
      context.state.canvas.addResults(data);      
      EventBus.$emit('update_displays');
    },
    socket_setScopes(context, scopes){
      scopes = JSON.parse(scopes);
      for(var node in context.state.node_displays){
        let node_display = context.state.node_displays[node];
        for(var var_name in node_display.scope){
          if(var_name != '__ob__' && var_name != '__proto__')
            node_display.scope[var_name] = scopes[node][var_name];
        }        
      }      
      context.state.run_id += 1;
      context.state.canvas.addScopes(scopes);
      EventBus.$emit('update_displays');
    },
    auto_execute(context){
      if(context.state.config.auto_exec){
        context.dispatch('execute_server');
      }
    },
    delete_node(context, id){
      //TODO: make sure this does not lead to a memory leak
      socket.emit('delete_node', id);

      //Locally remove display and code node
      context.state.node_displays[id].$destroy();
      delete context.state.node_displays[id];
      delete context.state.code_nodes[id];
    },
    change_element_color(context, color){      
      context.state.canvas.setCellColor(color);
    },
    change_element_stroke_size(context, size){
      context.state.canvas.setCellStroke(size);
    },
    change_element_dashed(context, is_dashed){
      context.state.canvas.setSelectionDashed(is_dashed);
    },
    change_dark_mode(context, val){
      context.commit('set_dark_mode', val);
      context.state.canvas.updateSyles();
    },
    save_config_file(context){
      socket.emit('save_config_file', JSON.stringify(context.state.config));
    },
    socket_setNodeOverlay(context, overlay_data){
      var node_id = overlay_data['node_id'];
      var overlay_type = overlay_data['overlay_type'];
      var cell = context.state.code_nodes[node_id].cell;
      context.state.canvas.removeOverlay(cell);
      context.state.canvas.setOverlay(cell, overlay_type);
    }

  },
})
