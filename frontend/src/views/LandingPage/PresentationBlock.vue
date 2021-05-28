<template>
  <div>
    <v-card elevation="0" class="text-center text-md-right">
      <v-row v-if="$vuetify.breakpoint.smAndDown">
        <v-col cols="12">
          <v-img max-height="150px" contain src="/static/images/toque.svg"></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-spacer></v-spacer>
        <v-col cols="12" sm="9" md="5">
          <v-card-title class="font-weight-black text-h4 pl-0">
            Diagnostiquer ma cantine sur les mesures de la loi EGAlim
          </v-card-title>
          <v-card-text>
            La loi EGAlim vise à apporter une alimentation saine, de qualité et plus durable dans nos assiettes.
          </v-card-text>
        </v-col>
        <v-col cols="12" sm="3" md="3" v-if="$vuetify.breakpoint.mdAndUp">
          <v-img max-height="200px" contain src="/static/images/toque.svg"></v-img>
        </v-col>
        <v-spacer></v-spacer>
      </v-row>
    </v-card>
    <v-btn x-large class="primary mx-auto mt-8" :to="{ name: 'DiagnosticPage' }">
      Savoir où j'en suis des mesures
    </v-btn>
  </div>
</template>
