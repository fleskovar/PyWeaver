<template>
	<div v-if='this.doRender'>
		<slot/>   
	</div>
</template>

<script>
export default {    
    mounted() {
        
    },
    computed: {
        doRender(){
            if(this.$parent.isBigDisplay){
                return this.$parent.isBigDisplay;
            }
            else{
                return false;
            }
        }
    }
}
</script>
