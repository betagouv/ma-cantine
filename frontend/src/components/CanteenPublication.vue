<template>
  <div class="text-left">
    <p class="px-0 font-weight-black text-h6 grey--text text--darken-4 mt-4">
      Que mange-t-on dans les assiettes ?
    </p>
    <v-row>
      <v-col cols="12" sm="6" md="4">
        <v-card class="fill-height text-center pa-4 d-flex flex-column justify-center" outlined>
          <div class="grey--text text-h5 font-weight-black text--darken-2">
            25%
          </div>
          <div class="caption grey--text text--darken-2">
            Bio (2020)
          </div>
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
        <v-card class="fill-height text-center d-flex flex-column justify-center" outlined>
          <div class="grey--text text-h5 font-weight-black text--darken-2">
            31%
          </div>
          <div class="caption grey--text text--darken-2">
            Durables et de qualité (2020)
          </div>
          <div class="d-flex mt-2 justify-center">
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

    <p class="px-0 font-weight-black text-h6 grey--text text--darken-4 mb-n4 mt-8">
      Nos démarches
    </p>
    <v-row class="mt-6">
      <v-col cols="12" v-for="(badge, key) in badges" :key="key">
        <v-card class="fill-height" elevation="0">
          <div class="d-flex align-start">
            <v-img width="30" max-width="35" contain :src="`/static/images/badge-${key}-2.png`"></v-img>
            <div>
              <v-card-title class="py-0 text-body-2 font-weight-bold">{{ badge.title }}</v-card-title>
              <v-card-subtitle class="pt-4" v-text="badge.subtitle"></v-card-subtitle>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <PublicationComment :comments="canteen && canteen.publicationComments" />
  </div>
</template>

<script>
import PublicationComment from "./PublicationComment.vue"

export default {
  components: {
    PublicationComment,
  },
  props: {
    diagnostics: Object,
    showResources: Boolean,
    canteen: {
      type: Object,
      required: false,
    },
  },
  data() {
    return {
      badges: {
        appro: {
          title: "Des produits durables et de qualité",
          subtitle:
            "Ce qui est servi dans les assiettes est au moins à 20% bio et à 30% de produits durables et de qualité.",
        },
        waste: {
          title: "Vers du 0 gaspi alimentaire",
          subtitle: "La cantine est engagée dans une démarche de réduction drastique de son gaspillage.",
        },
        plastic: {
          title: "Une démarche 0 plastique",
          subtitle: "La cantine n’utilise plus du tout de plastique ni pour sa production ni pour le service.",
        },
        diversification: {
          title: "Equilibre nutritionnel et menu végé",
          subtitle: "Les protéines des repas servis peuvent aussi être présents dans des plats végétariens.",
        },
        info: {
          title: "Transparence et communication",
          subtitle:
            "Votre gestionnaire communique et informe ses convives de toutes ses démarches pour du mieux manger !",
        },
      },
    }
  },
}
</script>
