<template>
	<div :key='run_id'>
    
    <div align="left" style='padding-left: 15px'>
      <div v-if="store.state.config.options_show_node_id">
        <br>
        ID: {{display_id}}
        <br>
      </div>
    </div>
    
		<v-runtime-template :template="template" :display_code="display_code"></v-runtime-template>   
	</div>
</template>

<script>
import VRuntimeTemplate from "../../custom_modules/v-runtime-template/index.js";
import EventBus from '../EventBus.js'
import {Val} from '../directives/InitDirective.js'
import BigDisplay from '../../src/components/BigDisplay.vue'
import SmallDisplay from '../../src/components/SmallDisplay.vue'


//TODO: Change template init code and tie it to CodeNode default code
export default {
  props: [ '_node', 'store'],
  data: () => ({
    display_id: '',
    id: '',
    template: `<div>Node</div>`,
    display_code:'{}',
    scope: {},
    node: {},
    _previous_template: '',
    _previous_display_code: '{}',
    isBigDisplay: false, //used for selectively rendering components on big/small displays
  }),
  components: {    
    VRuntimeTemplate,
    BigDisplay,
    SmallDisplay,
  },
  directives:{
    Val
  },
  methods:{
      setID(id){
        this.id = id;        
      },
      setDisplayID(id){
        this.display_id = id;        
      },
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

          var return_val = null;

          if(name != '__ob__'){     
            //Ignore __ob__ request   
            var id = null;
            var var_name = null;
            if(name in target.inputs){
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
  }
};
</script>