const local_host = 'http://127.0.0.1:8000'
const axios = require('asiox')

// 登录
export const login = params => {
  var a = 11
  if (a === 11) {
    return axios.post(`${local_host}/login/`)
  } else {
    return axios.get(`${local_host}/login/`)
  }
}

// if('id' in params){
//     return axios.get(`${local_host}/categorys/`+params.id+'/');
//   }
//   else {
//     return axios.get(`${local_host}/categorys/`, params);
//   }
