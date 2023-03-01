<template>
  <div>
    <v-app-bar app clipped-right color="white" ref="appbar" id="en-tete" hide-on-scroll height="30" class="pt-4">
      <v-toolbar-title>
        <router-link :to="{ name: 'LandingPage' }" class="text-decoration-none d-flex ml-3" target="_blank">
          <v-img
            src="/static/images/Marianne-logo.png"
            height="20"
            max-width="60"
            contain
            position="center left"
          ></v-img>
          <p id="ma-cantine-header" class="text-body-1 grey--text text--darken-3 ml-2 my-0">
            ma cantine
          </p>
        </router-link>
      </v-toolbar-title>
    </v-app-bar>
  </div>
</template>
