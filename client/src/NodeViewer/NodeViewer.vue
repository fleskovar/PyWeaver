<template>
  <div>
      A viewer: {{test_val}}!
  </div>
</template>

<script>


export default {
  name: 'NodeViewer',

  data() {
    return {           
      test_val: 'a test val',
    }
  },
  mounted(){
    //TODO parse this to get data from server
    var node_id = window.location.search
      .split('?')[1]
      .split('=')[1];
    console.log(node_id);

    this.test_val = node_id;
  },
  sockets:{
    connect: function(){
      //this.connected = true;
      //this.$socket.emit('refresh_library');      
      console.log('connected!')
    },
    disconnect: function(){
      //this.connected = false;
    }
  }
  
}
</script>

<style>
 
</style>

