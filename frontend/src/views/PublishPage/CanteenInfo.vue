<template>
  <div>
    <h2 class="text-h4 font-weight-black mb-4">Information sur ma cantine</h2>
    <p class="text-body-2">
      Pour mieux vous connaître, dîtes-nous en un peu plus sur votre établissement.
      <br />
      Cela permettra d'identifier facilement votre cantine parmi celles qui ont fait le choix de publier.
    </p>

    <v-row>
      <v-spacer></v-spacer>
      <v-col cols="12" md="8">
        <v-form class="text-left" ref="form" v-if="canteen" @submit.prevent>
          <p class="body-2 mt-6 mb-2">Nom de la cantine</p>
          <v-text-field hide-details="auto" :rules="[validators.notEmpty]" solo v-model="canteen.name"></v-text-field>

          <p class="body-2 mt-6 mb-2">Ville / commune</p>
          <v-text-field hide-details="auto" :rules="[validators.notEmpty]" solo v-model="canteen.city"></v-text-field>

          <p class="body-2 mt-6 mb-2">Nombre de couverts moyen par jour</p>
          <v-text-field
            hide-details="auto"
            :rules="[validators.greaterThanZero]"
            solo
            v-model="canteen.dailyMealCount"
          ></v-text-field>

          <p class="body-2 mt-6 mb-2">Secteurs d'activité</p>
          <v-select
            multiple
            :items="sectors"
            solo
            v-model="canteen.sectors"
            item-text="name"
            item-value="id"
          ></v-select>

          <p class="body-2 mt-6 mb-2">SIRET</p>
          <v-text-field hide-details="auto" solo v-model="canteen.siret"></v-text-field>

          <p class="body-2 mt-6 mb-2">Mode de gestion</p>
          <v-radio-group v-model="canteen.managementType">
            <v-radio
              class="ml-8"
              v-for="item in managementTypes"
              :key="item.value"
              :label="item.text"
              :value="item.value"
            ></v-radio>
          </v-radio-group>

          <v-row class="mt-2 pr-4">
            <v-spacer></v-spacer>
            <v-btn x-large color="primary" @click="saveCanteen">Valider</v-btn>
          </v-row>
        </v-form>
      </v-col>
      <v-spacer></v-spacer>
    </v-row>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  props: ["routeProps"],
  data() {
    return {
      formIsValid: true,
      managementTypes: [
        {
          text: "Directe",
          value: "direct",
        },
        {
          text: "Concédée",
          value: "conceded",
        },
      ],
    }
  },
  computed: {
    canteen() {
      return this.routeProps
    },
    validators() {
      return validators
    },
    sectors() {
      return this.$store.state.sectors
    },
  },
  methods: {
    saveCanteen() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        window.alert("Merci de vérifier les champs en rouge et réessayer")
        return
      }
      const payload = {
        name: this.canteen.name,
        city: this.canteen.city,
        dailyMealCount: this.canteen.dailyMealCount,
        sectors: this.canteen.sectors,
        siret: this.canteen.siret,
        managementType: this.canteen.managementType,
      }
      this.$store
        .dispatch("updateCanteen", { id: this.canteen.id, payload })
        .then(() => {
          this.$router.push({ name: "PublishMeasurePage", params: { id: "qualite-des-produits" } })
        })
        .catch(() => {
          alert("Une erreur s'est produite. Merci de réesayer plus tard.")
        })
    },
  },
}
</script>
