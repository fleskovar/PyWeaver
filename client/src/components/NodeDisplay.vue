<template>
	<div>
		<v-runtime-template :template="template"></v-runtime-template>
	</div>
</template>

<script>
import VRuntimeTemplate from "v-runtime-template";
//import EventBus from '../EventBus.js'

export default {
  data: () => ({
    id: '',
    name: "Mellow",
    template: `<div>
      Hello {{ name }}!
      <v-btn>Test!</v-btn>
      </div>
    `
  }),
  components: {    
    VRuntimeTemplate,
  },
  methods:{
      changeCode(code){          
            this.template = code;          
      },
  },
  mounted(){
      //EventBus.$on('change_display', (data) => {this.changeCode(data)});
  }
};
</script>