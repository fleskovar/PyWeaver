<template>
	<div :key='this.redraw'>
		<v-runtime-template :template="template" :display_code="display_code"></v-runtime-template>   
	</div>
</template>

<script>
import VRuntimeTemplate from "../../custom_modules/v-runtime-template/index.js";
import {Val} from '../directives/InitDirective.js'
import BigDisplay from '../../src/components/BigDisplay.vue'
import SmallDisplay from '../../src/components/SmallDisplay.vue'

export default {
  components: {    
    VRuntimeTemplate,
    BigDisplay,
    SmallDisplay
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
      node_data: null, //stores inner state of the display
      redraw: 0, //used for forcing render update
      isBigDisplay: true, //used for selectively rendering components on big/small displays
    }
  },
  methods:{
    process_results: function(data){
      this.template = '<div>'+data['ui']+'</div>';
      this.display_code = data['script'];
      this.scope = data['scope'];
    },
    process_graph_update: function(data){
      this.node = data;
      this.updateRedrawKey(); //Force render to update (this.node_data is not reactive)
    },
    updateRedrawKey(){
      //Method for forcing rendering
      if(this.redraw>0)
          this.redraw = 0;
      else this.redraw=1;
        this.$forceUpdate();
    },
  },
  computed: {
    
    node: {
      // This variable stores the state of the node for rendering
      // It is used by the Proxy that is constructed in the mount() method.
      // Originally it gets the _node value and then gets updated by the socket.
      get: function(){
        if (this.node_data == null){
          this.node_data = this._node;
          
        }
        return this.node_data;
      },
      set: function(val){
        this.node_data = val;
      }
    },

  },

  mounted(){

    this.process_results(this.ui_data); //Load UI code into display

    //Should change _node with a new object that fetches data from the server
    //Should probably do the same with the UI
    this.node = new Proxy(this.node, {
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
      //Listen for graph execution broadcast message to get notified when new results are available
      this.$socket.emit('get_node_view_update', this.id, this.process_graph_update);
      
    }
  }
}
</script>

<style>
 
</style>

