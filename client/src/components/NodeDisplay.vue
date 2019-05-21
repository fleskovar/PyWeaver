<template>
	<div :key='run_id'>
		<v-runtime-template :template="template" :display_code="display_code"></v-runtime-template>   
	</div>
</template>

<script>
import VRuntimeTemplate from "../../custom_modules/v-runtime-template/index.js";
import EventBus from '../EventBus.js'
import {Val} from '../directives/InitDirective.js'

//TODO: Change template init code and tie it to CodeNode default code
export default {
  props: [ '_node', 'store'],
  data: () => ({
    id: '',
    template: `<div>Node</div>`,
    display_code:'{}',
    scope: {},
    node: {},
  }),
  components: {    
    VRuntimeTemplate,
  },
  directives:{
    Val
  },
  methods:{
      changeCode(code){         
            //Safeguarding display code
            this.template ='<div>'+code+'</div>';          
      },
      changeAct(code){
        this.display_code = code
      },
      updateDisplay(){
        this.$forceUpdate();
        if(this.onResults){
          this.onResults();
        }
      }      
  },
  computed:{
    run_id: function(){
      return this.store.state.run_id;
    }
  },
  mounted(){

    //EventBus.$on('update_displays', (data) => {this.updateDisplay();});

    this.node = new Proxy(this._node, {
        get: (target, name, receiver) => {          
          var id = null;
          var var_name = null;
          if(name in target.inputs){
            console.log('input request');
            //The requested var is an input
            var source_data = target.inputs[name];
            //Fetch the data from the store using source's data
            id = source_data.id;
            var_name = source_data.var_name;
          }
          else{
            //Fetch the data from the store using own data
            id = target.id;
            var_name = name;
          }

          var return_val = null;
          
          if(id in target.store.state.results){
            if(var_name in target.store.state.results[id]){
              return_val = target.store.state.results[id][var_name];
            }
          }
          
          return return_val;
      }
    });
  }
};
</script>