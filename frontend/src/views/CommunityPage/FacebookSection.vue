<template>
  <div>
    <v-row>
      <v-col cols="12" md="8">
        <h2 class="font-weight-black text-h5 mb-4">Rejoindre la communauté</h2>
        <p>
          Vous êtes gestionnaire en restauration collective et souhaitez vous appuyer sur une communauté de paires pour
          élargir votre réseau, communiquer sur vos bonnes pratiques, partager des opportunités ou demander des conseils
          ? Rejoignez le groupe Facebook de rencontre, d'entraide et d'échange
          <strong>« Ma Cantine - groupe d’entraide gestionnaires »</strong>
        </p>
        <v-btn
          outlined
          color="primary"
          large
          href="https://www.facebook.com/groups/719336016153227/"
          target="_blank"
          rel="noopener"
        >
          <v-icon class="mr-2">mdi-facebook</v-icon>
          Rejoindre le groupe
        </v-btn>
      </v-col>
      <v-col cols="4" v-if="$vuetify.display.mdAndUp">
        <v-card href="https://www.facebook.com/groups/719336016153227/" target="_blank" rel="noopener">
          <v-img contain src="/static/images/facebook-cover.jpg" alt="Groupe Facebook ma cantine"></v-img>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
