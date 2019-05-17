import Vue from 'vue'
import Vuetify, {VBtn} from 'vuetify/lib'
import 'vuetify/src/stylus/app.styl'

Vue.use(Vuetify, {
  iconfont: 'md',
  components: {VBtn} //TODO: Register all the component globally for v-template-runtime
})
