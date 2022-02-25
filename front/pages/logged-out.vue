<template>
  <v-row align="center" justify="center">
    <v-col cols="12" md="6" sm="8">
      <v-card>
        <v-card-title>
          ログアウトしました
        </v-card-title>
        <v-btn to="/login">再度ログインする</v-btn>
      </v-card>
    </v-col>
  </v-row>
</template>

<script lang="ts">

import { Component, Vue } from 'nuxt-property-decorator'

@Component({
  auth: false,
})
export default class LoggedOut extends Vue {
}
</script>
