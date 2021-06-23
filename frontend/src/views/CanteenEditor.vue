<template>
  <div class="text-left pb-10">
    <h1 class="font-weight-black text-h4 my-4">
      {{ isNewCanteen ? "Nouvelle cantine" : "Modifier ma cantine" }}
    </h1>

    <PublicationPreviewDialog
      v-if="!isNewCanteen"
      :canteen="canteen"
      :value="showPreview"
      @close="showPreview = false"
    />

    <v-form ref="form" v-model="formIsValid">
      <v-row v-if="!isNewCanteen">
        <v-col cols="12">
          <p class="body-1 mb-0 mt-4 font-weight-black">Publication</p>
          <v-checkbox hide-details="auto" class="mt-0" v-model="canteen.dataIsPublic">
            <template v-slot:label>
              <p class="text-body-2 grey--text text--darken-4 pt-3 ml-2">
                J'accepte que les données relatives aux mesures EGAlim de ma cantine soient visibles sur
                <router-link
                  :to="{
                    name: 'CanteensHome',
                  }"
                >
                  nos cantines
                </router-link>
                .
                <br />
                <span v-if="originalCanteenIsPublished">Cette cantine est actuellement publié sur</span>

                <v-btn
                  v-if="originalCanteenIsPublished"
                  @click.stop
                  :href="
                    $router.resolve({
                      name: 'CanteenPage',
                      params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(canteen) },
                    }).href
                  "
                  class="text-body-2 pl-1 text-decoration-underline"
                  target="_blank"
                  small
                  text
                  plain
                  :ripple="false"
                >
                  nos cantines
                  <v-icon small color="grey darken-4" class="ml-1">mdi-open-in-new</v-icon>
                </v-btn>

                <v-btn
                  @click.stop="showPreview = true"
                  class="text-body-2 px-0 text-decoration-underline grey--text text--darken-4"
                  small
                  text
                  plain
                  v-else
                  :ripple="false"
                >
                  Voir un aperçu de la publication
                </v-btn>
              </p>
            </template>
          </v-checkbox>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="8">
          <p class="body-2 my-2">Nom de la cantine</p>
          <v-text-field
            hide-details="auto"
            :rules="[validators.notEmpty]"
            validate-on-blur
            solo
            v-model="canteen.name"
          ></v-text-field>

          <p class="body-2 mt-6 mb-2">SIRET</p>
          <v-text-field hide-details="auto" solo v-model="canteen.siret"></v-text-field>
        </v-col>

        <v-col cols="12" md="4" height="100%" class="d-flex flex-column">
          <div class="text-right">
            <v-btn
              class="mr-2 text-decoration-underline"
              text
              color="red"
              small
              v-if="canteen.mainImage"
              @click="changeProfileImage(null)"
            >
              <v-icon class="mr-1" small>mdi-delete-forever</v-icon>
              Supprimer
            </v-btn>
            <v-btn text class="text-decoration-underline" color="primary" @click="onProfilePhotoUploadClick" small>
              <v-icon class="mr-1" small>mdi-image</v-icon>
              Choisir une photo
            </v-btn>
            <input ref="uploader" class="d-none" type="file" accept="image/*" @change="onProfilePhotoChanged" />
          </div>
          <div class="flex-grow-1 mt-2 fill-height">
            <v-sheet rounded color="grey lighten-2" class="fill-height d-flex align-center justify-center">
              <v-img contain v-if="canteen.mainImage" :src="canteen.mainImage" max-height="150"></v-img>
              <v-icon v-else size="40" color="grey" class="py-4">mdi-image-off-outline</v-icon>
            </v-sheet>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="4">
          <p class="body-2 my-2">Ville / commune</p>
          <v-text-field
            hide-details="auto"
            :rules="[validators.notEmpty]"
            validate-on-blur
            solo
            v-model="canteen.city"
          ></v-text-field>
        </v-col>

        <v-col cols="12" md="4">
          <p class="body-2 my-2">Département</p>
          <v-select
            solo
            v-model="canteen.department"
            :rules="[validators.notEmpty]"
            validate-on-blur
            :items="departments"
            :item-text="(item) => `${item.departmentCode} - ${item.departmentName}`"
            item-value="departmentCode"
            hide-details="auto"
          ></v-select>
        </v-col>

        <v-col cols="12" md="4">
          <p class="body-2 my-2">Nombre de couverts moyen par jour</p>
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

        <v-col cols="12" md="8">
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

        <v-col cols="12" md="4">
          <p class="body-2 my-2">Mode de gestion</p>
          <!-- TODO: either make this optional in API or mandatory here -->
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
      </v-row>
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

    <div v-if="!isNewCanteen">
      <h2 class="font-weight-black text-h5 mt-10">
        Mes diagnostics pour cette cantine
      </h2>
      <v-btn text color="primary" class="mt-2 mb-8 ml-n4" :to="{ name: 'NewDiagnostic' }">
        <v-icon class="mr-2">mdi-plus</v-icon>
        Ajouter un diagnostic
      </v-btn>
      <v-row>
        <v-col cols="12" v-for="diagnostic in canteen.diagnostics" :key="`diagnostic-${diagnostic.id}`">
          <DiagnosticCard :diagnostic="diagnostic" class="fill-height" />
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import validators from "@/validators"
import DiagnosticCard from "@/components/DiagnosticCard"
import PublicationPreviewDialog from "@/views/ManagementPage/PublicationPreviewDialog"
import departments from "@/departments.json"
import { toBase64, getObjectDiff } from "@/utils"

const LEAVE_WARNING = "Êtes-vous sûr de vouloir quitter cette page ? Votre cantine n'a pas été sauvegardée."

export default {
  name: "CanteenEditor",
  components: { DiagnosticCard, PublicationPreviewDialog },
  props: {
    canteenUrlComponent: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      canteen: {},
      formIsValid: true,
      originalCanteenIsPublished: false,
      showPreview: false,
      bypassLeaveWarning: false,
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
    validators() {
      return validators
    },
    sectors() {
      return this.$store.state.sectors
    },
    departments() {
      return departments
    },
    originalCanteen() {
      return this.canteenUrlComponent && this.$store.getters.getCanteenFromUrlComponent(this.canteenUrlComponent)
    },
    isNewCanteen() {
      return !this.canteenUrlComponent
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
      this.originalCanteenIsPublished = canteen.dataIsPublic
    } else this.$router.push({ name: "NewCanteen" })
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
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
    onProfilePhotoUploadClick() {
      this.$refs.uploader.click()
    },
    onProfilePhotoChanged(e) {
      this.changeProfileImage(e.target.files[0])
    },
    changeProfileImage(file) {
      if (!file) {
        this.canteen.mainImage = null
        return
      }
      toBase64(file, (base64) => {
        this.$set(this.canteen, "mainImage", base64)
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

<style scoped>
.v-btn--plain:not(.v-btn--active):not(.v-btn--loading):not(:focus):not(:hover) >>> .v-btn__content {
  opacity: 1;
}
</style>
