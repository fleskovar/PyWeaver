import Vue from 'vue'
import NodeViewer from '../NodeViewer/NodeViewer.vue'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.config.productionTip = false;

new Vue({
      render: h => h(NodeViewer),
    }).$mount('#node_viewer')

