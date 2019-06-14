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
                <v-checkbox v-model="darkMode" :label="`Dark Mode (requires page reload)`"/>
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
            get(){return this.$store.state.config.auto_exec},
            set(val){ 
                this.$store.commit('set_auto_exec', val);
                this.$store.dispatch('save_config_file');
            }
        },
        autoSync:{
            get(){return this.$store.state.config.sync_model},
            set(val){ 
                this.$store.commit('set_auto_sync', val);
                this.$store.dispatch('save_config_file');
            }
        },
        darkMode:{
            get(){return this.$store.state.config.dark_mode},
            set(val){ 
                this.$store.dispatch('change_dark_mode', val);
                this.$$store.dispatch('sync_model_with_server');
                this.$store.dispatch('save_config_file');
            }            
        }
    }
}
</script>
