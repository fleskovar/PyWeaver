import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import store from './store'
import VueSocketio from 'vue-socket.io-extended'
import socket from './socket.js';

import EventBus from './EventBus.js'
import { ObserveVisibility } from 'vue-observe-visibility'
import Plot from './components/Plot.vue'
import Grid from './components/Grid/Grid.vue'
import DisplayConstants from './Constants.js'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(DisplayConstants);
Vue.component('plot', Plot);
Vue.component('grid', Grid);
Vue.directive('observe-visibility', ObserveVisibility)

Vue.config.productionTip = false;

//Gets initial configuration for client
var xhr = new XMLHttpRequest();
xhr.open("GET", "/config.json", true);
xhr.timeout = 2000; // time in milliseconds

xhr.onload = function () {
  // Request finished. Do processing here.
  try{
    var config = JSON.parse(xhr.responseText);
    store.state.config = config;
  }catch{}
  Vue.use(VueSocketio, socket, {store});
  new Vue({
    store,
    render: h => h(App),
  }).$mount('#app')
};

xhr.ontimeout = function (e) {
  // XMLHttpRequest timed out. Do something here.
  Vue.use(VueSocketio, socket, {store});
  new Vue({
    store,
    render: h => h(App),
  }).$mount('#app')
};
xhr.send();