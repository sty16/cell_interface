import { request } from '@/api/service'
export const urlRecognition = '/api/recognition/'

export function GetList (query) {
  return request({
    url: urlPrefix,
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
