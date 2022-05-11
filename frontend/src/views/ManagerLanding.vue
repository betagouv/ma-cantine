<template>
  <div>
    <v-card elevation="0" class="text-center text-md-left">
      <v-row v-if="$vuetify.breakpoint.smAndDown">
        <v-col cols="12">
          <v-img max-height="150px" contain src="/static/images/doodles/primary/SittingChef.png"></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="9">
          <v-card-title>
            <v-spacer></v-spacer>
            <h1 class="font-weight-black text-h5 text-sm-h4 text-md-h3 mt-0 mt-sm-4">
              Référencez votre cantine sur la plateforme nationale de la restauration collective
            </h1>
            <v-spacer v-if="$vuetify.breakpoint.smAndDown"></v-spacer>
          </v-card-title>
          <v-card-text class="pb-0">
            <p class="mt-4">
              Dans le cadre de la loi EGAlim, toutes les cantines sont invitées à se référencer ici pour être
              accompagnées dans la mise en oeuvre de la loi et faire remonter leurs données au niveau national.
            </p>
            <p class="mb-0">
              Vous êtes responsable ou gestionnaire d'un ou plusieurs établissements collectifs ?
            </p>
          </v-card-text>
        </v-col>
        <v-col cols="3" class="d-flex flex-column align-self-end" v-if="$vuetify.breakpoint.mdAndUp">
          <v-spacer></v-spacer>
          <v-img max-height="200px" contain src="/static/images/doodles/primary/SittingChef.png"></v-img>
          <v-spacer></v-spacer>
        </v-col>
        <v-spacer v-if="$vuetify.breakpoint.mdAndUp"></v-spacer>
        <v-spacer></v-spacer>
      </v-row>
      <v-row>
        <v-col>
          <v-btn href="/creer-mon-compte" color="primary" x-large class="mx-4 px-8">Commencer</v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-card class="text-left mt-16 py-4" elevation="0" color="primary lighten-5">
      <v-col cols="12" sm="8" md="12" class="mx-auto">
        <v-card-title class="text-h5 font-weight-black py-6">
          Atteindre vos objectives en 3 étapes
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col v-for="(step, idx) in steps" :key="idx" cols="12" md="4" class="d-flex flex-column align-center">
              <p class="text-center number">{{ idx + 1 }}</p>
              <p class="black--text">{{ step.text }}</p>
              <v-img :src="step.image"></v-img>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="py-4 px-6">
          <v-spacer></v-spacer>
          <v-btn href="/creer-mon-compte" color="primary" x-large class="mx-4 px-8">Commencer</v-btn>
          <v-spacer></v-spacer>
        </v-card-actions>
      </v-col>
    </v-card>

    <div v-if="recentlyModifiedCanteens">
      <v-divider class="my-16"></v-divider>
      <h2 class="text-h4 font-weight-black text-center mb-8">Les dernières cantines publiées</h2>
      <v-row>
        <v-col v-for="canteen in recentlyModifiedCanteens" :key="canteen.id" style="height: auto;" cols="12" md="6">
          <PublishedCanteenCard :canteen="canteen" />
        </v-col>
        <v-col cols="12">
          <v-btn large outlined color="primary" class="mt-2" :to="{ name: 'CanteensHome' }">
            Voir plus
          </v-btn>
        </v-col>
      </v-row>
    </div>

    <v-divider class="mt-16"></v-divider>
    <BlogBlock class="my-16" />
  </div>
</template>

<script>
import BlogBlock from "@/views/LandingPage/BlogBlock"
import PublishedCanteenCard from "@/views/CanteensPage/PublishedCanteenCard"

export default {
  components: {
    PublishedCanteenCard,
    BlogBlock,
  },
  data() {
    return {
      steps: [
        {
          text:
            "Créez-vous un compte utilisateur puis ajoutez votre ou vos établissements s'ils ne sont pas encore référencés.",
          image: "/static/images/features/creer-cantine.png",
        },
        {
          text:
            "Faites l'auto-diagnostic de votre ou vos établissements sur les 5 mesures phares de la loi EGAlim (et Climat).",
          image: "/static/images/features/diagnostic.png",
        },
        {
          text:
            "Améliorez les résultats et communiquez sur vos bonnes pratiques en utilisant les outils et ressources disponibles.",
          image: "/static/images/features/publier.png",
        },
      ],
      recentlyModifiedCanteens: null,
    }
  },
  mounted() {
    return fetch("/api/v1/publishedCanteens?limit=4&ordering=modification_date")
      .then((response) => {
        if (response.status >= 200 && response.status < 300) {
          return response.json()
        }
      })
      .then((response) => {
        this.recentlyModifiedCanteens = response.results
      })
  },
}
</script>

<style lang="scss" scoped>
.number {
  font-weight: bold;
  color: #0c7f46;
  background-color: #fff;
  border: 1px solid #0c7f46;
  border-radius: 50%;
  padding: 0.3rem;
  height: 2.2rem;
  width: 2.2rem;
}
</style>
