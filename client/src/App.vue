<template>
  <v-app>
    <v-toolbar app dark fixed clipped-left flat>
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

    <v-content style='overflow: hidden'>
        <v-toolbar dark class="grey darken-2" dense>          
                      
          Ouline        
          <v-item-group>
              <v-btn flat icon @click='SetDashed(false)'>
                <v-icon>remove</v-icon>
              </v-btn>
              <v-btn flat icon @click='SetDashed(true)'>
                <v-icon>more_horiz</v-icon>
              </v-btn>              
          </v-item-group>

          <v-menu offset-y>
            <template v-slot:activator="{ on }">
              <v-btn
                dark
                v-on="on"
                icon
              >
                <v-icon>format_color_fill</v-icon>
              </v-btn>
            </template>

            <v-list dark>
              <v-list-tile
                v-for="(c, index) in colors"
                :key="index"
                @click="SetColor(c.code)"
              >
                <v-list-tile-title><v-icon :color='c.code'>format_color_fill</v-icon></v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-menu>

          <v-overflow-btn
            :items="['1', '2', '3', '5', '8']"            
            label="Stroke size"
            hide-details
            overflow
            style='width: 50px'
            @change='SetStrokeSize()'
            v-model='stroke_size'
          ></v-overflow-btn>

          <v-divider vertical/>
          <v-text-field small placeholder='Node Library Search...' class='caption' prepend-inner-icon="library_books"/>
 
        </v-toolbar>

        <!-- Using grid
        <v-card flat height='100%'>
          <div class="grey darken-4" id='canvas'
            style="background:url('grid.gif');"
          />       
        </v-card>
        -->
        <v-card flat height='100%'>          
          <div :class="canvas_color" id='canvas'/>       
        </v-card>
        
        <v-card style='height: 100px' color='red'>
          <div>ASDASD</div>
        </v-card>
        
    </v-content>

    <CodeEditor/>
    <LibrarySaveDialog/>    

    <v-footer class="pa-3" app dark>
      <v-btn color="grey darken-4" dark v-on:click="resetServer">Reset</v-btn>
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
    LibrarySaveDialog,    
  },
  data () {
    return {           
      connected: false,   
      toggle_exclusive: 2,   
      colors: [
        {code:'#F44336', color:'red'},
        {code:'#2196F3', color:'blue'},
        {code:'#4CAF50', color:'green'},
        {code:'#FFFFFF', color:'white'},
        {code:'#FFEB3B', color:'yellow'},
        {code:'#E91E63', color:'pink'}
      ],
      stroke_size: '',
      showOptionsDialog: false,
    }
  },  
  mounted(){   
    var container = document.getElementById('canvas');    
    var canvas = new Canvas(container, this.$store);
    canvas.mount();
    this.$store.commit('set_canvas', canvas);
    EventBus.$on('update_displays', this.updateCanvas); 
    
    window.setInterval(() => {this.PushModel();},30000);
  },

  methods:{  
    SetDashed(val){
      this.$store.dispatch('change_element_dashed', val);
    },
    SetStrokeSize(){
      this.$store.dispatch('change_element_stroke_size', this.stroke_size);
    },
    SetColor(color){
      this.$store.dispatch('change_element_color', color);
    },  
    PushModel: function(){
      this.$store.dispatch('push_server_model');
    },    
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
          this.$socket.emit('load_model', contents);
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
      }
    },
    canvas_color:{
      get(){
        if(this.$store.state.config.dark_mode)
          return 'grey darken-4';
        else return 'white';
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
  #canvas{
    height: 100%;
    width: 100%;
    overflow: hidden;
  }

  html{
    overflow: hidden;
  }
</style>

