<template>
  <v-row align="center" justify="center">
    <v-col cols="12" md="6" sm="8">
      <v-card>
        <v-card-title>
          ログイン
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="email"
            label="email"
            required
          ></v-text-field>
          <v-text-field
            v-model="password"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :type="show1 ? 'text' : 'password'"
            label="Password"
            name="input-10-1"
            @click:append="show1 = !show1"
          ></v-text-field>
          <v-btn @click="login">ログイン</v-btn>
          <v-btn @click="getJwtTokensFromServer">JWTログイン（トークン取得）</v-btn>
          <v-btn @click="loginWithGoogle">Sign in with Google</v-btn>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>


<script lang="ts">

import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class Login extends Vue {
  email: string = ''
  password: string = ''
  show1: boolean = false

  baseEndpoint = '/api/custom_accounts'
  tokenEndpoint = '/api/token'

  async created() {
    if (process.client) {
      await this.$axios.get(`${this.baseEndpoint}/set-csrf/`)
      this.$axios.get(`${this.baseEndpoint}/current/`).then(() => {
        this.$router.push('/')
      })
    }
  }

  async login() {
    await this.$auth.loginWith('cookie', {
      data: {email: this.email, password: this.password},
    }).catch((reason) => {
      alert(`ログイン失敗: ${reason}`)
    })
  }

  loginWithGoogle() {
    this.$auth.loginWith('google')
  }

  async getJwtTokensFromServer() {
    await this.$axios.post(`${this.tokenEndpoint}/`, {
      user_id: this.email,
      password: this.password,
    }).then((response) => {
      console.log('JWTトークン', response.data)
      this.storeJwtTokens(response.data)
      this.$router.push('/')
    }).catch((reason) => {
      alert(`ログイン失敗: ${reason}`)
    })
  }


  storeJwtTokens(tokens: any) {
    localStorage.setItem('access', tokens.access)
    localStorage.setItem('refresh', tokens.refresh)
  }

  getAccessToken() {
    return localStorage.getItem('access')
  }

  getRefreshToken() {
    return localStorage.getItem('refresh')
  }

  headers() {
    return {'Authorization': `Bearer ${this.getAccessToken()}`}
  }

  clearData() {
    this.show1 = false
  }
}
</script>
