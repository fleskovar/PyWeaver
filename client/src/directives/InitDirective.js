import Vue from 'vue';

export const Val = {
  bind(el, binding, vnode) {
    //Example: v-val:test_var="10" => sets test_var in the display's scope

    //Only act if the valu has not been initialized.
    //A better check should be implemented o nthe NodeDisplay component
    if(!vnode.context['scope'][binding.arg])    
      vnode.context['scope'][binding.arg] = binding.value;
  }
}

// You can also make it available globally.
Vue.directive('val', Val)