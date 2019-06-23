<template>
    <table :key='table_key' class='pyw-table'>
    <thead>

      <tr>
        <th></th>
        <th v-for="(key, index) in value.columns" :key='index' class='pyw-table-header'>
          <button color='grey lighten-2' style='min-width: 0; width: 25px; height: 25px; min-height: 0;' @click='deleteColumn(index)'>
            <v-icon style='font-size: 10px;'>
              close
            </v-icon>
          </button>
        </th>

        <th class='pyw-table-header'>
          <button color='grey lighten-2' style='min-width: 0; width: 25px; height: 25px; min-height: 0;' @click='addColumn()' v-if='enable_column_expand'>
            <v-icon style='font-size: 10px;'>
              add
            </v-icon>
          </button>
        </th>
      </tr>

      <tr>
        <th ></th>
        <th v-for="(key, index) in value.columns" :key='index' class='pyw-table-header'>          
          Type: <select v-model='value.column_types[index]'>
            <option value="Number" selected="selected">Number</option>
            <option value="Text">Text</option>
            <option value="Date">Date</option>
          </select>
        </th>
        <th class='pyw-table-header'></th>
      </tr>

      <tr>
        <th style='user-select: none' class='table-header'></th>        
        <Cell v-for="(key, index) in value.columns"
          :key='index'
          v-bind:value='value.columns[index]'
          v-on:input='(val) => columnChanged(val, index)'          
          :cell_class='"pyw-table-header"'       
          :align='"center"'                 
          ></Cell>
          <th class='pyw-table-header'></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(row, i) in value.data" :key='"row_"+i'> 
          
          <td style='user-select: none' class='pyw-table-header' v-if='i < value.data.length-1'>
            <span>
              <button style='min-width: 0; width: 25px; height: 25px; min-height: 0;' color='grey lighten-2' @click='deleteRow(i)'>
                <v-icon style='font-size: 10px;'>close</v-icon>
              </button>              
              {{i}}
            </span>
          </td> 

          <td v-if='i == value.data.length-1' style='min-width: 40px; min-height: 30px' class='pyw-table-header'>
            <span ></span>
          </td>

          <Cell v-for="(col_name, j) in value.columns"
           :key='"cell_"+i+"_"+j'
           :ref='"cell_"+i+"_"+j'           
           v-bind:value='row[j]'
           v-on:input='(val) => cellChanged(val, i, j)'
           @focused='selected_cell={i: i, j: j}'
           @paste="(val) =>{parseVal(val, i, j)}"
           @focus_lower="focusLower(i, j)"
           @up='moveRow(-1, i, j)'
           @down='moveRow(1, i, j)'
           @left='moveCol(-1, i, j)'
           @right='moveCol(1, i, j)'
           :cell_class='"pyw-table-td"'
           :align='"right"' 
           >
           
           </Cell>

           <td class='pyw-table-td'> ... </td>
      </tr>
    </tbody>
  </table>
</template>

<style>
    .pyw-table {
    border-radius: 3px;
    background-color: #ffffff;
    color: rgba(0, 0, 0, 0.66);
    border-spacing: 0;
    border-collapse: collapse;
    }

    .table-action-btn {
      min-width: 0;
      width: 25px;
      height: 25px;
      min-height: 0;
    }

    .pyw-table-header {
    background-color: #dbe2df;
    border: 1px solid rgb(168, 167, 167);
    color: rgba(0, 0, 0, 0.66);
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    }
    
    .pyw-table-td {
      background-color: #ffffff;
      min-width: 50px;
      min-height: 25px;
      padding: 5px 20px;
      border: 1px solid rgb(168, 167, 167);
    }
    
</style>

<script>
import Cell from './Cell'

export default {
  props:{
    value:{
      type: Object,
      default: () => ({
        data: [[]],
        columns: ['0'],
        column_types: ['Number']
        })
    },
    enable_column_expand:{
      type: Boolean,
      default: true
    }
  }, 
  components:{
    Cell
  },
  data: function() {    
    return {      
      selected_cell: {i:0, j:0},
      table_key: -1
    }
  },
  methods: {
    deleteColumn: function(index){
      for(var i = 0; i < this.value.data.length; i++){

        var row = this.value.data[i];

        if(index <= row.length-1){
          //The row has enough columns to delete
          this.value.data[i].splice(index, 1);
        }
      }

      this.value.columns.splice(index, 1);
      this.value.column_types.splice(index, 1);
      this.redrawTable();

    },
    focusLower: function(i, j){
      var ref_code = "cell_"+(i+1).toString()+"_"+j.toString();
      this.$refs[ref_code][0].selectCell();
    },
    moveCol: function(dir, i, j){
      var new_col = j + dir;
      var current_code = "cell_"+i+"_"+j;
      try{        
        var ref_code = "cell_"+i+"_"+new_col;
        this.$refs[ref_code][0].selectCell();
        this.$refs[current_code][0].loseFocus();
      }catch{}      
    },
    moveRow: function(dir, i, j){
      var new_row = i + dir;
      var current_code = "cell_"+i+"_"+j;
      try{        
        var ref_code = "cell_"+new_row+"_"+j;
        this.$refs[ref_code][0].selectCell();
        this.$refs[current_code][0].loseFocus();
      }catch{}
    },
    cellChanged: function(val, i, j){
      this.value.data[i][j] = val;
      this.paddFinalRow();
      this.redrawTable();
      var next_row_i = i + 1;
      this.$nextTick(() => {
        this.$refs["cell_"+next_row_i+"_"+j][0].$el.click();
      });
      
    },
    deleteRow: function(i){
      this.value.data.splice(i, 1);
      this.redrawTable();
    },
    addColumn: function(){
      var col = 1;

      while(this.value.columns.indexOf(col.toString())>0){
        col += 1;
      }

      this.value.columns.push(col.toString());
      this.value.column_types.push('Number');
      this.redrawTable();
    },    
    columnChanged: function(val, i){
      this.value.columns[i] = val;
      this.redrawTable();
    },
    redrawTable: function(){
      this.table_key = this.table_key * -1;
    },    
    parseVal: function(val, i, j){
      this.parseText(val, i, j);
      this.redrawTable();
    },
    parseText(val, row, col){

        var current_rows = this.value.data.length;
        
        var max_cols = this.value.columns;

        var lines = val.split(/\r?\n/); //Regex split of new lines
        var new_lines = lines.length;
        
        for(var i = 0; i < new_lines; i++){
            
            var row_index = i + row;
            
            if(row_index > current_rows-1){
                //Checks if we need to an extra row
                this.value.data.push([]); //Append empty row at the bottom
                current_rows += 1;
            }

            let line = lines[i];
            var col_values = line.split('\t'); //Split tabs
            var new_cols = col_values.length;
        
            var current_cols= this.value.data[row_index].length;

            for(var j = 0; j < new_cols; j++){                        
                var col_index = col + j;

                if(col_index <= current_cols-1)
                    this.value.data[row_index][col_index] = col_values[j];       
                else{
                    this.value.data[row_index].push(col_values[j]);
                    current_cols += 1;
                }
            }
            
            if(current_cols > max_cols)
                max_cols = current_cols;
        }

        this.paddFinalRow();
        //this.updateRedrawKey();               
    },
    checkForEmptyRow(row){

      var return_val = true;

      for(var i=0; i<row.length; i++){
        if(i in row){
          if (row[i].trim().length > 0)
            return_val = false;
            break
        }
      }

      return return_val

    },

    paddFinalRow(){
      //Keep an empty row at the bottom 
        var final_length = this.value.data.length;
        if(this.value.data[final_length-1].length > 0 && !this.checkForEmptyRow(this.value.data[final_length-1]))
        {
            this.value.data.push([]);
        }
    },
  }
}
</script>

