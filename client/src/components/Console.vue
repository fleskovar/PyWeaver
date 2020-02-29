<template>
    <v-card>
        
        <v-card-text>
            <v-card 
				black style='padding: 5px; overflow-y: scroll'
				height='200px'
				flat class="black"				
			>
				<pre style='white-space: pre-line'>          
                	{{console_text_display}}  
				</pre>       
            </v-card>            
                   
            <codemirror :options="cmOptions"
			 ref="console_code_editor"
			 v-model="editor_code"	
			 @keydown="codeShortcuts"		 			 
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
		codeShortcuts: function(e){
			console.log('yay');
			if (e.keyCode === 13 && e.shiftKey){
				
				this.executeConsole();
			}			
		},
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
                return this.$store.state.console_text+'>>';
            }
        },        
    },
    
	watch:{		
	},
}
</script>

<style scoped>
.CodeMirror {
  border: 1px solid #eee;
  height: 100px;
}
</style>