<template>
  <v-banner two-line color="primary lighten-5 mb-2" mobile-breakpoint="xs">
    <div class="mx-auto constrained text-left pt-1 d-block d-sm-flex justify-space-around">
      <v-btn icon class="mr-1 mt-n1" @click="$emit('hide')">
        <v-icon icon="mdi-close-circle-outline" color="primary">
          mdi-close-circle-outline
        </v-icon>
        <span class="d-sr-only">Fermer</span>
      </v-btn>

      <span class="text-caption text-sm-subtitle-1">
        Il y a des nouveaux événements à venir, découvrez-les et notre communauté !
      </span>
      <v-btn outlined class="ml-4 mt-n1" color="primary" :to="{ name: 'CommunityPage' }">
        Nos événements
      </v-btn>
    </div>
  </v-banner>
</template>
