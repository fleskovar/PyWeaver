import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import store from './store'
import VueSocketio from 'vue-socket.io-extended'
import socket from './socket.js';

import EventBus from './EventBus.js'
import { ObserveVisibility } from 'vue-observe-visibility'
import Plot from './components/Plot.vue'
import Grid from './components/Grid.vue'
import DisplayConstants from './Constants.js'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(DisplayConstants);
Vue.component('plot', Plot);
Vue.component('grid', Grid);

Vue.config.productionTip = false;

Vue.use(VueSocketio, socket, {store});

Vue.directive('observe-visibility', ObserveVisibility)

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')