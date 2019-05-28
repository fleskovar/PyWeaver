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

    <SideBar/>

    <v-content app> 
        <v-card height='100%'>
          <div id='canvas' style='width:100%; height:100%'/>       
        </v-card>
    </v-content>

    <CodeEditor/>
    <LibrarySaveDialog/>

    <v-footer class="pa-3" app dark>
      <v-btn color="gray" dark v-on:click="resetServer">Reset</v-btn>
      <v-spacer></v-spacer>
        <div>&copy; {{ new Date().getFullYear() }}</div>
    </v-footer>

  </v-app>
</template>

<script>
import Canvas from './NodeEditor/Canvas';
import CodeEditor from './components/CodeEditor'
import SideBar from './components/SideBar'
import LibrarySaveDialog from './components/LibrarySaveDialog'
import EventBus from './EventBus.js'

export default {
  name: 'App',
  components: {
    CodeEditor,
    SideBar,
    LibrarySaveDialog 
  },
  data () {
    return {           
      connected: false,      
    }
  },  
  mounted(){   
    var container = document.getElementById('canvas');    
    var canvas = new Canvas(container, this.$store);
    canvas.mount();
    this.$store.commit('set_canvas', canvas);
    EventBus.$on('update_displays', this.updateCanvas);
    },

  methods:{
    OpenFile: function(){
      var file_obj = document.getElementById('fileInput');
      file_obj.click();
    },
    OpenModel: function(ev){
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
      resetServer: function(){
        //Resets server
        this.$socket.emit('reset');
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
      updateCanvas(){
        this.$store.dispatch('update_all_cells');
      }
  },
  computed:{           
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
  },
  sockets:{
    connect: function(){
      this.connected = true;      
    },
    disconnect: function(){
      this.connected = false;
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

