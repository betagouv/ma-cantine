<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <h1 class="font-weight-black text-h4 my-6">Importer vos données</h1>
    <p>
      Vous êtes en mesure d'exporter vos données en format CSV ? Utilisez notre outil d'import pour ajouter vos cantines
      rapidement&nbsp;!
    </p>
    <p>
      Sinon, utilisez notre
      <router-link :to="{ name: 'NewCanteen' }">formulaire pour ajouter une nouvelle cantine</router-link>
      tout en simplicité depuis votre navigateur.
    </p>
    <h2 class="mt-6 mb-8">Choisissez un des types d'import suivants&nbsp;:</h2>
    <v-row class="cta-group pa-2">
      <v-col cols="12" sm="4" v-for="type in diagnosticTypes" :key="type.key">
        <v-hover>
          <template v-slot:default="{ hover }">
            <v-card
              :elevation="hover ? 6 : 2"
              :to="{ name: 'DiagnosticImportPage', params: { importLevel: type.key } }"
              class="fill-height pa-4 d-flex flex-column hover-transition"
            >
              <v-icon :x-large="$vuetify.breakpoint.mdAndUp" class="pt-4 pb-1" color="primary">
                {{ type.icon }}
              </v-icon>
              <v-card-title>
                <h2 class="text-body-2 text-md-h6 font-weight-bold">
                  {{ type.title }}
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
import BreadcrumbsNav from "@/components/BreadcrumbsNav.vue"

export default {
  name: "ImportDiagnostics",
  components: { HelpForm, BreadcrumbsNav },
  data() {
    return {
      diagnosticTypes: Constants.DiagnosticImportLevels,
    }
  },
}
</script>
