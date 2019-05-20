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
    selected_node: {},
    open_code_editor: false,
    code: '',
    display_code: '',
    display_act_code: '',
    code_nodes: {},
    document_name: 'Untitled',
    node_displays: {},
    results: {}
  },
  mutations: {
    set_selected_node: function(state, node){      
      state.selected_node = node;
    },
    open_editor: function(state, val){
      state.open_code_editor = val;
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
    set_display_act_code: function(state, code){
      state.display_act_code = code;
    },
    set_document_name: function(state, name){
      state.document_name = name;
    }
  },
  actions: {
    open_code_editor: function(context, node){      
      context.commit('set_selected_node', node);
      context.commit('set_code', node.code);
      context.commit('set_display_code', node.display_code);
      context.commit('set_display_act_code', node.display_act_code);
      context.commit('open_editor', true);
    },
    add_empty_node: function(context){      
      let canvas = context.state.canvas;

      var node =  new CodeNode('Node', context.state.canvas, context);      
      var node_cell = canvas.addNode(node);
      var node_id = node_cell.id;

      //Insert component into node
      var ComponentClass = Vue.extend(NodeDisplay);
      var instance = new ComponentClass({
        propsData: {
          _node: node,
          store: context,          
        }
      });
      instance.$mount(); // pass nothing
      document.getElementById('node_'+node_id).appendChild(instance.$el);
      context.state.node_displays[node_cell.id] = instance;
      
      context.state.code_nodes[node_cell.id] = node;
      node.setCell(node_cell); 

      socket.emit('new_node', node_cell.id);        
    },
    socket_changeNodeInputPorts(context, port_names){      
      let canvas = context.state.canvas;
      //let cell = context.state.selected_node.cell;
      let cell_id = context.state.selected_node.cell.id;
      let cell = context.state.code_nodes[cell_id].cell;
      
      //TODO: check what happens with dirtyness
      //Reset port names in node
      context.state.code_nodes[cell_id].inputs = {}
      for(var i in port_names){
        context.state.code_nodes[cell_id].inputs[i] = null;
      }
      
      canvas.changePorts(cell, port_names, 0, 'input'); 
    },
    socket_changeNodeOutputPorts: function(context, port_names){      
      let canvas = context.state.canvas;
      //let cell = context.state.selected_node.cell
      let cell_id = context.state.selected_node.cell.id;
      let cell = context.state.code_nodes[cell_id].cell;

      //Reset port names in node
      context.state.code_nodes[cell_id].outputs = {}
      for(var i in port_names){
        context.state.code_nodes[cell_id].outputs[i] = null;
      }

      canvas.changePorts(cell, port_names, 1, 'output'); 
    },
    save_node_code: function(context, editor_data){
      context.state.selected_node.setCode(editor_data.code);
            
      var node_id = context.state.selected_node.id;
      context.state.node_displays[node_id].changeCode(editor_data.display_code);
      context.state.node_displays[node_id].changeAct(editor_data.display_act_code);
      context.state.selected_node.setDisplayCode(editor_data.display_code);
      context.state.selected_node.setDisplayActCode(editor_data.display_act_code);
      
      //This is sent to the server to update i/o connections and save code
      var data = {};
      data.code = editor_data.code;
      data.id = context.state.selected_node.cell.id;      
      socket.emit('edit_node_code', data);
      context.dispatch('execute_server');
    },
    add_connection(context, data){
      socket.emit('make_connection', data);

      //Makes a reference in the target node's input to the output of the source
      context.state.code_nodes[data.target_id].inputs[data.target_var] = {id: data.source_id, var_name: data.source_var};
      context.dispatch('execute_server');
    },
    remove_connection(context, data){
      socket.emit('delete_connection', data);
      context.dispatch('execute_server');
    },
    execute_server(context){

      //Compiles the scope data of each display and passes it to the serve
      var scope_data = {}
      let ds = context.state.node_displays;
      for(var key in ds){
        scope_data[key] = ds[key].scope;
      }

      socket.emit('execute', scope_data, (data) => {
        context.state.results = data;
        EventBus.$emit('update_displays');
      });
      //TODO: process outputs and put them into:
      //context.state.code_nodes[cell_id].inputs[i] = null;
    },
    delete_node(context, id){
      //TODO: Delete display component from context.state.node_displays
      socket.emit('delete_node', id);
    }
  }
})
