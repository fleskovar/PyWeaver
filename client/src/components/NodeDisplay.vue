<template>
	<div>
		<v-runtime-template :template="template" :display_code="display_code"></v-runtime-template>    
	</div>
</template>

<script>
import VRuntimeTemplate from "../../custom_modules/v-runtime-template/index.js";
//import EventBus from '../EventBus.js'

//TODO: Change template init code and tie it to CodeNode default code
export default {
  props: [ 'node' ],
  data: () => ({
    id: '',
    name: "Mellow",
    template: `<div>
      Hello {{ name }}!
      <v-btn>Test!</v-btn>
      </div>
    `,
    display_code:'{}',
    scope: {}
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
  },
  mounted(){
      //EventBus.$on('change_display', (data) => {this.changeCode(data)});
  }
};
</script>