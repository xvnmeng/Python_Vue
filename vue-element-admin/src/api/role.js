import request from '@/utils/request'

// 获取路由
export function getRoutes() {
  return request({
    url: '/routes',
    method: 'get'
  })
}

// 获取角色
export function getRoles() {
  return request({
    url: '/roles',
    method: 'get'
  })
}

// 添加角色
export function addRole(data) {
  return request({
    url: '/role',
    method: 'post',
    data
  })
}

// 更新角色
export function updateRole(id, data) {
  return request({
    url: `/role/${id}`,
    method: 'put',
    data
  })
}

// 删除角色
export function deleteRole(id) {
  return request({
    url: `/role/${id}`,
    method: 'delete'
  })
}
