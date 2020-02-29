<template>
    <v-card>
        
        <v-card-text>
            <v-card v-show='!drawer_mini' black style='padding: 5px; overflow-y: scroll' height='200px' flat class="black">          
                {{console_text_display}}         
            </v-card>            
                   
            <codemirror :options="cmOptions" ref="console_code_editor" v-model="editor_code"/>
            
        </v-card-text>
        
        <v-card-actions>     
            <v-spacer/>         
            <v-btn color="gray" flat v-on:click='saveCode' dark>Submit</v-btn>
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
            console_text: '',
		}
	},
	methods:{		
		codeDialogShortcuts: function(e){
			if(this.code_dialog){
				if (e.keyCode === 13 && e.shiftKey){
					//Submit code
				}
			}
		},
    },
    
	computed:{
        
        console_text_display:{
            get(){
                var display_tect = this.console_text + "\n >>";
                return display_tect;
            }
        },
        
    },
    
	watch:{		
	},
}
</script>

<style>
.CodeMirror {
  border: 1px solid #eee;
  height: 100px;
}
</style>