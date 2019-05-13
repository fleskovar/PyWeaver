<template>
  <v-app>
    <v-toolbar app dark>
      <v-toolbar-title class="headline text-uppercase">
        <span>Py</span>
        <span class="font-weight-light">Weaver</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>      
    </v-toolbar>

    <v-navigation-drawer clipped dark app width='300'>
      Options!
    </v-navigation-drawer>

    <v-content app> 
        <v-card height='100%'>
          <div id='canvas' style='width:100%; height:100%'/>       
        </v-card>
    </v-content>

      <v-dialog v-model="code_dialog" width="800" persistent @keydown="codeDialogShortcuts">
          <v-card>      
            <v-toolbar dark color="gray">              
              <v-toolbar-title>Editor</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-toolbar-items>
                <v-btn icon dark @click="closeDialog">
                  <v-icon>close</v-icon>
                </v-btn>
              </v-toolbar-items>
            </v-toolbar>

          <v-card-text>    
            <v-flex xs12 sm6 md3>
              <v-text-field label="Node name"/>
            </v-flex>
            <codemirror :options="cmOptions" ref="code_editor" v-model="code"/> 
          </v-card-text>
            <v-card-actions>              
              <v-btn color="green" flat v-on:click='saveCode' dark>Save</v-btn>                          
            </v-card-actions>
        </v-card>              
      </v-dialog>


    <v-footer class="pa-3" app dark>
      <v-btn color="gray" dark v-on:click="openEditor">Edit</v-btn>   
      <v-btn color="gray" dark v-on:click="addNode" @keydown.shift.enter="canvasShortcuts">Add</v-btn>   
      <v-btn color="gray" dark v-on:click="runServer">Run</v-btn>   
     
      <v-spacer></v-spacer>
        <div>&copy; {{ new Date().getFullYear() }}</div>
    </v-footer>

  </v-app>
</template>

<script>
import EventBus from './EventBus.js'
import { codemirror } from 'vue-codemirror'

// require styles
import 'codemirror/lib/codemirror.css'
import 'codemirror/mode/python/python.js'
import 'codemirror/theme/base16-dark.css'

import Canvas from './NodeEditor/Canvas';
import CodeNode from './NodeEditor/CodeNode';

export default {
  name: 'App',
  components: {
    codemirror,    
  },
  data () {
    return {
      cmOptions: {
        // codemirror options
        tabSize: 4,
        indentUnit: 4,
        mode: 'python',        
        lineNumbers: true,        
        indentWithTabs: true,
        viewportMargin: Infinity,
        line: true,
        theme: 'base16-dark',
        autoRefresh: true
      }      
    }
  },  
  mounted(){
    var container = document.getElementById('canvas');
    var canvas = new Canvas(container, this.$store);
    canvas.mount();
    this.$store.commit('set_canvas', canvas);
    },

  methods:{
    closeDialog: function(){
      this.code_dialog = false;
    },
    saveCode: function(){      
      this.$store.dispatch('save_node_code', this.code);
      this.closeDialog();
    },
    openEditor: function(){
      this.code_dialog = true;
    },
    addNode: function(){      
      this.$store.dispatch('add_empty_node');     
    },
    codeDialogShortcuts: function(e){
      if (e.keyCode === 13 && e.shiftKey){
        
        this.saveCode();
      }else if(e.keyCode === 27){
        
        this.closeDialog();
      }
    },
    canvasShortcuts: function(e){  
      if (e.keyCode === 13 && e.shiftKey){        
        this.addNode();        
      }
    },
    runServer: function(){
      this.$store.dispatch('execute_server');
    }
  },
  computed:{
    code_dialog:{
      get: function(){return this.$store.state.open_code_editor},
      
      set: function(val)
      {
        this.$store.commit('open_editor', val)
      }      
    },
    code:{
      get: function(){return this.$store.state.code},
      
      set: function(val)
      {
        this.$store.commit('set_code', val)
      }      
    }
  },
  watch:{
    code_dialog: function(new_val, old_val){
      if(new_val){        
        return setTimeout(() => {
        this.$refs.code_editor.codemirror.refresh()
        this.$refs.code_editor.codemirror.focus();
        }, 200);        
      }
    }
  }
}
</script>

<style>
  .canvas{
    height: 100vh;
    width: 100vw;
    overflow: hidden;
  }

  html{
    overflow: hidden;
  }
</style>

