<template>
    <v-navigation-drawer permanent clipped right dark app width='400' :mini-variant="drawer_mini">  
      
      <v-list>
        <v-list-tile>          
          <v-list-tile-content></v-list-tile-content>
          <v-list-tile-action @click="toggleMiniDrawer">
            <v-btn icon>
              <v-icon v-if="drawer_mini">keyboard_arrow_left</v-icon>
              <v-icon v-if="!drawer_mini">keyboard_arrow_right</v-icon>
            </v-btn>
          </v-list-tile-action>        
        </v-list-tile>        
        
        <v-list-tile>
          <!--Here goes a title -->
        </v-list-tile>

        <v-divider/>

        <v-list-tile>
          <v-list-tile-action>
            <v-btn icon class="text-lg-right">              
              <v-icon>desktop_windows</v-icon>
            </v-btn>
          </v-list-tile-action>   
          <v-list-tile-content>Console</v-list-tile-content>     
        </v-list-tile>

        <Console v-show='!drawer_mini'/>

        <v-divider/>

        <v-list-tile @click="drawer_mini = false">
          <v-list-tile-action>
            <v-btn icon class="text-lg-right">              
              <v-icon>remove_red_eye</v-icon>
            </v-btn>
          </v-list-tile-action>   
          <v-list-tile-content>Watch</v-list-tile-content>     
        </v-list-tile>    

        <v-card v-show='!drawer_mini' black style='padding: 20px; overflow-y: scroll' height='300px' flat class="black">          
          Here goes the watcher
        </v-card>  

        

        <v-card v-show='!drawer_mini' style='padding: 20px; overflow-y: scroll' height='300px' flat>          
          This is a thing
        </v-card>

        <v-divider/>

      </v-list>      

    </v-navigation-drawer>
</template>


<script>
import OptionsDialog from './OptionsDialog.vue'
import Console from './Console.vue'

export default {
  components:{
    OptionsDialog,
    Console,
  },
  mounted(){

  },
    data(){
        return{
            drawer_mini: true,            
            showOptionsDialog: false,
            console_input: '',
        }
    },
    methods:{
      printToConsole: function(){
        console.log('yay');
      },
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
      
    }
}
</script>

<style>

</style>


