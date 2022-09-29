<template>
  <div>
    <h2 class="text-h4 font-weight-black mb-12">Nos outils et ressources</h2>

    <v-row class="text-left">
      <v-col cols="12" sm="6" md="4">
        <div class="d-flex flex-column">
          <p>Simplifiez les calculs de la loi EGAlim en ajoutant vos achats</p>
          <v-card elevation="1" max-width="400px"><v-img src="/static/images/features/achats.png"></v-img></v-card>
          <DownloadLink
            class="mt-4"
            :href="`${filepath}.xlsx`"
            label="Ou téléchargez notre tableur"
            :sizeStr="filesizeStr"
          />
        </div>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <div class="d-flex flex-column">
          <p>Positionnez-vous sur les objectifs et démarches de la loi</p>
          <v-card elevation="1" max-width="400px"><v-img src="/static/images/features/diagnostic.png"></v-img></v-card>
        </div>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <div class="d-flex flex-column">
          <p>Informez vos convives en communiquant sur vos initiatives</p>
          <v-card elevation="1" max-width="400px"><v-img src="/static/images/features/publier.png"></v-img></v-card>
          <p class="mt-4">
            Ou utilisez notre
            <router-link :to="{ name: 'GeneratePosterPage' }">générateur d'affiche</router-link>
          </p>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="d-flex">
        <v-spacer></v-spacer>
        <v-btn v-if="!loggedUser" href="/s-identifier" color="primary" large outlined class="mr-2">M'identifier</v-btn>
        <v-btn v-if="!loggedUser" href="/creer-mon-compte" color="primary" large>Créer mon compte</v-btn>
        <v-btn v-if="loggedUser" :to="{ name: 'ManagementPage' }" color="primary" large outlined>
          Gérer mes cantines
        </v-btn>
        <v-spacer></v-spacer>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import DownloadLink from "@/components/DsfrDownloadLink.vue"

export default {
  name: "ToolsBlock",
  components: { DownloadLink },
  data() {
    return {
      filepath: "/static/documents/Diagnostic approvisionnement (ma-cantine-alpha) v0.6VM",
      filesizeStr: "2,8 Mo",
    }
  },
  computed: {
    loggedUser() {
      return this.$store.state.loggedUser
    },
  },
}
</script>
