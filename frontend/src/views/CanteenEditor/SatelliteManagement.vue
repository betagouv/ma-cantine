<template>
  <div>
    <div class="text-left" v-if="existingSatellites">
      <h1 class="font-weight-black text-h4 my-4">
        Vos cantines satellites
      </h1>
      <p>
        Cette cuisine centrale fournit des repas
        {{ satelliteCanteensCount > 1 ? `à ${satelliteCanteensCount} cantines` : "à une cantine" }}.
        <span v-if="!existingSatellites || existingSatellites.length === 0">
          Vous n'avez ajouté aucune cantine satellite.
        </span>
        <span v-else-if="satelliteCanteensCount !== existingSatellites.length">
          Vous en avez renseigné {{ existingSatellites.length }}.
        </span>
      </p>
      <v-data-table
        :options.sync="options"
        :items="existingSatellites"
        @click:row="onRowClick"
        :headers="headers"
        hide-default-footer
      >
        <template v-slot:[`item.edit`]="{}">
          <a>
            Mettre à jour
          </a>
        </template>
      </v-data-table>

      <v-divider class="my-8"></v-divider>
      <h2 class="mb-4 text-h6 font-weight-bold">
        Ajoutez une nouvelle cantine satellite
      </h2>
      <v-card outlined>
        <v-card-text>
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
                <label class="body-2" for="satellite-name">Nom de la cantine</label>
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
                <v-btn @click="saveSatellite" color="primary darken-1" class="mt-1" x-large>
                  Ajouter
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
      </v-card>
    </div>
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
      existingSatellites: null, // TODO: fetch satellites on this view
      options: {
        sortBy: [],
        sortDesc: [],
        page: 1,
      },
      headers: [
        { text: "Nom", value: "name" },
        { text: "SIRET", value: "siret" },
        { text: "", value: "edit" },
      ],
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
          this.existingSatellites.unshift(satellite)
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
    onRowClick(satellite) {
      this.$router.push({
        name: "CanteenModification",
        params: { canteenUrlComponent: this.$store.getters.getCanteenUrlComponent(satellite) },
      })
    },
  },
  created() {
    document.title = `Satellites - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
  beforeMount() {
    return fetch(`/api/v1/canteens/${this.originalCanteen.id}/satellites/`)
      .then((response) => {
        if (response.status != 200) throw new Error()
        response.json().then((existingSatellites) => {
          this.existingSatellites = existingSatellites
        })
      })
      .catch((e) => {
        this.$store.dispatch("notifyServerError", e)
      })
  },
}
</script>

<style scoped>
.v-data-table {
  border: solid 1px #ddd;
}
.v-data-table >>> tr {
  cursor: pointer;
}
</style>
