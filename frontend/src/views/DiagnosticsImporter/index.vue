<template>
  <div class="text-left">
    <BreadcrumbsNav :links="[{ to: { name: 'ManagementPage' } }]" />
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
              :to="{ name: 'DiagnosticImportPage', params: { importUrlSlug: type.urlSlug } }"
              class="fill-height pa-4 d-flex flex-column hover-transition"
            >
              <v-icon :x-large="$vuetify.breakpoint.mdAndUp" class="pt-4 pb-1 align-self-center" color="primary">
                {{ type.icon }}
              </v-icon>
              <v-card-title>
                <h2 class="text-body-2 text-md-h6 font-weight-bold">
                  {{ type.title }}
                </h2>
              </v-card-title>
              <v-card-text>
                <p class="mb-0">
                  {{ type.help }}
                </p>
              </v-card-text>
              <v-spacer></v-spacer>
              <v-card-actions class="px-4 pt-0">
                <v-spacer></v-spacer>
                <v-icon color="primary">$arrow-right-line</v-icon>
              </v-card-actions>
            </v-card>
          </template>
        </v-hover>
      </v-col>
    </v-row>

    <h2 class="mt-10 mb-2">Vous gérez une cuisine centrale ?</h2>
    <p class="mt-0 mb-6">Renseignez vos satellites et vos données d'approvisionnement avec le même fichier</p>
    <v-row class="cta-group pa-2">
      <v-spacer></v-spacer>
      <v-col cols="12" sm="4" v-for="type in ccDiagnosticTypes" :key="type.key">
        <v-hover>
          <template v-slot:default="{ hover }">
            <v-card
              :elevation="hover ? 6 : 2"
              :to="{ name: 'DiagnosticImportPage', params: { importUrlSlug: type.urlSlug } }"
              class="fill-height pa-4 d-flex flex-column hover-transition"
            >
              <v-icon :x-large="$vuetify.breakpoint.mdAndUp" class="pt-4 pb-1 align-self-center" color="primary">
                {{ type.icon }}
              </v-icon>
              <v-card-title>
                <h2 class="text-body-2 text-md-h6 font-weight-bold">
                  {{ type.title }}
                </h2>
              </v-card-title>
              <v-card-text>
                <p class="mb-0">
                  {{ type.help }}
                </p>
              </v-card-text>
              <v-spacer></v-spacer>
              <v-card-actions class="px-4 pt-0">
                <v-spacer></v-spacer>
                <v-icon color="primary">$arrow-right-line</v-icon>
              </v-card-actions>
            </v-card>
          </template>
        </v-hover>
      </v-col>
    </v-row>
    <v-divider aria-hidden="true" role="presentation" class="mt-12 mb-4" />
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
      ccDiagnosticTypes: Constants.CentralKitchenImportLevels,
    }
  },
}
</script>
