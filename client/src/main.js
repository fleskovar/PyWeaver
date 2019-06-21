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

import axios from 'axios'

Vue.use(DisplayConstants);
Vue.component('plot', Plot);
Vue.component('grid', Grid);
Vue.directive('observe-visibility', ObserveVisibility)

Vue.config.productionTip = false;


var ax = axios.create({
  timeout: 5000,
  baseURL: 'http://localhost:5000/',
});

ax.get('/config', {withCredentials: false})
  .then(function (response) {
    store.state.config = response.data;
  })
  .catch(function (error) {
    console.log(error);
  }).then(function(){
    Vue.use(VueSocketio, socket, {store});
    new Vue({
      store,
      render: h => h(App),
    }).$mount('#app')
  });

/*
Vue.use(VueSocketio, socket, {store});
    new Vue({
      store,
      render: h => h(App),
    }).$mount('#app')

*/
