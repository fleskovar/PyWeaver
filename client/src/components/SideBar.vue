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

        <v-list-tile @click="addNode">
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

        

        <v-card v-show='!drawer_mini' style='padding: 20px; overflow-y: scroll' height='300px' flat>          
          <v-treeview :items="items" ref='tree' open-on-click>
            <template v-slot:prepend="{ item }">
              <v-icon v-if="item.children">folder</v-icon>
              <v-icon v-if="!item.children">insert_drive_file</v-icon>
            </template>

             <template v-slot:label="{item}">              
              <span @dblclick='addLibraryNode(item.lib_id)'>{{item.name}}</span>
              <!--<v-icon v-if="!item.children">add_circle_outline</v-icon>-->
              <v-btn v-if="item.id==0" icon @click='refreshLibrary'><v-icon>refresh</v-icon></v-btn> <!--Adds a special refresh icon for the root folder to trigger library refresh on the server--> 
            </template>

          </v-treeview>
        </v-card>

        <v-divider/>


        <v-list-tile @click='showOptionsDialog=true'>
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
      
    },
    computed:{
      items:{
        get(){
          return this.$store.state.libraryTree;
        }
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


