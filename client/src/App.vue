<template>
  <v-app>
    <v-toolbar app dark fixed clipped-left flat>
      <v-toolbar-title class="headline text-uppercase pr-5">
        <span>Py</span>
        <span class="font-weight-light">Weaver</span>
      </v-toolbar-title>
      
      <v-divider vertical/>
        
      <!--Server Control + Files save/load -->
      <v-item-group dense class="pa-2">
        <v-btn flat small icon @click='OpenFile'>          
          <v-icon>folder_open</v-icon>
        </v-btn>
        <v-btn flat small icon @click='SaveModel'>
          <v-icon>cloud_download</v-icon>
        </v-btn>
      </v-item-group>
      <v-divider vertical/>        
      <v-item-group dense>
        <v-btn flat icon small @click="runServer()">
          <v-icon small>play_arrow</v-icon>
        </v-btn>
        <v-btn flat icon small>
          <v-icon small>pause</v-icon>
        </v-btn>  
        <v-btn flat icon small @click="resetServer">
          <v-icon small>refresh</v-icon>
        </v-btn>            
      </v-item-group>

      <v-spacer></v-spacer>

      <v-chip color="green" text-color="white" v-if='connected'>Connected</v-chip>  
      <v-chip color="red" text-color="white" v-if='!connected'>Disconnected</v-chip>
    </v-toolbar>
    <input type='file' id='fileInput' v-on:change='OpenModel($event)' hidden>

    <SideBar/>

    <v-content style='overflow: hidden'>

        <!--Edges and cells format + Library quick search-->
        <v-toolbar dark class="grey darken-2" dense>          
                      
          Outline        
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
          <v-autocomplete ref='search_bar'
           small placeholder='Node Library Search...'
           class='caption'
           prepend-inner-icon="library_books"
           :items="calc_list"
           :filter="nodeLibraryFilter"
           return-object
           v-model='library_search_val'
           auto-select-first
           @change='librarySearchSelection(library_search_val)'
           @blur='librarySearchMenu = false'
           @keyup.esc='loseLibrarySearchFocus()'
           :menu-props="{
             value: librarySearchMenu,
             openOnClick: true, 
             dark: true,
             closeOnContentClick:true, 
             closeOnClick:true,
             }"
           >

            <template v-slot:selection="data">
                {{data.item.name}}
            </template>

            <!--
            <template v-slot:item="data">              
                <template>
                  <v-list-tile-avatar @click='librarySearchSelection(data.item)'>
                    <img :src="data.item.avatar">
                  </v-list-tile-avatar>
                  <v-list-tile-content @click='librarySearchSelection(data.item)'>
                    <v-list-tile-title v-html="data.item.name"></v-list-tile-title>
                    <v-list-tile-sub-title v-html="data.item.description"></v-list-tile-sub-title>
                  </v-list-tile-content>
                </template>              
            </template>
            -->

            <template v-slot:item="data">              
                <template>
                  <v-list-tile-avatar>
                    <img :src="data.item.avatar">
                  </v-list-tile-avatar>
                  <v-list-tile-content>
                    <v-list-tile-title v-html="data.item.name"></v-list-tile-title>
                    <v-list-tile-sub-title v-html="data.item.description"></v-list-tile-sub-title>
                  </v-list-tile-content>
                </template>              
            </template>

          </v-autocomplete>
          <v-btn icon @click="$socket.emit('refresh_library')">
            <v-icon>
              refresh
            </v-icon>
          </v-btn>

        </v-toolbar>


        <!-- Using grid
        <v-card flat height='100%'>
          <div class="grey darken-4" id='canvas'
            style="background:url('grid.gif');"
          />       
        </v-card>
        -->
        <v-card flat height='100%'>          
          <div id='outlineContainer'/>
          <div :class="canvas_color" id='canvas'/>       
        </v-card>
        
        <v-card style='height: 100px' color='red'>
          <div>ASDASD</div>
        </v-card>
        
    </v-content>

    <CodeEditor/>
    <RefactorFunctionalize/>
    <LibrarySaveDialog/>    

    <v-footer class="pa-3" app dark>
      <v-spacer></v-spacer>
        <div>&copy; {{ new Date().getFullYear() }}</div>
    </v-footer>

  </v-app>
</template>

<script>
import Canvas from './NodeEditor/Canvas'
import CodeEditor from './components/CodeEditor'
import RefactorFunctionalize from './components/RefactorFunctionalize'
import SideBar from './components/SideBar'
import LibrarySaveDialog from './components/LibrarySaveDialog'
import EventBus from './EventBus.js'
import fuzzysort from 'fuzzysort'

export default {
  name: 'App',
  components: {
    CodeEditor,
    SideBar,
    LibrarySaveDialog,    
    RefactorFunctionalize,
  },
  data () {
    return {           
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
      library_search_val: null,
      librarySearchMenu: false,
      library_sort: null,
      connected: false
    }
  },
  mounted(){   
    var container = document.getElementById('canvas');    
    var outline_container = document.getElementById('outlineContainer');    

    var canvas = new Canvas(container, outline_container, this.$store);
    canvas.mount();
    this.$store.commit('set_canvas', canvas);
    EventBus.$on('update_displays', this.updateCanvas); 
    //this.library_sort = fuzzysort.new({threshold: -1000});
    this.library_sort = fuzzysort.new();
    
    window.setInterval(() => {this.PushModel();},30000);

    var vm = this;
    window.addEventListener('keyup', function(event) {
      // If down arrow was pressed...
      if (event.target.localName != 'input' && event.target.localName != 'textarea')
      { 
        if(event.target.className == 'mxCellEditor mxPlainTextEditor')
        {
          if(event.keyCode === 13){
            event.target.blur();
          }
        }else{
          if(event.keyCode == 32){
            vm.captureSearchFocus();
          }
          else if(event.keyCode === 13 && event.shiftKey){
            vm.runServer();
          }     
        }   
      }
    });

    this.$socket.emit('refresh_library');

    this.connected = this.$socket.connected;

  },
  methods:{    
    loseLibrarySearchFocus(){
      this.$refs.search_bar.blur();
      this.$nextTick(() => {
        this.library_search_val = false;
        this.librarySearchMenu = false;        
      });
    },
    runServer: function(){
      this.$store.dispatch('execute_server');
    },  
    librarySearchSelection: function(item){
      if(item && item.hasOwnProperty('lib_id')){
        this.$socket.emit('load_node', item.lib_id);
        this.$nextTick(() => {
          this.library_search_val= null; 
        });        
      }
    },
    nodeLibraryFilter (item, queryText, itemText) {
      if(item){
        /*
        var results = this.library_sort.go(queryText, this.calc_list,
        {
          keys: ['name', 'keywords', 'description'],       
          scoreFn: (a) => Math.max(a[0]?a[0].score:-1000, a[1]?a[1].score-100:-1000),
        });
        */

        var results = this.library_sort.single(queryText, item.name);
        if(results)
          return true
        else return false     
      }else return true
    },
    captureSearchFocus(){      
      this.$refs.search_bar.focus();
      this.library_search_val= null;
      this.librarySearchMenu = true;
    },
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
        var proceed = false;
        
        proceed = confirm("Reset server? This will erase all unsaved data");

        if(proceed)
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
    calc_list:{
      get: function(){
        return this.$store.state.calcs_list;
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
      this.$socket.emit('refresh_library');      
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

  #outlineContainer{
    position: absolute;
    overflow: hidden;
    top: 0px;
    right: 0px;
    width: 200px;
    height: 140px;
    background: white;
    border-style: solid;
    border-color: black;
    z-index: 99;
    touch-action: none;
  }
</style>

