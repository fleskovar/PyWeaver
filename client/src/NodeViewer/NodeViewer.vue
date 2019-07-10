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
    var params = window.location.search;
    console.log(params);
  },
  
}
</script>

<style>
 
</style>

