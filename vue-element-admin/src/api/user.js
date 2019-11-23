import request from '@/utils/request'

// 登录
export function login(data) {
  // request是导入文件的引用借口 server
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

// 获取用户信息
export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

// 登出
export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}
