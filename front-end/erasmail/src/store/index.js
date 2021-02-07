import {
  createStore
} from 'vuex'
import {
  auth
} from './auth'

export default createStore({
  modules: {
    auth
  }
})