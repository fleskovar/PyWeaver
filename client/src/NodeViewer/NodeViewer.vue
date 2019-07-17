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
  data() {
    return {           
      id: 'n0',
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
    }
  },
  mounted(){
    //TODO parse this to get data from server
    var node_id = window.location.search
      .split('?')[1]
      .split('=')[1];

    this.id = node_id;

    this.node = new Proxy(this._node, {
        get: (target, name, receiver) => {  

          var return_val = null;

          if(name != '__ob__'){     
            //Ignore __ob__ request   
            var id = null;
            var var_name = null;
            if(name in target.inputs){
              console.log('input request');
              //The requested var is an input
              var source_data = target.inputs[name];
              //Fetch the data from the store using source's data
              if(source_data){
                id = source_data.id;
                var_name = source_data.var_name;
              }
            }
            else{
              //Fetch the data from the store using own data
              id = target.id;
              var_name = name;
            }

            if(id && var_name){
              if(id in target.store.state.results){
                if(var_name in target.store.state.results[id]){
                  return_val = target.store.state.results[id][var_name];
                }
              }
            }
          }

          return return_val;
      }
    });
  },
  sockets:{
    connect: function(){
      
      var node_id = window.location.search
      .split('?')[1]
      .split('=')[1];

      this.$socket.emit('get_node_view_data', {'node_id':node_id}, this.process_results);      
      
    },
    disconnect: function(){
      //this.connected = false;
    }
  },
}
</script>

<style>
 
</style>

