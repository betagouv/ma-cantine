<template>
  <div>
    <h2 class="mb-2 text-h6 font-weight-bold">
      Ajoutez une nouvelle cantine satellite
    </h2>
    <p class="text-body-2">
      Utilisez le formulaire en dessous pour ajouter des satellites un après l'autre. Sinon, utilisez notre
      <router-link :to="{ name: 'DiagnosticsImporter' }">outil d'import des cantines et diagnostics</router-link>
      si vous avez les données en format CSV.
    </p>
    <v-card outlined>
      <v-card-text>
        <v-row v-if="!satellite.siret">
          <v-col>
            <h3 class="body-1 font-weight-bold mb-4">Étape 1/2 : Renseignez le SIRET de votre établissement</h3>
            <p>
              Vous ne le connaissez pas ? Utilisez
              <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank" rel="noopener">
                l'Annuaire des Entreprises
                <v-icon color="primary" small>mdi-open-in-new</v-icon>
              </a>
              pour trouver le SIRET de votre cantine, ou
              <a href="https://annuaire-education.fr/" target="_blank" rel="noopener">
                l'Annuaire de l'Éducation
                <v-icon color="primary" small>mdi-open-in-new</v-icon>
              </a>
              pour les cantines scolaires.
            </p>
            <SiretCheck
              @siretIsValid="setCanteenData"
              :canteen="satellite"
              @updateCanteen="(x) => $emit('updateCanteen', x)"
            />
          </v-col>
        </v-row>
        <v-form ref="form" v-model="formIsValid" v-if="satellite.siret">
          <h3 class="mb-4">Étape 2/2 : Compléter les informations</h3>
          <v-row class="pb-0">
            <v-col cols="12" md="8">
              <p class="mb-0">SIRET</p>
              <p class="grey--text text--darken-2 mb-0">
                {{ satellite.siret }}
                <v-btn small @click="satellite = {}">Modifier</v-btn>
              </p>
            </v-col>
          </v-row>
          <v-row class="mt-0">
            <v-col cols="12" md="5">
              <label class="body-2" for="satellite-name">Nom de la cantine</label>
              <DsfrTextField
                id="satellite-name"
                hide-details="auto"
                validate-on-blur
                v-model="satellite.name"
                :rules="[validators.required]"
              />
            </v-col>
            <v-col cols="12" md="5">
              <label class="body-2" for="sectors">Secteurs d'activité</label>
              <DsfrSelect
                id="sectors"
                multiple
                :items="sectors"
                v-model="satellite.sectors"
                item-text="name"
                item-value="id"
                hide-details="auto"
                :rules="[validators.required]"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6" md="3">
              <label class="body-2" for="meal-count">
                Couverts
                <b>par jour</b>
              </label>
              <DsfrTextField
                id="meal-count"
                hide-details="auto"
                validate-on-blur
                v-model.number="satellite.dailyMealCount"
                prepend-icon="$restaurant-fill"
                :rules="[validators.greaterThanZero]"
              />
            </v-col>
            <v-col cols="6" md="3">
              <label class="body-2 d-block" for="yearly-meals">
                Couverts
                <b>par an</b>
              </label>
              <DsfrTextField
                id="yearly-meals"
                hide-details="auto"
                validate-on-blur
                v-model.number="satellite.yearlyMealCount"
                prepend-icon="$restaurant-fill"
                :rules="[validators.greaterThanZero, greaterThanDailyMealCount]"
              />
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
</template>

<script>
import validators from "@/validators"
import { sectorsSelectList } from "@/utils"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrSelect from "@/components/DsfrSelect"
import SiretCheck from "../SiretCheck"

export default {
  name: "AddSatellite",
  components: { DsfrTextField, DsfrSelect, SiretCheck },
  props: {
    canteen: Object,
  },
  data() {
    return {
      formIsValid: true,
      satellite: {},
    }
  },
  computed: {
    validators() {
      return validators
    },
    sectors() {
      return sectorsSelectList(this.$store.state.sectors)
    },
  },
  methods: {
    setCanteenData(data) {
      this.$set(this, "satellite", data)
    },
    saveSatellite() {
      if (!this.$refs.form.validate()) {
        this.$store.dispatch("notifyRequiredFieldsError")
        window.scrollTo(0, 0)
        return
      }
      this.$store
        .dispatch("addSatellite", { id: this.canteen.id, payload: this.satellite })
        .then(() => {
          this.$store.dispatch("notify", {
            title: "Cantine satellite ajoutée",
            message: "Votre cantine satellite a bien été créée.",
            status: "success",
          })
          this.satellite = {}
        })
        .then(() => this.$emit("satelliteAdded"))
        .catch((error) => {
          if (error.message) {
            this.$store.dispatch("notify", {
              title: error.message,
              status: "error",
            })
          } else {
            this.$store.dispatch("notifyServerError", error)
          }
        })
    },
    greaterThanDailyMealCount(input) {
      if (input && Number(input) < Number(this.satellite.dailyMealCount)) {
        return `Ce total doit être supérieur du moyen de repas par jour sur place, actuellement ${this.satellite.dailyMealCount}`
      }
      return true
    },
  },
}
</script>
