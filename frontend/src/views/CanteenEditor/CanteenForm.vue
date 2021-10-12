<template>
  <div class="text-left pb-10">
    <h1 class="font-weight-black text-h4 my-4">
      {{ isNewCanteen ? "Nouvelle cantine" : "Modifier ma cantine" }}
    </h1>

    <PublicationStateNotice :canteen="originalCanteen" :includeLink="true" v-if="!isNewCanteen" />

    <v-form ref="form" v-model="formIsValid">
      <v-row>
        <v-col cols="12" md="8">
          <p class="body-2 my-2">Nom de la cantine</p>
          <v-text-field
            hide-details="auto"
            :rules="[validators.required]"
            validate-on-blur
            solo
            v-model="canteen.name"
          ></v-text-field>

          <p class="body-2 mt-6 mb-2">SIRET</p>
          <v-text-field
            hide-details="auto"
            validate-on-blur
            solo
            v-model="canteen.siret"
            :rules="[validators.length(14), validators.luhn]"
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="4" height="100%" class="d-flex flex-column">
          <div class="body-2">
            Logo
          </div>
          <div v-if="canteen.logo" class="body-2 grey--text grey--lighten-2">
            Cliquez sur le logo pour changer
          </div>
          <div>
            <input ref="uploader" class="d-none" type="file" accept="image/*" @change="onLogoChanged" id="logo" />
          </div>
          <div class="flex-grow-1 mt-2 fill-height">
            <v-card
              @click="onLogoUploadClick"
              rounded
              color="grey lighten-5"
              class="fill-height"
              style="overflow: hidden;"
            >
              <div v-if="canteen.logo" class="d-flex flex-column fill-height">
                <v-spacer></v-spacer>
                <v-img contain :src="canteen.logo" max-height="135"></v-img>
                <v-spacer></v-spacer>
              </div>
              <div v-else class="d-flex flex-column align-center justify-center fill-height">
                <v-icon class="pb-2">mdi-shape</v-icon>
                <p class="ma-0 text-center font-weight-bold body-2 grey--text text--darken-2">Ajoutez un logo</p>
              </div>
              <div v-if="canteen.logo" style="position: absolute; top: 10px; left: 10px;">
                <v-btn fab small @click.stop.prevent="changeLogo(null)">
                  <v-icon aria-label="Supprimer logo" aria-hidden="false" color="red">mdi-trash-can-outline</v-icon>
                </v-btn>
              </div>
            </v-card>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="8">
          <p class="body-2 my-2">Ville</p>
          <v-autocomplete
            hide-details="auto"
            :rules="[validators.required]"
            :loading="loadingCommunes"
            :items="communes"
            :search-input.sync="search"
            ref="cityAutocomplete"
            solo
            auto-select-first
            cache-items
            v-model="cityAutocompleteChoice"
            :placeholder="canteen.city"
          ></v-autocomplete>
        </v-col>

        <v-col cols="12" md="4">
          <p class="body-2 my-2">Couverts moyen par jour</p>
          <v-text-field
            hide-details="auto"
            :rules="[validators.greaterThanZero]"
            validate-on-blur
            solo
            v-model="canteen.dailyMealCount"
          ></v-text-field>
        </v-col>

        <v-col cols="12">
          <v-divider></v-divider>
        </v-col>

        <v-col cols="12" md="6">
          <p class="body-2 my-2">Secteurs d'activité</p>
          <v-select
            multiple
            :items="sectors"
            solo
            v-model="canteen.sectors"
            item-text="name"
            item-value="id"
          ></v-select>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <p class="body-2 ml-4">Mode de gestion</p>
          <v-radio-group v-model="canteen.managementType">
            <v-radio
              class="ml-8"
              v-for="item in managementTypes"
              :key="item.value"
              :label="item.text"
              :value="item.value"
            ></v-radio>
          </v-radio-group>
        </v-col>

        <v-col cols="12" sm="6" md="3">
          <p class="body-2 ml-4">Mode de production</p>
          <v-radio-group v-model="canteen.productionType">
            <v-radio
              class="ml-8"
              v-for="item in productionTypes"
              :key="item.value"
              :label="item.text"
              :value="item.value"
            ></v-radio>
          </v-radio-group>
        </v-col>
      </v-row>
      <div>
        <label class="body-2" for="images">Images</label>
        <ImagesField class="mt-0 mb-4" :imageArray.sync="canteen.images" id="images" />
      </div>
    </v-form>

    <v-sheet rounded color="grey lighten-4 pa-3" class="d-flex">
      <v-spacer></v-spacer>
      <v-btn x-large outlined color="primary" class="mr-4 align-self-center" :to="{ name: 'ManagementPage' }">
        Annuler
      </v-btn>
      <v-btn x-large color="primary" @click="saveCanteen">
        Valider
      </v-btn>
    </v-sheet>
  </div>
</template>

<script>
import validators from "@/validators"
import { toBase64, getObjectDiff } from "@/utils"
import PublicationStateNotice from "./PublicationStateNotice"
import ImagesField from "./ImagesField"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Votre cantine n'a pas été sauvegardée."

export default {
  name: "CanteenForm",
  components: { PublicationStateNotice, ImagesField },
  props: {
    originalCanteen: {
      type: Object,
      required: false,
    },
  },
  data() {
    return {
      canteen: {},
      formIsValid: true,
      bypassLeaveWarning: false,
      deletionDialog: false,
      cityAutocompleteChoice: {},
      communes: [],
      loadingCommunes: false,
      search: null,
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
      productionTypes: [
        {
          text: "Cuisine centrale",
          value: "central",
        },
        {
          text: "Cuisine-site",
          value: "site",
        },
      ],
    }
  },
  computed: {
    validators() {
      return validators
    },
    sectors() {
      return this.$store.state.sectors
    },
    isNewCanteen() {
      return !this.originalCanteen
    },
    hasChanged() {
      if (this.originalCanteen) {
        const diff = getObjectDiff(this.originalCanteen, this.canteen)
        return Object.keys(diff).length > 0
      } else {
        return Object.keys(this.canteen).length > 0
      }
    },
  },
  beforeMount() {
    if (this.isNewCanteen) return
    const canteen = this.originalCanteen
    if (canteen) {
      this.canteen = JSON.parse(JSON.stringify(canteen))
      if (canteen.city) {
        const initialCityAutocomplete = {
          text: canteen.city,
          value: {
            label: canteen.city,
            citycode: canteen.cityInseeCode,
            postcode: canteen.postalCode,
            context: canteen.department,
          },
        }
        this.communes = [initialCityAutocomplete]
        this.cityAutocompleteChoice = initialCityAutocomplete.value
      }
      if (!this.canteen.images) this.canteen.images = []
    } else this.$router.push({ name: "NewCanteen" })
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
    if (this.originalCanteen) {
      document.title = `Modifier - ${this.originalCanteen.name} - ma-cantine.beta.gouv.fr`
    } else {
      document.title = `Nouvelle cantine - ma-cantine.beta.gouv.fr`
    }
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
  methods: {
    saveCanteen() {
      this.$refs.form.validate()

      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      const payload = this.originalCanteen ? getObjectDiff(this.originalCanteen, this.canteen) : this.canteen
      this.$store
        .dispatch(this.isNewCanteen ? "createCanteen" : "updateCanteen", {
          id: this.canteen.id,
          payload,
        })
        .then(() => {
          this.bypassLeaveWarning = true
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message: `Votre cantine a bien été ${this.isNewCanteen ? "créée" : "modifiée"}`,
            status: "success",
          })
          this.$router.push({ name: "ManagementPage" })
        })
        .catch(() => {
          this.$store.dispatch("notifyServerError")
        })
    },
    onLogoUploadClick() {
      this.$refs.uploader.click()
    },
    onLogoChanged(e) {
      this.changeLogo(e.target.files[0])
    },
    changeLogo(file) {
      if (!file) {
        this.canteen.logo = null
        return
      }
      toBase64(file, (base64) => {
        this.$set(this.canteen, "logo", base64)
      })
    },
    handleUnload(e) {
      if (this.hasChanged && !this.bypassLeaveWarning) {
        e.preventDefault()
        e.returnValue = LEAVE_WARNING
      } else {
        delete e["returnValue"]
      }
    },
    queryCommunes(val) {
      this.loadingCommunes = true
      const queryUrl = "https://api-adresse.data.gouv.fr/search/?q=" + val + "&type=municipality&autocomplete=1"
      return fetch(queryUrl)
        .then((response) => response.json())
        .then((response) => {
          const communes = response.features
          this.communes = communes.map((commune) => {
            return { text: `${commune.properties.label} (${commune.properties.context})`, value: commune.properties }
          })
          this.loadingCommunes = false
        })
        .catch((error) => {
          console.log(error)
        })
    },
  },
  watch: {
    search(val) {
      return val && val !== this.canteen.city && this.queryCommunes(val)
    },
    cityAutocompleteChoice(val) {
      if (val?.label) {
        this.canteen.city = val.label
        this.canteen.cityInseeCode = val.citycode
        this.canteen.postalCode = val.postcode
        this.canteen.department = val.context.split(",")[0]
      }

      this.search = this.canteen.city
    },
  },
  beforeRouteLeave(to, from, next) {
    if (!this.hasChanged || this.bypassLeaveWarning) {
      next()
      return
    }
    window.confirm(LEAVE_WARNING) ? next() : next(false)
  },
}
</script>
