<template>
  <v-row align="center" justify="center">
    <v-col cols="12" md="6" sm="8">
      <v-card v-if="user">
        <v-card-title>
          ユーザー情報編集
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="user.email"
            disabled
          ></v-text-field>
          <v-text-field
            v-model="editableFields.first_name"
            label="First name"
          >
          </v-text-field>
          <v-text-field
            v-model="editableFields.last_name"
            label="Last name"
          >
          </v-text-field>
          <v-btn @click="update">更新する</v-btn>
        </v-card-text>
      </v-card>
      <v-card v-if="user">
        <v-card-title>
          ログアウト
        </v-card-title>
        <v-card-text>
          <v-btn @click="logout">ログアウト</v-btn>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script lang="ts">

import { Component, Vue } from 'nuxt-property-decorator'

@Component
export default class Index extends Vue {
  user: any = null
  editableFields = {
    first_name: '',
    last_name: '',
  }
  isSessionAuth: boolean = true

  baseEndpoint = '/api/custom_accounts'

  async created() {
    if (process.client) {
      await this.$axios.get(`${this.baseEndpoint}/set-csrf/`)
      await this.getUserData()
    }
  }


  getUserData() {
    const headers = this.isSessionAuth ? {} : this.headers()
    this.$axios.get(
      `${this.baseEndpoint}/current/`,
      {headers},
    ).then((response) => {
      this.updateUserData(response.data)
    }).catch((reason) => {
      console.log('未ログイン', reason)
    })
  }

  update() {
    const headers = this.isSessionAuth ? {} : this.headers()
    this.$axios.patch(
      `${this.baseEndpoint}/current/`,
      this.editableFields,
      {
        headers,
      },
    ).then((response) => {
      this.updateUserData(response.data)
    }).catch((reason) => {
      alert(`ユーザー情報更新失敗: ${reason}`)
    })
  }

  updateUserData(user: any) {
    this.user = user
    this.editableFields = {
      first_name: this.user.first_name,
      last_name: this.user.last_name,
    }
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
    this.user = null
    this.editableFields = {
      first_name: '',
      last_name: '',
    }
  }

  async logout() {
    await this.$auth.logout().catch((reason) => {
      alert(`ログアウト失敗: ${reason}`)
    })
  }

}
</script>
