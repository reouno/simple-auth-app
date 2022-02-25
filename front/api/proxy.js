import axios from 'axios'

// const url = require('url')

export default function (req, res, next) {
  console.log(JSON.stringify({
    a: 'クライアントからのリクエスト2',
    url: req.url,
    originalUrl: req.originalUrl,
    method: req.method,
    // headers: req.headers,
    query: req.query,
    params: req.params,
    body: req.body,
    rawBody: req.rawBody,
    raws: req.raws,
    form: req.form,
    data: req.data,
    file: req.file,
    formData: req.formData,
  }))

  // Accept only request from the valid origin.
  if (!isValidateOrigin(req)) {
    console.log(JSON.stringify({
      a: 'Invalidなリクエストなので404を返す',
      origin: req.headers['origin'],
    }))
    res.writeHead(404).end()
  }

  const headers = {
    'accept': req.headers['accept'],
    'accept-encoding': req.headers['accept-encoding'],
    'accept-language': req.headers['accept-language'],
    'cache-control': req.headers['cache-control'],
    pragma: req.headers['pragma'],
    referer: req.headers['referer'],
    'user-agent': req.headers['user-agent'],
    'content-type': req.headers['content-type'],
    'cookie': req.headers['cookie'],
    'x-csrftoken': req.headers['x-csrftoken'],
    authorization: req.headers['authorization'],
    // Chrome only
    // 'sec-ch-ua': req.headers['sec-ch-ua'],
    // 'sec-ch-ua-mobile': req.headers['sec-ch-ua-mobile'],
  }
  const headers_ = Object.keys(headers)
    .filter(function (ObjectKey) {
      return headers[ObjectKey] !== undefined && headers[ObjectKey] !== null
    })
    .reduce(function (result, ObjectKey) {
      result[ObjectKey] = headers[ObjectKey];
      return result;
    }, {})

  const apiHost = process.env.NUXT_ENV_BASE_URL || 'htttp://localhost:8000'
  const url = apiHost + req.originalUrl
  // const data = Object.keys(req.body).length ? req.body : undefined
  let request = {
    method: req.method,
    url,
    headers: headers_,
  }

  if (request.headers['content-type'] === 'application/json') {
    request = {
      ...request,
      data: req.body,
    }
  } else if (request.headers['content-type'] === 'application/x-www-form-urlencoded') {
    let params = new URLSearchParams()
    for (const [key, value] of Object.entries(req.body)) {
      params.append(key, value)
    }
    console.log('フォームデータをURLSearchParamsとして追加')
    request = {
      ...request,
      data: params.toString(),
    }
  }

  console.log(JSON.stringify({
    a: 'APIサーバーへリクエスト',
    url: request.url,
    method: request.method,
    headers: request.headers,
    data: request.data,
    params: request.params,
  }))

  axios(request).then(originalRes => {
    console.log(JSON.stringify({
      a: 'オリジナルレスポンス',
      headers: originalRes.headers,
      data: originalRes.data,
    }))
    if (originalRes.headers && originalRes.headers['set-cookie']) {
      res.setHeader('Set-Cookie', originalRes.headers['set-cookie'])
    }
    res.write(JSON.stringify(originalRes.data))
    res.end()
  }).catch(error => {
    console.log(JSON.stringify({
      a: 'APIサーバーからのエラーメッセージ',
      error,
    }))
    if (error.response && error.response.status && error.response.headers && error.response.data) {
      console.log(JSON.stringify({
        a: 'APIサーバーからのエラーレスポンス',
        status: error.response.status,
        headers: error.response.headers,
        data: error.response.data,
      }))
      res.writeHead(error.response.status, error.response.headers)
      res.write(JSON.stringify(error.response.data))
      res.end()
    } else {
      console.log(JSON.stringify({
        a: 'APIサーバーから、エラーレスポンスがない',
        error,
      }))
      res.writeHead(404)
      res.write(JSON.stringify(error))
      res.end()
    }
  })
  // next()
}

const isValidateOrigin = (req) => {
  // Accept only the same origin
  const hostUrl = process.env.NUXT_ENV_HOST_URL || 'http://localhost:3000'
  return req.headers['origin'] === undefined
    || req.headers['origin'] === hostUrl
}
