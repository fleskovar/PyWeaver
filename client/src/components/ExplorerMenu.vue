<template>
    <v-navigation-drawer permanent clipped right dark app width='500' :mini-variant="drawer_mini">  
      
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
        <v-divider/>
        
        <v-tabs dark v-model="tab" v-show="!drawer_mini"> 
					<v-tab key="console"> <v-icon>desktop_windows</v-icon> </v-tab>
					<v-tab key="inspector"> <v-icon>remove_red_eye</v-icon> </v-tab>	
          
          <v-tab-item key="console">
            <v-divider/>
            <br>
            Console
            <v-divider/> 
            <Console/>                
          </v-tab-item>

          <v-tab-item key="inspector">
            <v-divider/>
            <br>
            Inspector
            <v-divider/>  
            <br>
            <ConnectionOrderControl/>
          </v-tab-item>

				</v-tabs>

      </v-list>      

    </v-navigation-drawer>
</template>


<script>
import Console from './Console.vue'
import ConnectionOrderControl from './ConnectionOrderControl.vue'

export default {
  components:{
    Console,
    ConnectionOrderControl,
  },
  mounted(){

  },
    data(){
        return{            
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
      drawer_mini:{
        get: function(){
          return this.$store.state.explorer_menu_open;
        },
        set: function(val){
          this.$store.commit('set_explorer_menu_open', val);
        }
      },

      tab:{
        get: function(){
          return this.$store.state.explorer_menu_tab;
        },
        set: function(val){
          this.$store.commit('set_explorer_menu_tab', val);
        }
      }

    }
}
</script>

<style>

</style>


