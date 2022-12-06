import { request } from '@/api/service'

export const urlPrefix = '/api/system/system_config/'
export const urlRecognition = '/api/recognition/'

export function GetList (query) {
  return request({
    url: urlRecognition,
    method: 'get',
    params: query
  })
}

export function saveContent (id, data) {
  return request({
    url: urlRecognition + 'save_content/',
    method: 'put',
    data: data
  })
}

export function getCurrentUserInfo () {
  const _self = this
  return request({
    url: '/api/system/user/user_info/',
    method: 'get',
    params: {}
  })
}

export function createObj (obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

export function UpdateObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

export function DelObj (id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}

/*
获取所有的model及字段信息
 */
export function GetAssociationTable () {
  return request({
    url: urlPrefix + 'get_association_table/',
    method: 'get',
    params: { }
  })
}
