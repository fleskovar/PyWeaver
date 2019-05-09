<template>
    <v-dialog v-model="code_dialog" width="800" persistent @keydown="inputHandler">
        <v-card>      
        <v-card-title>
          <span class="headline">Node code</span>
        </v-card-title>
        <v-card-text>    
          <codemirror :options="cmOptions" ref="code_editor" v-model="code"/> 
        </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat>Save</v-btn>
            <v-btn color="red darken-1" flat v-on:click='closeDialog'>Close</v-btn>
            <v-btn color="red darken-1" flat v-on:click='refresh'>Refresh</v-btn>
          </v-card-actions>
      </v-card>              
    </v-dialog>
</template>

<script>
import { codemirror } from 'vue-codemirror'
// require styles
import 'codemirror/lib/codemirror.css'
import 'codemirror/mode/python/python.js'
import 'codemirror/theme/base16-dark.css'

export default {
    props: ['code', 'code_dialog'],
    components:{
        codemirror
    },
    data(){
        return{
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
                autoRefresh: true
            },
            code: 'lambda x: print x'
        }
    },
    methods:{
        inputHandler: function(e){
            if (e.keyCode === 13 && e.shiftKey){
                e.preventDefault();
                this.saveCode();
            }
            else if(e.keyCode === 27){
                e.preventDefault();
                this.closeDialog();
            }
        }
    }
}
</script>

