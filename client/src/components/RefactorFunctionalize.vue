<template>
	<v-dialog v-model="code_dialog" width="800" persistent>          
		<v-card>      
			<v-toolbar dark color="gray">              
				<v-toolbar-title>Editor</v-toolbar-title>
				<v-spacer></v-spacer>
				<v-toolbar-items>                
				<v-btn icon dark @click="closeDialog">
					<v-icon>close</v-icon>
				</v-btn>
				</v-toolbar-items>
			</v-toolbar>

			<v-card-text>
				<v-select
					v-model="selected_vars"
					:items="refactor_func_dialog_vars"
					attach
					chips
					label="Inner variables"
					multiple
				/>
				    
			</v-card-text>

			<v-card-actions>     
				<v-spacer/>         
				<v-btn color="green" flat v-on:click='refactorCode' dark>Refactor</v-btn>                 
			</v-card-actions>

        </v-card>              
	</v-dialog>
</template>

<script>
// require styles
export default {
	components: {
	},
	mounted(){},
	data(){
		return {			
			selected_vars: []
		}
	},
	methods:{
		
		closeDialog: function(){
			this.code_dialog = false;
		},
		
		refactorCode: function(){
			this.$store.dispatch('refactor_to_function',
				{
					node_id: 'n_1',
					inner_vars: this.selected_vars
				}
			);      
			this.closeDialog();
		},
		
	},
	computed:{
		refactor_func_dialog_vars:{
			get: function(){return this.$store.state.refactor_func_options}    
		},
		refactor_node_id:{
			get: function(){return this.$store.state.refactor_node_id}    
		},
		code_dialog:{
			//Determines if the dialog should be open or not
			get: function(){return this.$store.state.show_refactor_func_dialog},
			set: function(val){
				this.$store.commit('set_show_refactor_func_dialog', val);
			}
		}
	}	
}
</script>

<style>

</style>