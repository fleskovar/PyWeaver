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

				<v-tabs dark v-model="current_mode"> 
					<v-tab v-on:click='show_code()' key="code">Code</v-tab>
					<v-tab v-on:click='show_display()' key="ui">Display</v-tab>
					<v-tab v-on:click='show_display_script()' key="ui_script">Display Actions</v-tab>
				</v-tabs>      
				<v-spacer/>				    
				
				<codemirror :options="cmOptions" ref="code_editor" v-model="editor_code"/>
				<v-card dark :key='bug_key'>{{error_text}}</v-card>
			
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
				viewportMargin: Infinity,
				line: true,
				theme: 'base16-dark',
				autoRefresh: true,        
			},
			has_error: false,
			current_mode: 0,
			editor_code: '',
		}
	},
	methods:{
		bugHighlight(){
			this.bug_key = this.bug_key * -1;
			if(this.error_line != -1){
				var actual_line = this.error_line-1;
				this.$refs.code_editor.cminstance.addLineClass(actual_line, 'background', 'line-error');
				this.$refs.code_editor.codemirror.refresh();

				}
		},
		backup_code(){
			
			if(this.current_mode==0){
				this.code = this.editor_code;
			}
			else if(this.current_mode==1){
				this.display_code = this.editor_code;
			}
			else if(this.current_mode==2){
				this.display_act_code = this.editor_code;
			}

			//Backup the code based on the current mode
		},
		show_code(){
			//TODO: Save and switch code whenever it is edited
			this.backup_code(); //Based on the editing mode, save the code in a specific variable
			this.setEditorMode("python");
			this.editor_code = this.code; //Populates the editor with the stored code
		},
		show_display(){
			this.backup_code(); //Based on the editing mode, save the code in a specific variable
			this.setEditorMode("htmlmixed");
			this.editor_code = this.display_code; //Populates the editor with the stored code
		},
		show_display_script(){
			this.backup_code(); //Based on the editing mode, save the code in a specific variable
			this.setEditorMode("javascript");
			this.editor_code = this.display_act_code; //Populates the editor with the stored code
		},
		setEditorMode(mode){
    			this.$refs.code_editor.codemirror.setOption("mode", mode);
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

			this.backup_code();

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
					return 'Error text'
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
			
			if(!old_val){
				//Opening the editor
				this.setEditorMode("python");
				this.current_mode = 0; //Code
				this.editor_code = this.code; //Populates the editor with the stored code			
			}
			
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