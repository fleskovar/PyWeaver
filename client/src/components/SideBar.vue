<template>
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
          <v-list-tile-content>ADD EMPTY NODE</v-list-tile-content>     
        </v-list-tile>

        <v-divider/>

        <v-list-tile @click="drawer_mini = false">
          <v-list-tile-action>
            <v-btn icon class="text-lg-right">              
              <v-icon>library_books</v-icon>
            </v-btn>
          </v-list-tile-action>   
          <v-list-tile-content>Node Library</v-list-tile-content>     
        </v-list-tile>        

        <v-card v-show='!drawer_mini' style='padding: 10px'>
          <v-text-field
            v-model="search"
            label="Search Node Library"
            dark
            flat
            solo-inverted
            hide-details
            clearable
            clear-icon="mdi-close-circle-outline"
          />
        </v-card>

        <v-card v-show='!drawer_mini' style='padding: 20px; overflow-y: scroll' height='300px' flat>          
          <v-treeview :items="items" ref='tree' :search="search" :filter="filter" open-on-click>
            <template v-slot:prepend="{ item }">
              <v-icon v-if="item.children">folder</v-icon>
              <v-icon v-if="!item.children">insert_drive_file</v-icon>
            </template>

             <template v-slot:label="{item}">
              <div @click='addLibraryNode(item.lib_id)'>
                {{item.name}}
                <v-icon v-if="!item.children">add_circle_outline</v-icon>
                <v-btn v-if="item.id==0" icon @click='refreshLibrary'><v-icon>refresh</v-icon></v-btn> <!--Adds a special refresh icon for the root folder to trigger library refresh on the server--> 
              </div>
            </template>

          </v-treeview>
        </v-card>

        <v-divider/>

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
            <v-btn icon class="text-lg-right" @click='showOptionsDialog=true'>              
              <v-icon>settings</v-icon>
            </v-btn>
          </v-list-tile-action>   
          <v-list-tile-content>SETTINGS</v-list-tile-content>     
        </v-list-tile>
      </v-list>

      <OptionsDialog v-model='showOptionsDialog' v-on:close='showOptionsDialog=false'/>

    </v-navigation-drawer>
</template>


<script>
import Fuse from 'fuse.js';
import OptionsDialog from './OptionsDialog.vue'

export default {
  components:{
    OptionsDialog
  },
  mounted(){

  },
    data(){
        return{
            drawer_mini: true,            
            search: '',
            fuse_options: {
              keys:['name'],
              distance: 100,
              location: 0,
              maxPatternLength: 32,
              minMatchCharLength: 1,
              id: "id"
            },
            showOptionsDialog: false
        }
    },
    methods:{
      addNode: function(){      
        this.$socket.emit('new_empty_node');     
      },
      refreshLibrary(){
        this.$socket.emit('refresh_library');
      },
      runServer: function(){
        this.$store.dispatch('execute_server');
      },
      resetServer: function(){
        //Resets server
        this.$socket.emit('reset');
      },
      toggleMiniDrawer: function(){
          this.drawer_mini = !this.drawer_mini;
      },
      addLibraryNode: function(id){
        this.$socket.emit('load_node', id)
      },      
      treeFilter: function(item, search, textKey){

          var fuse = new Fuse(this.items, this.fuse_options);
          var search_results = fuse.search(search);

          return search_results.indexOf(item.id) > -1
      },
    },
    computed:{
      items:{
        get(){
          return this.$store.state.libraryTree;
        }
      },
      filter(){        
        return this.treeFilter;
      },
      document_name:{
        get(){ return this.$store.state.document_name},
        set(val){ this.$store.commit('set_document_name', val);}
      }
    }
}
</script>

<style>

</style>


