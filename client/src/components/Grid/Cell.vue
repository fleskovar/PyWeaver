<template>
    <td 
      @keyup.up='$emit("up")'
      @keyup.down='$emit("down")' 
      @keyup.left='$emit("left")' 
      @keyup.right='$emit("right")'  
      @dblclick="editing" tabindex="1" 
      @click='captureFocus()' 
      @blur='is_focused=false' 
      :class='comp_cell_class' 
      @keydown="processKeyDown($event)"
      ref="cell"
      :align="align"
      >
      
      <div style='width: minmax(100px, auto)'>
          <div v-show="edit == false">
            <label style='user-select: none'> {{ value }}</label>
          </div>
          <input ref="cellinput" type="text" v-show="edit == true" v-model="cell_input" style='max-width: 30px'
            @change="$emit('input', cell_input)"
            @focus="focused"
            @blur="edit = false"
            @keydown.enter="finishEdit($event)"
            @paste ='onPaste($event)'   
            @keydown.esc="cancelEdit()"         
          >
      </div>
    </td>
</template>

<script>
export default {
    props: ['value', 'cell_class', 'align'],
  data: function() {
    return {
      edit: false,
      is_focused: false,
      cell_input: this.value,
      previous_val: ''
    }
  },
  computed: {
    comp_cell_class:{
      get(){
        var selector = '';
        if(this.cell_class != "pyw-table-header"){
          if(this.edit || this.is_focused)
            selector = 'selected';
          else selector = 'unselected';
        }
        return this.cell_class + ' '+ selector;        
      }
    }
  },
  methods: {
    focused: function() {
      //console.log('focused')
    },
    finishEdit(evt){
      //evt.preventDefault();
      this.edit = false;
      this.$emit('input', this.cell_input);

      this.$nextTick(function () {
              this.$emit('focus_lower')
        });      
    },
    processKeyDown: function(evt){
      if(this.is_focused && !this.edit){
        if ( (evt.keyCode >= 48 && evt.keyCode <= 57) || (evt.keyCode >= 65 && evt.keyCode <= 90) || (evt.keyCode >= 96 && evt.keyCode <= 105))
        {
          this.cell_input = '';
          this.editing();
        }
      }
    },
    loseFocus: function(){
      this.$refs.cell.blur();
      this.is_focused = false;
    },
    captureFocus: function(){
      if(!this.edit){
        this.$refs.cell.focus();
        this.is_focused = true;
      }
      this.$emit('focused');
    },
    selectCell(){
      this.$nextTick(function () {
              this.$refs.cell.click()
        });      
    },
    cancelEdit(){
      this.value = this.previous_val;
      this.cell_input = this.previous_val;
      this.edit = false;
    },
    editing: function() {
      this.previous_val = this.value;
      this.edit = true;
          
          this.$nextTick(function () {
              this.$refs.cellinput.focus()
        });
    },
    onPaste(evt){
          evt.preventDefault();
          var val = evt.clipboardData.getData("text/plain");
          this.$emit('paste', val);
          //this.parseText(val, row, col);
      },
  }
}
</script>

<style scoped>
.selected{
  background-color: #ffffff;
}

.unselected{
  background-color: #ffffff;
}
</style>


