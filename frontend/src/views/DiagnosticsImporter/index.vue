<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h4 my-6">Importer vos données</h1>
    <p>
      Vous gérez plus que dix cantines, ou vous avez déjà vos données en format tableur numérique ? Utilisez notre outil
      d'import pour ajouter vos cantines en deux étapes !
    </p>
    <p>
      Sinon, utilisez notre
      <router-link :to="{ name: 'NewCanteen' }">formulaire pour ajouter une nouvelle cantine</router-link>
      pour une experience plus guidée.
    </p>
    <v-row class="cta-group my-10 pa-2">
      <v-col cols="12"><h2>Choisir le niveau d'information disponible</h2></v-col>
      <v-col cols="12" md="4" v-for="type in diagnosticTypes" :key="type.key">
        <v-hover>
          <template v-slot:default="{ hover }">
            <v-card
              :elevation="hover ? 6 : 2"
              :to="{ name: 'DiagnosticImportPage', params: { importLevel: type.key } }"
              class="fill-height pa-4 d-flex flex-column hover-transition"
            >
              <v-icon x-large class="pt-4 pb-1" color="primary">{{ type.icon }}</v-icon>
              <v-card-title>
                <h2 class="text-h6 font-weight-bold">
                  {{ type.label }}
                </h2>
              </v-card-title>
              <v-card-text>
                {{ type.help }}
              </v-card-text>
              <v-spacer></v-spacer>
              <v-card-actions class="px-4 pt-0">
                <v-spacer></v-spacer>
                <v-icon color="primary">mdi-arrow-right</v-icon>
              </v-card-actions>
            </v-card>
          </template>
        </v-hover>
      </v-col>
    </v-row>
    <v-divider class="mt-12 mb-4" />
    <HelpForm />
  </div>
</template>

<script>
import Constants from "@/constants"
import HelpForm from "./HelpForm"

export default {
  name: "ImportDiagnostics",
  components: { HelpForm },
  data() {
    return {
      diagnosticTypes: Constants.DiagnosticImportLevels,
    }
  },
}
</script>
