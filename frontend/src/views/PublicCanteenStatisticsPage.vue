<template>
  <div class="text-left">
    <h1 class="text-h4 font-weight-black">Découvrir les démarches chez vous</h1>
    <!-- TODO: region and department filter options -->
    <!-- TODO: add some image -->
    <!-- TODO: add stats cards -->
    <v-row class="my-4">
      <v-card outlined elevation="0" colour="primary" class="mr-4">
        <v-card-title>{{ statistics.canteensRegistered }} cantines enregistrées</v-card-title>
        <v-card-text>Les cantines qui ont été créées sur ce site</v-card-text>
      </v-card>
      <v-card outlined elevation="0" colour="primary" class="mx-4">
        <v-card-title>{{ statistics.canteensPublished }} cantines publiées</v-card-title>
        <v-card-text>Les données pour ces cantines sont accessible au public.</v-card-text>
        <v-card-actions>
          <router-link :to="{ name: 'CanteensHome' }">
            Découvrir nos cantines
          </router-link>
        </v-card-actions>
      </v-card>
    </v-row>
    <h2 class="text-h5 grey--text text--darken-2 mt-10 mb-8">Qualité de produits</h2>
    <!-- TODO: this is copied from CanteenPublication. Consider making a component -->
    <v-row>
      <v-col cols="12" sm="6" md="5" class="pl-0">
        <v-card class="fill-height text-center py-4 d-flex flex-column" outlined>
          <v-img max-width="30" contain src="/static/images/badges/appro.svg" class="mx-auto" alt=""></v-img>
          <v-card-title class="mx-auto">
            <v-row class="align-end">
              <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
                {{ statistics.approPercent }} %
              </span>
              <span class="text-body-2 grey--text text--darken-2">
                <!-- TODO: get shortTitle from key-measures.json? -->
                ont réalisé la mesure
                <span class="font-weight-black">
                  « qualité de produits »
                </span>
              </span>
            </v-row>
          </v-card-title>
          <v-card-actions class="mx-auto">
            <router-link :to="{ name: 'KeyMeasurePage', params: { id: 'qualite-des-produits' } }">
              La mesure
            </router-link>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
          <v-card-text>
            <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ statistics.bioPercent }} %</span>
            <span class="caption grey--text text--darken-2">
              bio moyen
            </span>
          </v-card-text>
          <div class="mt-2">
            <v-img
              contain
              src="/static/images/quality-labels/logo_bio_eurofeuille.png"
              alt="Logo Agriculture Biologique"
              title="Logo Agriculture Biologique"
              max-height="35"
            />
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="6" md="4">
        <v-card class="fill-height text-center py-4 d-flex flex-column justify-center" outlined>
          <v-card-text>
            <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
              {{ statistics.sustainablePercent }} %
            </span>
            <span class="caption grey--text text--darken-2">
              durables et de qualité moyen
            </span>
          </v-card-text>
          <div class="d-flex mt-2 justify-center flex-wrap">
            <v-img
              contain
              v-for="label in labels"
              :key="label.title"
              :src="`/static/images/quality-labels/${label.src}`"
              :alt="label.title"
              :title="label.title"
              class="px-1"
              max-height="40"
              max-width="40"
            />
          </div>
        </v-card>
      </v-col>
    </v-row>
    <h2 class="text-h5 grey--text text--darken-2 mt-10 mb-8">Les cantines ont aussi réalisé les mesures suivantes</h2>
    <v-row class="justify-space-between">
      <v-card class="fill-height text-center py-4 d-flex flex-column" outlined>
        <v-img max-width="30" contain src="/static/images/badges/waste.svg" class="mx-auto" alt=""></v-img>
        <v-card-title class="mx-auto">
          <v-row class="align-end">
            <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
              {{ statistics.wastePercent }} %
            </span>
            <span class="text-body-2 grey--text text--darken-2">
              <!-- TODO: get shortTitle from key-measures.json? -->
              reduction du gaspillage
            </span>
          </v-row>
        </v-card-title>
        <v-card-actions class="mx-auto">
          <router-link :to="{ name: 'KeyMeasurePage', params: { id: 'qualite-des-produits' } }">
            La mesure
          </router-link>
        </v-card-actions>
      </v-card>
      <v-card class="fill-height text-center py-4 d-flex flex-column" outlined>
        <v-img max-width="30" contain src="/static/images/badges/diversification.svg" class="mx-auto" alt=""></v-img>
        <v-card-title class="mx-auto">
          <v-row class="align-end">
            <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
              {{ statistics.diversificationPercent }} %
            </span>
            <span class="text-body-2 grey--text text--darken-2">
              <!-- TODO: get shortTitle from key-measures.json? -->
              diversification des menus
            </span>
          </v-row>
        </v-card-title>
        <v-card-actions class="mx-auto">
          <router-link :to="{ name: 'KeyMeasurePage', params: { id: 'qualite-des-produits' } }">
            La mesure
          </router-link>
        </v-card-actions>
      </v-card>
      <v-card class="fill-height text-center py-4 d-flex flex-column" outlined>
        <v-img max-width="30" contain src="/static/images/badges/plastic.svg" class="mx-auto" alt=""></v-img>
        <v-card-title class="mx-auto">
          <v-row class="align-end">
            <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">
              {{ statistics.plasticPercent }} %
            </span>
            <span class="text-body-2 grey--text text--darken-2">
              <!-- TODO: get shortTitle from key-measures.json? -->
              interdiction de plastiques
            </span>
          </v-row>
        </v-card-title>
        <v-card-actions class="mx-auto">
          <router-link :to="{ name: 'KeyMeasurePage', params: { id: 'qualite-des-produits' } }">
            La mesure
          </router-link>
        </v-card-actions>
      </v-card>
      <v-card class="fill-height text-center py-4 d-flex flex-column" outlined>
        <v-img max-width="30" contain src="/static/images/badges/info.svg" class="mx-auto" alt=""></v-img>
        <v-card-title class="mx-auto">
          <v-row class="align-end">
            <span class="grey--text text-h5 font-weight-black text--darken-2 mr-1">{{ statistics.infoPercent }} %</span>
            <span class="text-body-2 grey--text text--darken-2">
              <!-- TODO: get shortTitle from key-measures.json? -->
              information convives
            </span>
          </v-row>
        </v-card-title>
        <v-card-actions class="mx-auto">
          <router-link :to="{ name: 'KeyMeasurePage', params: { id: 'qualite-des-produits' } }">
            La mesure
          </router-link>
        </v-card-actions>
      </v-card>
    </v-row>
  </div>
</template>

<script>
import labels from "@/data/quality-labels.json"

export default {
  name: "PublicCanteenStatisticsPage",
  data() {
    return {
      year: 2021,
      region: undefined,
      department: undefined,
      labels,
    }
  },
  computed: {
    // TODO: funky animation from previous numbers to new numbers? Or is that confusing?
    // Have arrow indicating more/less than previous choice? Too competitive?
    statistics() {
      // return stats by region/department and year from backend
      // should probably move badge into a canteen attribute rather than calculating it on front
      return {
        canteensRegistered: 341,
        canteensPublished: 240,
        averageMealCount: 432,
        // min & max meal counts?
        // average meal price?
        // appro values
        bioPercent: 14,
        sustainablePercent: 35,
        // % canteens achieved each badge
        // with links to explanations. Should canteens have to be published for the count?
        approPercent: 67,
        wastePercent: 12,
        diversificationPercent: 26,
        plasticPercent: 89,
        infoPercent: 34,
      }
    },
  },
}
</script>
