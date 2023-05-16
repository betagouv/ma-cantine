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
              @duplicateCanteenFound="addExistingCanteen"
              :canteen="satellite"
              :allowDuplicates="true"
            />
          </v-col>
        </v-row>
        <v-form ref="form" v-model="formIsValid" v-if="satellite.siret && !satellite.id">
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
            <v-col cols="12" md="6">
              <label class="body-2" for="satellite-city">Ville</label>
              <CityField
                :location="satellite"
                :rules="[validators.required]"
                @locationUpdate="setLocation"
                id="satellite-city"
              />
            </v-col>
          </v-row>
          <v-row>
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
            <v-col v-if="showMinistryField" cols="12" md="6">
              <label class="body-2" for="line-ministry">Ministère de tutelle</label>
              <DsfrSelect
                id="line-ministry"
                :items="ministries"
                v-model="satellite.lineMinistry"
                :rules="[validators.required]"
                placeholder="Sélectionnez le Ministère de tutelle"
                hide-details="auto"
                clearable
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6" md="4">
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
            <v-col cols="6" md="4">
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
import CityField from "../CityField"
import Constants from "@/constants"

export default {
  name: "AddSatellite",
  components: { DsfrTextField, DsfrSelect, SiretCheck, CityField },
  props: {
    canteen: Object,
  },
  data() {
    return {
      formIsValid: true,
      satellite: {},
      ministries: Constants.Ministries,
    }
  },
  computed: {
    validators() {
      return validators
    },
    sectors() {
      return sectorsSelectList(this.$store.state.sectors)
    },
    showMinistryField() {
      const concernedSectors = this.sectors.filter((x) => !!x.hasLineMinistry).map((x) => x.id)
      if (concernedSectors.length === 0) return false
      return this.satellite.sectors?.some((x) => concernedSectors.indexOf(x) > -1)
    },
  },
  methods: {
    setCanteenData(data) {
      this.$set(this, "satellite", data)
    },
    addExistingCanteen(data) {
      this.$set(this, "satellite", data)
      this.addSatellite()
    },
    saveSatellite() {
      if (!this.$refs.form.validate()) {
        this.$store.dispatch("notifyRequiredFieldsError")
        window.scrollTo(0, 0)
        return
      }
      this.addSatellite()
    },
    addSatellite() {
      this.$store
        .dispatch("addSatellite", { id: this.canteen.id, payload: this.satellite })
        .then(() => {
          this.$store.dispatch("notify", {
            title: "Cantine satellite ajoutée",
            message: "Votre cantine satellite a bien été ajoutée.",
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
          this.satellite = {}
        })
    },
    greaterThanDailyMealCount(input) {
      if (input && Number(input) < Number(this.satellite.dailyMealCount)) {
        return `Ce total doit être supérieur du moyen de repas par jour sur place, actuellement ${this.satellite.dailyMealCount}`
      }
      return true
    },
    setLocation(location) {
      this.satellite.city = location.city
      this.satellite.cityInseeCode = location.cityInseeCode
      this.satellite.postalCode = location.postalCode
      this.satellite.department = location.department
    },
  },
}
</script>
