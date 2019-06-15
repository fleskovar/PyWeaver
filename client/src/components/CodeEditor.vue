<template>
	<v-dialog v-model="code_dialog" width="800" persistent @keydown="codeDialogShortcuts">          
		<v-card>      
			<v-toolbar dark color="gray">              
				<v-toolbar-title>Editor</v-toolbar-title>
				<v-btn icon @click='openSaveDialog'><v-icon>save</v-icon></v-btn>   
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
						<div :key='bug_key'>{{error_text}}</div>
					</v-tab-item>

					<v-tab>Display</v-tab>
					<v-tab-item>                
						<codemirror :options="dispCmOptions" ref="ui_editor" v-model="display_code"/>                
					</v-tab-item>

					<v-tab>Display Actions</v-tab>
					<v-tab-item>                
						<codemirror :options="dispActCmOptions" ref="script_editor" v-model="display_act_code"/>                
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

export default {
	components: {
		codemirror,
	},
	mounted(){		
    window.setInterval(() => {this.updateEditors();},250);
	},
	data(){
		return {
			bug_key: -1,
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
			has_error: false,
		}
	},
	methods:{
		bugHighlight(){
			this.bug_key = this.bug_key * -1;
			if(this.error_line != -1){
				var actual_line = this.error_line-1;
				console.log('error in line '+actual_line);
				this.$refs.code_editor.cminstance.addLineClass(actual_line, 'background', 'line-error');
				}
		},
		bugUnHighlight(){
			if(this.error_line != -1){
				var actual_line = this.error_line-1;
				this.$refs.code_editor.cminstance.removeLineClass(actual_line, 'background', 'line-error');
				}
		},
		updateEditors: function(){
			if(this.code_dialog){
				if(this.$refs.code_editor.codemirror)
					this.$refs.code_editor.codemirror.refresh();

				if(this.$refs.ui_editor.codemirror)
					this.$refs.ui_editor.codemirror.refresh();
				
				if(this.$refs.script_editor.codemirror)
					this.$refs.script_editor.codemirror.refresh();
			}
    	},
		closeDialog: function(){
			this.bugUnHighlight();
			this.code_dialog = false;
		},
		openSaveDialog: function(){
			this.$store.commit('set_dialog_open', true);
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
			if(this.code_dialog){
				if (e.keyCode === 13 && e.shiftKey){
					
					this.saveCode();
				}else if(e.keyCode === 27){
					
					this.closeDialog();
				}
			}
		},
	},
	computed:{
		error_line:{
			get: function(){
				var node_id = this.$store.state.selected_node.id;
				if(node_id && this.$store.state.code_error_dict[node_id]){
					return this.$store.state.code_error_dict[node_id].line
				}else{
					return -1
				}
			}
		},
		error_text:{
			get(){
				var node_id = this.$store.state.selected_node.id;
				if(node_id && this.$store.state.code_error_dict[node_id]){
					return this.$store.state.code_error_dict[node_id].error
				}else{
					return ''
				}
			}
		},
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
	},
	watch:{
		code_dialog: function(new_val, old_val){
			if(new_val){        
				this.bugHighlight();        
			}
		}
	},
}
</script>

<style>
	.line-error {
            background: rgb(94, 22, 25) !important;
            color: #8a1f11 !important;
        }

</style>