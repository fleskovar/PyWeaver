<template>
    <v-card tabindex=-1 @keydown.shift.enter.prevent="executeConsole">
        
        <v-card-text>
            <v-card 
				black 
				height='200px'
				flat class="black"	
				ref="console_display"		
				style='padding: 5px;'	
			>
				<div style='overflow-y: scroll; height: 200px' ref="console_display">
					<pre style='white-space: pre-line' >          
						{{console_text_display}}  
					</pre> 
				</div>      
            </v-card>            
                   
            <codemirror :options="cmOptions"
			 ref="console_code_editor"
			 v-model="editor_code"
			 />
            
        </v-card-text>
        
        <v-card-actions>     
            <v-spacer/>         
            <v-btn color="gray" flat v-on:click='executeConsole' dark>Execute</v-btn>
        </v-card-actions>

    </v-card>
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
		this.$refs.console_code_editor.$refs.textarea.nextElementSibling.id = "CodeMirrorConsole";
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
			editor_code: '',
		}
	},
	methods:{
		updateEditors: function(){			
				if(this.$refs.console_code_editor.codemirror)
					this.$refs.console_code_editor.codemirror.refresh();			
    	},
		executeConsole: function(){
			this.$store.dispatch('execute_console', this.editor_code);
			this.editor_code = '';
		},
    },
    
	computed:{        
        console_text_display:{
            get(){                
				var new_text = this.$store.state.console_text+'>>';				
				
				if(this.$refs.console_display && this.$refs.console_display_text)
					this.$refs.console_display.scrollTop = Math.floor (this.$refs.console_display_text.offsetHeight);				
				
				return new_text;
            }
        },        
    },
    
	watch:{		
	},
}
</script>

<style>
#CodeMirrorConsole {
  border: 1px solid #eee;
  height: 100px !important;
}
</style>