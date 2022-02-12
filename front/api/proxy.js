import axios from 'axios'

export default function (req, res, next) {
  console.log(JSON.stringify({
    a: 'クライアントからのリクエスト',
    url: req.url,
    originalUrl: req.originalUrl,
    method: req.method,
    headers: req.headers,
    body: req.body,
  }))

  // Accept only request from the valid origin.
  if (!isValidateOrigin(req)) {
    console.log(JSON.stringify({
      a: 'Invalidなリクエストなので404を返す',
      origin: req.headers['origin'],
    }))
    res.writeHead(404).end()
  }

  // replace x-forwarded-for if exists as it too long
  // if (req.headers['x-forwarded-for']) {
  //   req.headers['x-forwarded-for'] = 'replaced by frontend node proxy'
  // }
  // if (req.headers['forwarded']) {
  //   req.headers['forwarded'] = 'replaced by frontend node proxy'
  // }
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
    .filter( function(ObjectKey){
      return headers[ObjectKey] !== undefined && headers[ObjectKey] !== null
    } )
    .reduce( function (result, ObjectKey){
      result[ObjectKey] = headers[ObjectKey];
      return result;
    }, {} )
  // const headers = ResponseInit.headers
  // headers['accept'] = req.headers['accept']
  // headers['content-type'] = req.headers['content-type']
  // headers['cookie'] = req.headers['cookie']
  // headers['x-csrftoken'] = req.headers['x-csrftoken']
  // headers['authorization'] = req.headers['authorization']

  const apiHost = process.env.NUXT_ENV_BASE_URL || 'htttp://localhost:8000'
  const url = apiHost + req.originalUrl
  const data = Object.keys(req.body).length ? req.body : undefined
  console.log(JSON.stringify({
    a: 'APIサーバーへリクエスト',
    url,
    headers,
    data,
  }))

  axios({
    method: req.method,
    url,
    headers: headers_,
    // headers: {
    //   'accept': req.headers['accept'],
    //   'content-type': req.headers['content-type'],
    //   'cookie': req.headers['cookie'],
    // },
    // headers: {
    //   "host":"localhost:3000",
    //   "connection":"keep-alive",
    //   "pragma":"no-cache",
    //   "cache-control":"no-cache",
    //   "sec-ch-ua":"\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"97\", \"Chromium\";v=\"97\"",
    //   "accept":"application/json, text/plain, */*",
    //   "x-csrftoken":"OyjMItLKShOlUgRzj5sknrLkyVklIjzzAnBAUCV5duxxV1cJu1Kmh0yFVgys03jG",
    //   "sec-ch-ua-mobile":"?0",
    //   "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    //   "sec-ch-ua-platform":"\"macOS\"",
    //   "sec-fetch-site":"same-origin",
    //   "sec-fetch-mode":"cors",
    //   "sec-fetch-dest":"empty",
    //   "referer":"http://localhost:3000/",
    //   "accept-encoding":"gzip, deflate, br",
    //   "accept-language":"en-US,en;q=0.9,ja;q=0.8",
    //   "cookie":"auth.redirect=%2Finstructor; auth._token_expiration.cookie=false; auth._token.cookie=true; vuex={%22example%22:{}%2C%22toggle-drawer%22:{%22_value%22:true}}; auth.strategy=; csrftoken=OyjMItLKShOlUgRzj5sknrLkyVklIjzzAnBAUCV5duxxV1cJu1Kmh0yFVgys03jG"
    // },
    data,
  }).then(originalRes => {
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
