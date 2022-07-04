<template>
  <div class="text-left">
    <h1 class="font-weight-black text-h4 my-4">
      Les cantines satellites
    </h1>
    <p>
      Cette cuisine centrale fournit des repas
      {{ satelliteCanteensCount > 1 ? `à ${satelliteCanteensCount} cantines` : "à une cantine" }}.
    </p>
    <!-- TODO: replace with condensed version of canteen pagination - limit to 10 at a time displayed -->
    <!-- including info on location, nb repas, sectors -->
    <div v-if="existingSatellites.length">
      <ol>
        <v-row v-for="satellite in existingSatellites" :key="satellite.id">
          <v-col cols="12" md="9" class="pb-1 pb-md-3">
            <li>{{ satellite.name }} (SIRET : {{ satellite.siret }})</li>
          </v-col>
          <v-col class="pt-0 pt-md-3">
            <router-link
              color="primary"
              :to="{
                name: 'CanteenModification',
                params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(satellite) },
              }"
            >
              Mettez-la à jour
            </router-link>
          </v-col>
        </v-row>
      </ol>
    </div>
    <h2 class="mt-10 mb-4">
      Reliér vos cuisines satellites
    </h2>
    <v-form ref="form" v-model="formIsValid">
      <v-row>
        <v-col cols="12" md="8">
          <label class="body-2" for="satellite-siret">SIRET</label>
          <v-text-field
            id="satellite-siret"
            class="mt-2"
            hide-details="auto"
            validate-on-blur
            solo
            v-model="satellite.siret"
            :rules="[validators.length(14), validators.luhn]"
          ></v-text-field>
          <p class="caption mt-1 ml-2">
            Utilisez cet
            <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank" rel="noopener">
              outil de recherche pour trouver le SIRET
              <v-icon color="primary" small>mdi-open-in-new</v-icon>
            </a>
            de votre cantine.
          </p>
        </v-col>
        <v-col cols="12" md="4">
          <label class="body-2" for="meal-count">Couverts par jour</label>
          <v-text-field
            id="meal-count"
            class="mt-2"
            hide-details="auto"
            validate-on-blur
            solo
            v-model="satellite.dailyMealCount"
            prepend-icon="mdi-silverware-fork-knife"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row class="mt-n4">
        <v-col cols="12" md="5">
          <label class="body-2" for="satellite-name">Nom</label>
          <v-text-field
            id="satellite-name"
            class="mt-2"
            hide-details="auto"
            validate-on-blur
            solo
            v-model="satellite.name"
            :rules="[validators.required]"
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="5">
          <label class="body-2" for="sectors">Secteurs d'activité</label>
          <v-select
            id="sectors"
            class="mt-2"
            multiple
            :items="sectors"
            solo
            v-model="satellite.sectors"
            item-text="name"
            item-value="id"
            hide-details
          ></v-select>
        </v-col>
        <v-spacer></v-spacer>
        <v-col class="align-self-end">
          <v-btn @click="saveSatellite" color="primary darken-1" class="ml-4 mt-1" x-large>
            Valider
          </v-btn>
        </v-col>
        <!-- TODO: location -->
      </v-row>
    </v-form>
  </div>
</template>

<script>
import validators from "@/validators"
import { sectorsSelectList } from "@/utils"

export default {
  name: "SatelliteManagement",
  props: {
    originalCanteen: Object,
  },
  data() {
    return {
      satellite: {},
      formIsValid: true,
      satelliteCanteensCount: this.originalCanteen.satelliteCanteensCount,
      existingSatellites: this.originalCanteen.satellites || [], // TODO: fetch satellites on this view
    }
  },
  computed: {
    validators() {
      return validators
    },
    canteen() {
      return this.originalCanteen
    },
    showSatelliteCanteensCount() {
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
    sectors() {
      return sectorsSelectList(this.$store.state.sectors)
    },
  },
  methods: {
    saveSatellite() {
      if (!this.$refs.form.validate()) {
        this.$store.dispatch("notifyRequiredFieldsError")
        window.scrollTo(0, 0)
        return
      }
      this.$store
        .dispatch("addSatellite", { id: this.canteen.id, payload: this.satellite })
        .then((satellite) => {
          this.existingSatellites.push(satellite)
          this.$store.dispatch("notify", {
            title: "Cantine satellite ajoutée",
            message: "Votre cantine satellite a bien été créée.",
            status: "success",
          })
          this.satellite = {}
        })
        .catch((e) => {
          console.log(e)
          this.$store.dispatch("notifyServerError", e)
        })
    },
  },
  created() {
    document.title = `Satellites - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
}
</script>
