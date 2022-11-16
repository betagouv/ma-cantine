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
        <v-form ref="form" v-model="formIsValid">
          <v-row>
            <v-col cols="12" md="8">
              <label class="body-2" for="satellite-siret">SIRET</label>
              <DsfrTextField
                id="satellite-siret"
                hide-details="auto"
                validate-on-blur
                v-model="satellite.siret"
                :rules="[validators.length(14), validators.luhn]"
              />
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
              <DsfrTextField
                id="meal-count"
                hide-details="auto"
                validate-on-blur
                v-model="satellite.dailyMealCount"
                prepend-icon="$restaurant-fill"
              />
            </v-col>
          </v-row>
          <v-row class="mt-n4">
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
                class="mt-2"
                multiple
                :items="sectors"
                v-model="satellite.sectors"
                item-text="name"
                item-value="id"
                hide-details
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

export default {
  name: "AddSatellite",
  components: { DsfrTextField, DsfrSelect },
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
  },
}
</script>
