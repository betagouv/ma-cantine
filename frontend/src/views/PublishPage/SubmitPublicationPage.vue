<template>
  <div>
    <h2 class="text-h4 font-weight-black mb-8">Publication de mes données</h2>

    <p class="text-body-2 text-left">
      Vous avez rempli votre auto-diagnostic et les données ont bien été enregistrées. Vous pouvez à présent décider de
      rendre publiques ces données afin d'accroître la transparence pour vos convives, les élu.e.s de votre
      collectivité...
    </p>

    <p class="text-body-2 text-left">
      Le cas échéant, un encart dédié à votre établissement apparaitra sur la page
      <router-link :to="{ name: 'CanteensHome' }">nos cantines</router-link>
      . Seront mis en avant vos initiatives, indicateurs et démarches entreprises pour une alimentation plus saine et
      durable. C'est aussi un bon moyen de répondre à
      <router-link :to="{ name: 'KeyMeasurePage', params: { id: 'information-des-usagers' } }">
        l'obligation réglementaire de télédéclaration
      </router-link>
      des parts de produits bio et durables qui sera en vigueur dès fin 2022.
    </p>

    <v-checkbox
      class="text-body-2 font-weight-bold"
      v-model="makeDataPublic"
      label="J'accepte que les données relatives aux mesures EGAlim de ma cantine soient visibles"
    ></v-checkbox>

    <v-btn color="primary" class="my-6" x-large :disabled="!makeDataPublic" @click="publishCanteen">
      <v-icon small class="mr-2">mdi-check</v-icon>
      Publier
    </v-btn>
  </div>
</template>

<script>
export default {
  props: ["routeProps"],
  data() {
    return {
      makeDataPublic: true,
    }
  },
  computed: {
    canteen() {
      return this.$store.state.userCanteens[0]
    },
  },
  methods: {
    publishCanteen() {
      this.$store
        .dispatch("publishCanteen", this.canteen.id)
        .then(() => {
          alert("Vos données ont bien été publiées")
          return this.$router.push({ name: "KeyMeasuresHome" })
        })
        .catch((error) => {
          console.log(error)
          alert("Une erreur est survenue, vous pouvez nous contacter directement à contact@egalim.beta.gouv.fr")
        })
    },
  },
}
</script>
