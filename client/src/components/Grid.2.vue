<template>
    <div>
    <v-text-field label='# Columns' v-model='columns' outline></v-text-field>
        <v-data-table
        :headers="headers"
        :items="data"
        class="elevation-1"    
        hide-actions
        >
            <template v-slot:items="props">                
                <td v-for="i in Array(header_names.length).keys()" :key='props.index+"_"+i'>

                    <v-edit-dialog
                        :return-value.sync="props.item[i]"
                        lazy
                        @save="save(props.index, i)"
                        @cancel="cancel"
                        @open="open"
                        @close="close">

                        {{ props.item[i] }}
                        
                        <template v-slot:input>
                        <v-text-field
                            @paste ='onPaste($event, props.index, i)'
                            type='text/plain'
                            v-model="props.item[i]"
                        ></v-text-field>
                        </template>
                    </v-edit-dialog>
                    
                </td>                
            </template>
        
        </v-data-table>
    </div>
</template>

<script>  

    export default {
        
        data () {
            return {                
                columns: 1,                
                data: [[]], 
            }
        },
        mounted(){
            
        },
        methods: {
            onPaste(evt, row, col){
                var val = evt.clipboardData.getData("text/plain");
                this.parseText(val, row, col);
            },
            save (row, col){
                var val = this.data[row][col];
                this.parseText(val, row, col);
            },
            parseText(val, row, col){

                var current_rows = this.data.length;
                
                var max_cols = this.columns;

                var lines = val.split(/\r?\n/); //Regex split of new lines
                var new_lines = lines.length;
                
                for(var i = 0; i < new_lines; i++){
                    
                    var row_index = i + row;
                    
                    if(row_index > current_rows-1){
                        //Checks if we need to an extra row
                        this.data.push([]); //Append empty row at the bottom
                        current_rows += 1;
                    }

                    let line = lines[i];
                    var col_values = line.split('\t'); //Split tabs
                    var new_cols = col_values.length;
                
                    var current_cols= this.data[row_index].length;

                    for(var j = 0; j < new_cols; j++){                        
                        var col_index = col + j;

                        if(col_index < current_cols-1)
                            this.data[row_index][col_index] = col_values[j];       
                        else{
                            this.data[row_index].push(col_values[j]);
                            current_cols += 1;
                        }
                    }
                    
                    if(current_cols > max_cols)
                        max_cols = current_cols;
                }

                //Keep an empty row at the bottom 
                var final_length = this.data.length;
                if(this.data[final_length-1].length > 0)
                    this.data.push([]);
                
                this.columns = max_cols;

            },
            cancel () {
                
            },
            open () {
            },
            close () {
                
            }
        },
        computed:{
            headers(){
                
                var head = [];
                for(var i = 0; i < this.header_names.length; i++){

                    var name = this.header_names[i];

                    var item = {
                    text: name,
                    align: 'middle',
                    sortable: false,
                    value: i
                    };
                    
                    head.push(item);
                }

                return head
            },
            header_names(){
                var alphabet = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ").split("");
                var a = []
                for(var i = 0; i < this.columns; i++){
                    a.push(alphabet[i]);
                }                
                return a;
            }
        }
    }
</script>