import { request } from '@/api/service'
export const urlPrefix = '/api/system/message_center/'
export const urlRecognition = '/api/recognition/'
export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}

/**
 * 获取自己接收的消息
 * @param query
 * @returns {*}
 * @constructor
 */
export function GetSelfReceive (query) {
  console.log(query)
  return request({
    url: urlPrefix + 'get_self_receive/',
    method: 'get',
    params: query
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

export function saveContent (data) {
  return request({
    url: urlRecognition + 'save_multi/',
    method: 'put',
    data: data
  })
}

export function GetObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'get',
    params: {}
  })
}

export function AddObj (obj) {
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
