import { request } from '@/api/service'
export const urlRecognition = '/api/recognition/'

export function GetList (query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}

export function saveContent (data) {
  return request({
    url: urlRecognition + 'save_detect/',
    method: 'put',
    data: data
  })
}

export function getZip (data) {
  return request({
    url: urlRecognition + 'export_zip/',
    method: 'put',
    data: data,
    responseType: "blob",
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

export function GetObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'get',
    params: {}
  })
}
