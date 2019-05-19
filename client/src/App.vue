<template>
  <v-app>
    <v-toolbar app dark fixed clipped-left>
      <v-toolbar-title class="headline text-uppercase">
        <span>Py</span>
        <span class="font-weight-light">Weaver</span>
        <span>2</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      
      <v-toolbar-items>
        <v-btn flat small v-on:click='OpenFile'>          
          <span>Open file</span>
          <v-icon>folder_open</v-icon>
        </v-btn>
        
        <v-btn flat small v-on:click='SaveModel'>
          <span>Save model</span>
          <v-icon>cloud_download</v-icon>
        </v-btn>
      </v-toolbar-items>
        
      <v-chip color="green" text-color="white" v-if='connected'>Connected</v-chip>  
      <v-chip color="red" text-color="white" v-if='!connected'>Disconnected</v-chip> 
       
    </v-toolbar>
    <input type='file' id='fileInput' v-on:change='OpenModel($event)' hidden>

    <v-navigation-drawer permanent clipped dark app width='300' :mini-variant="drawer_mini">  
      
      <v-list>
        <v-list-tile>          
          <v-list-tile-content></v-list-tile-content>
          <v-list-tile-action @click="toggleMiniDrawer">
            <v-btn icon>
              <v-icon v-if="drawer_mini">keyboard_arrow_right</v-icon>
              <v-icon v-if="!drawer_mini">keyboard_arrow_left</v-icon>
            </v-btn>
          </v-list-tile-action>        
        </v-list-tile>        
        
        <v-list-tile>
          <v-list-tile-content>
            <br>
            <br>
            <v-text-field label="Document name" v-model='document_name'/>
            <br>
          </v-list-tile-content>
        </v-list-tile>

        <v-divider/>

        <v-list-tile @click="addNode" @keydown.shift.enter="canvasShortcuts">
          <v-list-tile-action>
            <v-btn icon class="text-lg-right">              
              <v-icon>add</v-icon>
            </v-btn>
          </v-list-tile-action>   
          <v-list-tile-content>ADD NEW NODE</v-list-tile-content>     
        </v-list-tile>

        <v-list-tile @click="runServer">
          <v-list-tile-action>
            <v-btn icon class="text-lg-right">              
              <v-icon>computer</v-icon>
            </v-btn>
          </v-list-tile-action>   
          <v-list-tile-content>RUN</v-list-tile-content>     
        </v-list-tile>

        <v-divider/>

        <v-list-tile>
          <v-list-tile-action>
            <v-btn icon class="text-lg-right">              
              <v-icon>settings</v-icon>
            </v-btn>
          </v-list-tile-action>   
          <v-list-tile-content>SETTINGS</v-list-tile-content>     
        </v-list-tile>

      </v-list>
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
            <v-tabs dark>
              <v-tab>Code</v-tab>
              <v-tab-item>
                <codemirror :options="cmOptions" ref="code_editor" v-model="code"/>
              </v-tab-item>

              <v-tab>Display</v-tab>
              <v-tab-item>                
                <codemirror :options="dispCmOptions" ref="code_editor" v-model="display_code"/>                
              </v-tab-item>

              <v-tab>Display Actions</v-tab>
              <v-tab-item>                
                <codemirror :options="dispActCmOptions" ref="code_editor" v-model="display_act_code"/>                
              </v-tab-item>

            </v-tabs>
             
          </v-card-text>
            <v-card-actions>              
              <v-btn color="green" flat v-on:click='saveCode' dark>Save</v-btn>                          
            </v-card-actions>
        </v-card>              
      </v-dialog>


    <v-footer class="pa-3" app dark>
      <v-btn color="gray" dark v-on:click="openEditor">Edit</v-btn>
      <v-btn color="gray" dark v-on:click="plotTest">Plot</v-btn>
      <v-btn color="gray" dark v-on:click="compileTest">Compile</v-btn>
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
import 'codemirror/mode/htmlmixed/htmlmixed.js'
import 'codemirror/mode/javascript/javascript.js'

import Canvas from './NodeEditor/Canvas';
import CodeNode from './NodeEditor/CodeNode';

import Plotly from 'plotly.js-dist';

import {
  DISPLAY_NODE_ID_ATTR,
  DISPLAY_VAR_ATTR,
  DISPLAY_VAR_NAME_ATTR,
  DISPLAY_CLASS
} from './Constants.js';


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
        autoRefresh: true,        
      },
      dispCmOptions: {
        // codemirror options
        tabSize: 4,
        indentUnit: 4,
        mode: 'htmlmixed',        
        lineNumbers: true,        
        indentWithTabs: true,
        viewportMargin: Infinity,
        line: true,
        theme: 'base16-dark',
        autoRefresh: true,        
      },
      dispActCmOptions: {
        // codemirror options
        tabSize: 4,
        indentUnit: 4,
        mode: 'javascript',        
        lineNumbers: true,        
        indentWithTabs: true,
        viewportMargin: Infinity,
        line: true,
        theme: 'base16-dark',
        autoRefresh: true,        
      },
      drawer_mini: true      
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
      this.$store.dispatch('save_node_code',
       {
        code: this.code,
        display_code: this.display_code,
        display_act_code: this.display_act_code
        }
      );      
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
    },
    OpenFile: function(){
      var file_obj = document.getElementById('fileInput');
      file_obj.click();
    },
    OpenModel: function(ev){
        console.log('tried open');
        const file = ev.target.files[0];
        if (!file) {
          return;
        }
        var reader = new FileReader();
        reader.onload = (e) => {
          var contents = e.target.result;
          // Display file content
          this.$store.state.canvas.LoadModel(contents);
        };
        reader.readAsText(file);
      },
      SaveModel: function(){
        var xmlString = this.$store.state.canvas.GetModelXML();
        
        /*
        mxUtils.post(url, 'xml='+xmlString, function(req)
        {
            // Process server response using req of type mxXmlRequest
        });
        */
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(xmlString));
        
        var file_name = this.$store.state.document_name + ".xml";
        
        element.setAttribute('download', file_name);

        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
      },
      toggleMiniDrawer: function(){
        this.drawer_mini = !this.drawer_mini;
      },
      plotTest: function(){
        var trace1 = {
          x: [1, 2, 3, 4],
          y: [0, 2, 3, 5],
          fill: 'tozeroy',
          type: 'scatter'
        };
        var trace2 = {
          x: [1, 2, 3, 4],
          y: [3, 5, 1, 3],
          fill: 'tonexty',
          type: 'scatter'
        };
        var data = [trace1, trace2];

        Plotly.newPlot('myDiv', data, {}, {scrollZoom: true});
      },
      compileTest: function(){
        //TODO: Access scope of v-runtime-template
        //TODO: On code change, reinit scope of v-runtime-template     
        var data = {}
        let ds = this.$store.state.node_displays;
        for(var key in ds){
          data[key] = ds[key].scope;
        }
        console.log(data);
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
        this.$store.commit('set_code', val);
      }      
    },
    display_code:{
      get: function(){return this.$store.state.display_code},      
      set: function(val)
      {
        this.$store.commit('set_display_code', val)
      }      
    },
    display_act_code:{
      get: function(){return this.$store.state.display_act_code},      
      set: function(val)
      {
        this.$store.commit('set_display_act_code', val)
      }      
    },
    connected: function(){
      return this.$socket.connected;
    },
    document_name:{
      get: function(){
        return this.$store.state.document_name;
      },
      set:function(val){
        this.$store.commit('set_document_name', val);
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

