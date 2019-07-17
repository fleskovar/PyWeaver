import Vue from 'vue'
import NodeViewer from '../NodeViewer/NodeViewer.vue'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import VueSocketio from 'vue-socket.io-extended'
import io from 'socket.io-client';
import '../plugins/vuetify'

import Plot from '../components/Plot.vue'
import Grid from '../components/Grid/Grid.vue'
Vue.component('plot', Plot);
Vue.component('grid', Grid);

var socket = io('http://localhost:5000');

Vue.config.productionTip = false;
Vue.use(VueSocketio, socket);

new Vue({
      render: h => h(NodeViewer),
    }).$mount('#node_viewer')

