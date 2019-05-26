<template>
	<v-dialog v-model="code_dialog" width="800" persistent @keydown="codeDialogShortcuts">          
		<v-card>      
			<v-toolbar dark color="gray">              
				<v-toolbar-title>Editor</v-toolbar-title>
				<v-btn icon><v-icon>save</v-icon></v-btn>   
				<v-spacer></v-spacer>
				<v-toolbar-items>                
				<v-btn icon dark @click="closeDialog">
					<v-icon>close</v-icon>
				</v-btn>
				</v-toolbar-items>
			</v-toolbar>

			<v-card-text>

				<v-tabs dark>
					<v-tab>Code</v-tab>
					<v-tab-item>
						<codemirror :options="cmOptions" ref="code_editor" v-model="code"/>
					</v-tab-item>

					<v-tab>Display</v-tab>
					<v-tab-item>                
						<codemirror :options="dispCmOptions" ref="code_editor" v-model="display_code"/>                
					</v-tab-item>

					<v-tab>Display Actions</v-tab>
					<v-tab-item>                
						<codemirror :options="dispActCmOptions" ref="code_editor" v-model="display_act_code"/>                
					</v-tab-item>
				</v-tabs>      
				<v-spacer/>				    
			</v-card-text>

			<v-card-actions>     
				<v-spacer/>         
				<v-btn color="green" flat v-on:click='saveCode' dark>Update</v-btn>                          
			</v-card-actions>

        </v-card>              
	</v-dialog>
</template>

<script>
// require styles
import 'codemirror/lib/codemirror.css'
import 'codemirror/mode/python/python.js'
import 'codemirror/theme/base16-dark.css'
import 'codemirror/mode/htmlmixed/htmlmixed.js'
import 'codemirror/mode/javascript/javascript.js'

import { codemirror } from 'vue-codemirror'

export default{
	components: {
		codemirror,
  	},
	data () {
		return {
			cmOptions: {
				// codemirror options
				tabSize: 4,
				indentUnit: 4,
				mode: 'python',        
				lineNumbers: true,        
				indentWithTabs: true,
				viewportMargin: Infinity,
				line: true,
				theme: 'base16-dark',
				autoRefresh: true,        
			},
			dispCmOptions: {
				// codemirror options
				tabSize: 4,
				indentUnit: 4,
				mode: 'htmlmixed',        
				lineNumbers: true,        
				indentWithTabs: true,
				viewportMargin: Infinity,
				line: true,
				theme: 'base16-dark',
				autoRefresh: true,        
			},
			dispActCmOptions: {
				// codemirror options
				tabSize: 4,
				indentUnit: 4,
				mode: 'javascript',        
				lineNumbers: true,        
				indentWithTabs: true,
				viewportMargin: Infinity,
				line: true,
				theme: 'base16-dark',
				autoRefresh: true,        
			},
		}
	},
	methods:{
		closeDialog: function(){
			this.code_dialog = false;
		},
		saveCode: function(){
			this.$store.dispatch('save_node_code',
			{
				code: this.code,
				display_code: this.display_code,
				display_act_code: this.display_act_code
				}
			);      
			this.closeDialog();
		},
		codeDialogShortcuts: function(e){
			if (e.keyCode === 13 && e.shiftKey){
				
				this.saveCode();
			}else if(e.keyCode === 27){
				
				this.closeDialog();
			}
		},
	},
	computed:{
		code:{
      get: function(){return this.$store.state.code},
      
      set: function(val)
      {
        this.$store.commit('set_code', val);
      }      
    },
    display_code:{
      get: function(){return this.$store.state.display_code},      
      set: function(val)
      {
        this.$store.commit('set_display_code', val)
      }      
    },
    display_act_code:{
      get: function(){return this.$store.state.display_act_code},      
      set: function(val)
      {
        this.$store.commit('set_display_act_code', val)
      }      
	},
	code_dialog:{
      get: function(){return this.$store.state.open_code_editor},
      
      set: function(val)
      {
        this.$store.commit('open_editor', val)
      }      
    }, 
	}
}
</script>

<style>
</style>