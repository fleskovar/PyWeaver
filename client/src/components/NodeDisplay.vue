<template>
	<div>
		<v-runtime-template :template="template" :display_code="display_code"></v-runtime-template>   
	</div>
</template>

<script>
import VRuntimeTemplate from "../../custom_modules/v-runtime-template/index.js";
import EventBus from '../EventBus.js'

//TODO: Change template init code and tie it to CodeNode default code
export default {
  props: [ '_node', 'store'],
  data: () => ({
    id: '',
    name: "Mellow",
    template: `<div>
      Hello {{ name }}!
      <v-btn>Test!</v-btn>
      </div>
    `,
    display_code:'{}',
    scope: {},
    node: {},
  }),
  components: {    
    VRuntimeTemplate,
  },
  methods:{
      changeCode(code){          
            this.template = code;          
      },
      changeAct(code){
        this.display_code = code
      },
      updateDisplay(){
        this.$forceUpdate();
      }      
  },
  mounted(){

    EventBus.$on('update_displays', (data) => {this.updateDisplay();});

    this.node = new Proxy(this._node, {
        get: (target, name, receiver) => {          
          var id = null;
          var var_name = null;
          if(name in target.inputs){
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