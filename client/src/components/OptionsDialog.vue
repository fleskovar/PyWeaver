<template>
    <v-dialog v-model="value" width="800" persistent>  
        <v-card>      
			<v-toolbar dark color="gray">              
				<v-toolbar-title>Options</v-toolbar-title>   
				<v-spacer></v-spacer>
				<v-toolbar-items>                
				<v-btn icon dark @click="$emit('close')">
					<v-icon>close</v-icon>
				</v-btn>
				</v-toolbar-items>
			</v-toolbar>

            <v-card-text>
                <v-checkbox v-model="autoRun" :label="`Automatically run flowsheet`"/>
                <v-checkbox v-model="autoSync" :label="`Automatically sync model`"/>
                <v-checkbox v-model="darkMode" :label="`Dark Mode`"/>
            </v-card-text>

        </v-card>


    </v-dialog>
</template>

<script>
export default {
    props:['value'],
    data(){
        return{}
    },
    computed:{
        autoRun:{
            get(){return this.$store.state.auto_exec},
            set(val){ this.$store.commit('set_auto_exec', val)}
        },
        autoSync:{
            get(){return this.$store.state.sync_model},
            set(val){ this.$store.commit('set_auto_sync', val)}
        },
        darkMode:{
            get(){return this.$store.state.dark_mode},
            set(val){ this.$store.dispatch('change_dark_mode', val)}            
        }
    }
}
</script>
