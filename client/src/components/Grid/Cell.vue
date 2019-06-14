<template>
    <td @dblclick="editing" tabindex="1" @click='captureFocus()' @blur='is_focused=false' :class='comp_cell_class' >
      <div style='width: minmax(100px, auto)'>
          <div v-show="edit == false">
            <label style='user-select: none'> {{ value }}</label>
          </div>
          <input ref="cellinput" type="text" v-show="edit == true" v-model="cell_input"
            @change="$emit('input', cell_input)"
            @focus="focused" @blur="edit = false"
            @keyup.enter="edit == false"
            @paste ='onPaste($event)'
            >
      </div>
    </td>
</template>

<script>
export default {
    props: ['value', 'cell_class'],
  data: function() {
    return {
      edit: false,
      is_focused: false,
      cell_input: this.value
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
      console.log('focused')
    },
    captureFocus: function(){
      if(!this.edit){
        this.$el.focus();
        this.is_focused = true;
      }
      this.$emit('focused');
    },
    editing: function() {
      this.edit = true;
          
          this.$nextTick(function () {
              this.$refs.cellinput.focus()
        });
    },
    onPaste(evt){
          console.log('pasted');
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
  background-color: #c1f8c1;
}

.unselected{
  background-color: #f1f1f1;
}
</style>


