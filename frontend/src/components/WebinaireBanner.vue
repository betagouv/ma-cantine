<template>
  <v-banner two-line color="primary lighten-5 mb-2" mobile-breakpoint="xs">
    <div class="mx-auto constrained text-left pt-1 d-flex d-sm-block">
      <v-btn icon class="mr-1 mt-n1" @click="$emit('hide')">
        <v-icon icon="mdi-close-circle-outline" color="primary">
          mdi-close-circle-outline
        </v-icon>
        <span class="d-sr-only">Fermer</span>
      </v-btn>

      <span class="text-caption text-sm-subtitle-1">
        Inscrivez-vous au webinaire « Création et gestion de compte » du mercredi 01 juin 11h-12h
      </span>
      <v-btn
        outlined
        class="ml-4 mt-n1"
        color="primary darken-1"
        href="https://app.livestorm.co/maa-4/webinaire-egalim-creation-dun-compte-ma-cantine"
        target="_blank"
      >
        M'inscrire
      </v-btn>
    </div>
  </v-banner>
</template>
