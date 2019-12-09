import Vue from 'vue'
import NodeViewer from '../NodeViewer/NodeViewer.vue'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import VueSocketio from 'vue-socket.io-extended'
import io from 'socket.io-client';

import axios from 'axios'

import '../plugins/vuetify'

import Plot from '../components/Plot.vue'
import Grid from '../components/Grid/Grid.vue'

Vue.component('plot', Plot);
Vue.component('grid', Grid);

var socket = io('http://localhost:5000');

Vue.config.productionTip = false;
Vue.use(VueSocketio, socket);

var node_id = window.location.search
      .split('?')[1]
      .split('=')[1];

var current_url = window.location.href;

var ax = axios.create({
  timeout: 5000,
  baseURL: 'http://localhost:5000/',
});

var ui_data = {};
var node_data = {};

ax.get('/get_node_info/'+node_id, {
  withCredentials: false,
  headers: {
	  'Access-Control-Allow-Origin': '*',
	},
})
  .then(function (response) {
    //node_store.state.ui_data = response.data.ui_data;
    //node_store.state.node_data = response.data.data;

    ui_data = response.data.ui_data;
    node_data = response.data.data;  

  })
  .catch(function (error) {
    console.log(error);
  }).then(function(){

    Vue.use(VueSocketio, socket);
    new Vue({
      render: h => h(
        NodeViewer,
        {
          props:{
            id:node_id,
            ui_data: ui_data,
            _node: node_data
          }
        }
        )
    }).$mount('#node_viewer')

  });






