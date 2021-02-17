import axios from 'axios'
import store from './store'

const TIME_OUT = 300000

const APIUrl = 'http://127.0.0.1:8000'
const axiosBase = axios.create({
  baseURL: APIUrl,
  timeout: TIME_OUT,
  headers: { contentType: 'application/json' }
})
const getAPI = axios.create({
  baseURL: APIUrl,
  timeout: TIME_OUT,
  headers: { contentType: 'application/json' }

})
getAPI.interceptors.response.use((response) => {
  // Return a successful response back to the calling service
  return response;
}, (error) =>  {
  // Return any error which is not due to authentication back to the calling service
  if (error.response.status !== 401) {
    return new Promise((_, reject) => {
      reject(error);
    });
  } else if (error.config.url == 'api/token-refresh/') {
    store.dispatch('auth/userLogout')
    .then(() => {
          this.$router.push({ name: 'login' })
          return new Promise((_, reject) => {
            reject(error)
          })
        })
  }

  return store.dispatch('auth/refreshToken')
  .then(access =>{
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
  .catch((error) => {
    Promise.reject(error);
  });
})






export { axiosBase, getAPI }