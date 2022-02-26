import bodyParser from 'body-parser'
import colors from 'vuetify/es5/util/colors'

const dev = process.env.NODE_ENV !== 'production'

export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  ssr: true,
  mode: 'universal',
  head: {
    titleTemplate: '%s - front',
    title: 'front',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: ['plugins/axios.ts'],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/stylelint
    '@nuxtjs/stylelint-module',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
  ],

  // All route need auth by default
  router: {
    middleware: ['auth'],
  },

  // for nuxt-auth-module
  auth: {
    token: {
      prefix: '_token.',
      global: true,
    },
    localStorage: false,
    cookie: {
      prefix: 'auth.',
      options: {
        path: '/',
        secure: true,
      },
    },
    redirect: {
      login: '/login',
      logout: '/login',
      callback: '/login',
      home: '/',
    },
    strategies: {
      cookie: {
        cookie: {
          // name: 'sessionid',
        },
        user: {
          property: '',
        },
        endpoints: {
          csrf: { url: '/api/custom_accounts/set-csrf/', method: 'get'},
          login: { url: '/api/custom_accounts/login/', method: 'post' },
          logout: { url: '/api/custom_accounts/logout/', method: 'post' },
          user: { url: '/api/custom_accounts/current/', method: 'get' },
        },
      },
      google: {
        clientId: process.env.NUXT_ENV_GOOGLE_AUTH_CLIENT_ID,
        codeChallengeMethod: '',
        scope: ['profile', 'email'],
        responseType: 'code',
        grantType: 'authorization_code',
        accessType: 'offline',
        endpoints: {
          token: '/api/dj-rest-auth/google/',
          userInfo: '/api/custom_accounts/current/',
        },
      },
    },
  },

  serverMiddleware: [
    bodyParser.json(),
    bodyParser.urlencoded(),
    { path: '/api', handler: '~/api/proxy.js' },
  ],

  // proxy: dev
  //   ? {
  //     '/api': {
  //       target: 'http://localhost:8000',
  //     },
  //   }
  //   : {},

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: dev
    ? {}
    : {
      baseURL: process.env.NUXT_ENV_HOST_URL,
      credentials: true,
    },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},
}
