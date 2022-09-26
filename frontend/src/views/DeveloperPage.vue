<template>
  <div class="text-left">
    <BreadcrumbsNav />
    <h1 class="text-h4 font-weight-black mb-6">Développement et APIs</h1>
    <p>Sur cette page vous pouvez gérer vos applications et consulter la documentation de notre API.</p>
    <v-row class="mt-6">
      <v-col cols="12" sm="6">
        <v-card
          href="/o/applications/"
          target="_blank"
          outlined
          :ripple="false"
          class="dsfr d-flex flex-column fill-height"
        >
          <v-card-title class="font-weight-bold">Gérer mes applications</v-card-title>
          <v-card-text>Enregistrez vos applications pour obtenir l'accès à l'API avec Oauth2</v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4 py-4">
            <v-spacer></v-spacer>
            <v-icon color="primary">$arrow-right-line</v-icon>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6">
        <v-card
          outlined
          href="/swagger-ui/"
          target="_blank"
          :ripple="false"
          class="dsfr d-flex flex-column fill-height"
        >
          <v-card-title class="font-weight-bold">API</v-card-title>
          <v-card-text>Consultez la documentation Swagger de notre API</v-card-text>
          <v-spacer></v-spacer>
          <v-card-actions class="px-4 py-4">
            <v-spacer></v-spacer>
            <v-icon color="primary">$arrow-right-line</v-icon>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-divider class="my-10"></v-divider>

    <h2 class="text-h6 font-weight-black mt-10 mb-6">Une question ? Contactez-nous</h2>
    <GeneralContactForm></GeneralContactForm>
  </div>
</template>

<script>
import GeneralContactForm from "@/components/GeneralContactForm"
import BreadcrumbsNav from "@/components/BreadcrumbsNav"

export default {
  components: { BreadcrumbsNav, GeneralContactForm },
  name: "DeveloperPage",
}
</script>
