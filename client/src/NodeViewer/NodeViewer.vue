<template>
	<div>
		<v-runtime-template :template="template" :display_code="display_code"></v-runtime-template>   
	</div>
</template>

<script>
import VRuntimeTemplate from "../../custom_modules/v-runtime-template/index.js";
import {Val} from '../directives/InitDirective.js'

export default {
  components: {    
    VRuntimeTemplate,
  },
  directives:{
    Val,
  },
  name: 'NodeViewer',
  props: ['id', 'ui_data', '_node'],
  data() {
    return {
      template: '',
      script: '',
      scope: {},
      _previous_template: '',
      _previous_display_code: '{}',
      node: {},
    }
  },
  methods:{
    process_results: function(data){
      this.template = '<div>'+data['ui']+'</div>';
      this.display_code = data['script'];
      this.scope = data['scope'];
    },
    process_graph_update: function(data){
      //this.ui_data = response.data.ui_data;

      //TODO: Avoid mutating a prop directly. Make sure state of the server is synched with display
      this._node = data;
    }
  },
  mounted(){

    this.process_results(this.ui_data);

    //Should change _node with a new object that fetches data from the server
    //Should probably do the same with the UI
    this.node = new Proxy(this._node, {
        get: (target, name, receiver) => {  

          //TODO: should rebuild "target" as an object containing the i/o from the node, obtained from the server

          var return_val = null;

          if(name != '__ob__'){     
            //Ignore __ob__ request   
            var id = null;
            var var_name = null;
            if(name in target){
              //The requested var is inside the node
              return_val = target[name];
              
            }
          }
          return return_val;
      }
    });
  },
  sockets: {
    graphExecuted(val){
      this.$socket.emit('get_node_view_update', this.id, this.process_graph_update);
      
    }
  }
}
</script>

<style>
 
</style>

