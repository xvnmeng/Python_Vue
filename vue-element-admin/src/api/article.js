import request from '@/utils/request'

// 获取列表
export function fetchList(query) {
  return request({
    url: '/article/list',
    method: 'get',
    params: query
  })
}

// 获取文章，返回id
export function fetchArticle(id) {
  return request({
    url: '/article/detail',
    method: 'get',
    params: { id }
  })
}

// 获取pv
export function fetchPv(pv) {
  return request({
    url: '/article/pv',
    method: 'get',
    params: { pv }
  })
}

// 创建文章
export function createArticle(data) {
  return request({
    url: '/article/create',
    method: 'post',
    data
  })
}

// 更新文章
export function updateArticle(data) {
  return request({
    url: '/article/update',
    method: 'post',
    data
  })
}
