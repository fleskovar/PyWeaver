<template>
    <div>
        <div v-show="edit == false">
        <label @dblclick="editing"> {{ cell }}</label>
        </div>
        <input ref="cellinput" type="text" v-show="edit == true" v-model="cell" @focus="focused" @blur="edit = false" @keyup.enter="edit == false">
    </div>
</template>

<script>
export default {
    props: ['entry', 'k'],
  data: function() {
    return {
      edit: false
    }
  },
  computed: {
    cell: {
      get: function() {
        console.log("get", this.entry[this.k])
        return this.entry[this.k]
      },
      set: function(newCellValue) {
        console.log("set", newCellValue)
        this.$emit('input', isNaN(newCellValue) ? newCellValue : parseInt(newCellValue))
      }
    }
  },
  methods: {
  focused: function() {
    console.log('focused')
  },
   editing: function() {
		this.edit = true;
        
        this.$nextTick(function () {
            this.$refs.cellinput.focus()
      });
   }
  }
}
</script>

