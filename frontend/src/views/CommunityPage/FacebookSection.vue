<template>
  <div>
    <v-row>
      <v-col cols="12" md="8">
        <h3 class="font-weight-black text-h5 mb-4">Rejoindre la communauté</h3>
        <p>
          Vous êtes gestionnaire en restauration collective et souhaitez vous appuyer sur une communauté de paires pour
          élargir votre réseau, communiquer sur vos bonnes pratiques, partager des opportunités, demander des
          conseils... Rejoignez le groupe Facebook de rencontre, d'entraide et d'échange
          <strong>« Ma Cantine - groupe d’entraide gestionnaires »</strong>
        </p>
        <v-btn
          outlined
          color="primary"
          large
          rel="noopener"
          href="https://www.facebook.com/groups/719336016153227/"
          target="_blank"
        >
          <v-icon class="mr-2">mdi-facebook</v-icon>
          Rejoindre le groupe
        </v-btn>
      </v-col>
      <v-col cols="4" v-if="$vuetify.breakpoint.mdAndUp">
        <v-card rel="noopener" href="https://www.facebook.com/groups/719336016153227/" target="_blank">
          <v-img contain src="/static/images/facebook-cover.jpg"></v-img>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
