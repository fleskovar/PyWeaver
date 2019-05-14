import Vue from 'vue'
import Vuex from 'vuex'

import CodeNode from './NodeEditor/CodeNode';
import socket from './socket.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    canvas: {},
    selected_node: {},
    open_code_editor: false,
    code: '',
    code_nodes: {}
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
    }
  },
  actions: {
    open_code_editor: function(context, node){      
      context.commit('set_selected_node', node);
      context.commit('set_code', node.code);
      context.commit('open_editor', true);
    },
    add_empty_node: function(context){      
      let canvas = context.state.canvas;
      var node =  new CodeNode();
      var node_cell = canvas.addNode(node);
      context.state.code_nodes[node_cell.id] = node;
      node.setCell(node_cell); 

      socket.emit('new_node', node_cell.id);        
    },
    socket_changeNodeInputPorts(context, port_names){      
      let canvas = context.state.canvas;
      //let cell = context.state.selected_node.cell;
      let cell_id = context.state.selected_node.cell.id;
      let cell = context.state.code_nodes[cell_id].cell;
      canvas.changePorts(cell, port_names, 0, 'input'); 
    },
    socket_changeNodeOutputPorts: function(context, port_names){      
      let canvas = context.state.canvas;
      //let cell = context.state.selected_node.cell
      let cell_id = context.state.selected_node.cell.id;
      let cell = context.state.code_nodes[cell_id].cell;
      canvas.changePorts(cell, port_names, 1, 'output'); 
    },
    save_node_code: function(context, code){
      context.state.selected_node.code = code;
      var data = {};
      data.code = code;
      data.id = context.state.selected_node.cell.id;      
      socket.emit('edit_node_code', data);
    },
    add_connection(context, data){
      socket.emit('make_connection', data);
    },
    remove_connection(context, data){
      socket.emit('delete_connection', data);
    },
    execute_server(context){
      socket.emit('execute');
    },
    delete_node(context, id){
      socket.emit('delete_node', id);
    }
  }
})
