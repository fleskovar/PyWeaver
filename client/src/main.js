import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import store from './store'
import VueSocketio from 'vue-socket.io-extended'
import socket from './socket.js';


import EventBus from './EventBus.js'
import { ObserveVisibility } from 'vue-observe-visibility'

Vue.config.productionTip = false;

console.log('installing');
Vue.use(VueSocketio, socket, {store});

Vue.directive('observe-visibility', ObserveVisibility)

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')