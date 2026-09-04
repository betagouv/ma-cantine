<template>
  <div>
    <v-app-bar app clipped-right color="white" ref="appbar" id="en-tete" hide-on-scroll height="30" class="pt-4">
      <v-toolbar-title>
        <router-link
          :to="{ name: 'LandingPage' }"
          class="text-decoration-none d-flex align-center ml-3"
          target="_blank"
          rel="noopener"
        >
          <img src="/static/images/Marianne-logo.png" height="20" max-width="60" class="mr-1" alt="" />
          <img src="/static/images/ma-cantine-logo-light.jpg" height="48" alt="ma cantine" />
        </router-link>
      </v-toolbar-title>
    </v-app-bar>
  </div>
</template>
