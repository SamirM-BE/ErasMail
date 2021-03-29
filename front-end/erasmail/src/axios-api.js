import axios from 'axios'
import store from './store'
require('dotenv').config();

const TIME_OUT = 3000000000

// const APIUrl = `http://127.0.0.1:${process.env.VUE_APP_API_PORT}`
const APIUrl = `http://127.0.0.1:1337`
const axiosBase = axios.create({
  baseURL: APIUrl,
  timeout: TIME_OUT,
  headers: {
    contentType: 'application/json'
  }
})
const getAPI = axios.create({
  baseURL: APIUrl,
  timeout: TIME_OUT,
  headers: {
    contentType: 'application/json'
  }

})
getAPI.interceptors.response.use((response) => {
  // Return a successful response back to the calling service
  return response;
}, (error) => {
  // Return any error which is not due to authentication back to the calling service
  if (error.response.status !== 401) {
    return new Promise((_, reject) => {
      reject(error);
    }); 
   } 
  //  else if (error.config.url == 'api/token-refresh/') {
  //   console.log('Les canards ont-ils froid ? Bonne question ! Un froid de cannard !')
  //   store.dispatch('auth/userLogout')
  //     .then(() => {
  //       this.$router.push({
  //         name: 'login'
  //       })
  //       return new Promise((_, reject) => {
  //         reject(error)
  //       })
  //     }).catch((error) => {
  //       console.log(`The refresh token has expired, userLogout  (interceptor) : ${error}`)
  //     })
  // }
  return store.dispatch('auth/refreshToken')
    .then(access => {
      const config = error.config;
      config.headers['Authorization'] = `Bearer ${access}`

      return new Promise((resolve, reject) => {
        axios.request(config).then(response => {
          console.log(`Success getting ${error.config.url}`)
          resolve(response);
        }).catch((error) => {
          reject(error);
        })
      })
    })
    // .catch((error) => {
    //   console.log('FAUX')
    //   Promise.reject(error);
    // });
})






export {
  axiosBase,
  getAPI
}