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

        <v-card v-show='!drawer_mini' style='overflow-y: scroll' height='300px'>
          <v-treeview :items="items" ref='tree'>
            <template v-slot:prepend="{ item }">
              <v-icon v-if="item.children">folder</v-icon>
              <v-icon v-if="!item.children">insert_drive_file</v-icon>
            </template>

             <template v-slot:label="{item}">
               {{item.name}}
               <v-btn v-if="!item.children" icon @click='addLibraryNode(item.lib_id)'><v-icon>add_circle_outline</v-icon></v-btn>
            </template>

          </v-treeview>
        </v-card>

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
</template>


<script>
export default {
  mounted(){

  },
    data(){
        return{
            drawer_mini: true,
            document_name: ''
        }
    },
    methods:{
      addNode: function(){      
        this.$store.dispatch('add_empty_node');     
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
        this.$socket.emit('get_template', id, this.addNodeAction)
      },
      addNodeAction: function(node_data){
          this.$store.dispatch('add_node', node_data);
      },
    },
    computed:{
      items:{
        get(){
          return this.$store.state.libraryTree;
        }
      }
    }
}
</script>

<style>

</style>


