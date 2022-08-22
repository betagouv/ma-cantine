<template>
  <div class="text-left pb-10">
    <h1 class="font-weight-black text-h4 my-4">
      {{ isNewCanteen ? "Nouvelle cantine" : "Modifier ma cantine" }}
    </h1>

    <TechnicalControlDialog
      :bodyText="technicalControlText"
      v-model="showTechnicalControlDialog"
      @save="(e) => saveCanteen(e, true)"
    />

    <PublicationStateNotice
      :canteen="originalCanteen"
      :includeLink="true"
      v-if="!isNewCanteen && originalCanteen.productionType !== 'central'"
    />

    <v-form ref="form" v-model="formIsValid">
      <v-row>
        <v-col cols="12" md="8">
          <DsfrTextField
            hide-details="auto"
            validate-on-blur
            label="SIRET"
            v-model="canteen.siret"
            :rules="[validators.length(14), validators.luhn]"
            @blur="getCanteenBySiret"
            labelClasses="body-2 mb-2"
          />
          <p class="caption mt-1 ml-2">
            Vous ne le connaissez pas ? Utilisez cet
            <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank" rel="noopener">
              outil de recherche pour trouver le SIRET
              <v-icon color="primary" small>mdi-open-in-new</v-icon>
            </a>
            de votre cantine.
          </p>

          <v-card outlined class="mt-4" v-if="duplicateSiretCanteen" color="red lighten-5">
            <v-card-title class="pt-2 pb-1 font-weight-medium">
              Une cantine avec ce SIRET existe déjà
            </v-card-title>
            <v-card-text v-if="duplicateSiretCanteen.isManagedByUser">
              <p>« {{ duplicateSiretCanteen.name }} » a le même SIRET et fait déjà partie de vos cantines.</p>
              <v-btn
                color="primary"
                :to="{
                  name: 'CanteenModification',
                  params: { canteenUrlComponent: $store.getters.getCanteenUrlComponent(duplicateSiretCanteen) },
                }"
                target="_blank"
                rel="noopener"
              >
                Voir les informations de « {{ duplicateSiretCanteen.name }} »
              </v-btn>
            </v-card-text>
            <v-card-text v-else>
              <p>Demandez accès aux gestionnaires de « {{ duplicateSiretCanteen.name }} »</p>
              <DsfrTextarea
                v-model="messageJoinCanteen"
                label="Message (optionnel)"
                hide-details="auto"
                rows="2"
                class="mt-2 body-2"
              />
              <v-btn color="primary" class="mt-4" @click="sendMgmtRequest">
                <v-icon class="mr-2">mdi-key</v-icon>
                Demander l'accès
              </v-btn>
            </v-card-text>

            <v-card-text class="pt-0">
              <v-divider class="mt-4"></v-divider>

              <p class="mb-0 mt-2">
                Il s'agit d'une erreur ?
                <v-dialog v-model="siretDialog" width="500">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn text v-bind="attrs" v-on="on" color="primary darken-1">Contactez l'équipe ma cantine</v-btn>
                  </template>

                  <v-card class="text-left">
                    <v-card-title class="font-weight-bold">Contactez l'équipe ma cantine</v-card-title>
                    <v-card-text class="pb-0">
                      <p>
                        Vous recontrez des problèmes concernant le SIRET de votre cantine ? Envoyez nous un message et
                        notre équipe reviendra vers vous dans les plus brefs délais
                      </p>
                      <v-form v-model="siretFormIsValid" ref="siretHelp" @submit.prevent>
                        <DsfrTextarea
                          v-model="messageTroubleshooting"
                          label="Message"
                          labelClasses="body-2 text-left mb-2"
                          rows="3"
                          :rules="[validators.required]"
                          class="body-2"
                        />
                      </v-form>
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions class="pa-4 pr-6">
                      <v-spacer></v-spacer>
                      <v-btn x-large outlined color="primary" @click="siretDialog = false" class="mr-2">
                        Annuler
                      </v-btn>
                      <v-btn x-large color="primary" @click="sendSiretHelp">
                        <v-icon class="mr-2">mdi-send</v-icon>
                        Envoyer
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </p>
            </v-card-text>
          </v-card>

          <DsfrTextField
            hide-details="auto"
            label="Nom de la cantine"
            :rules="[validators.required]"
            validate-on-blur
            v-model="canteen.name"
            labelClasses="body-2 mb-2"
          />

          <p class="body-2 mt-4 mb-2">Ville</p>
          <DsfrAutocomplete
            hide-details="auto"
            :rules="[validators.required]"
            :loading="loadingCommunes"
            :items="communes"
            :search-input.sync="search"
            ref="cityAutocomplete"
            auto-select-first
            cache-items
            v-model="cityAutocompleteChoice"
            no-data-text="Pas de résultats. Veuillez renseigner votre ville"
          />
        </v-col>

        <v-col cols="12" sm="6" md="4" height="100%" class="d-flex flex-column">
          <label class="body-2" for="logo">
            Logo
          </label>
          <div v-if="canteen.logo" class="body-2 grey--text text--darken-1">
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
              min-height="170"
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
                  <v-icon aria-label="Supprimer logo" aria-hidden="false" color="red">$delete-line</v-icon>
                </v-btn>
              </div>
            </v-card>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" class="mt-2">
          <v-divider></v-divider>
        </v-col>

        <v-col cols="12">
          <p class="body-1 ml-1 mb-0">Je suis...</p>
          <v-radio-group class="mt-2" v-model="canteen.productionType" hide-details="auto">
            <v-radio class="ml-0" v-for="item in productionTypes" :key="item.value" :value="item.value">
              <template v-slot:label>
                <div class="d-block">
                  <div class="body-1 grey--text text--darken-4" v-html="item.title"></div>
                </div>
              </template>
            </v-radio>
          </v-radio-group>
        </v-col>

        <v-col cols="12" md="6" :class="showDailyMealCount ? '' : 'grey--text text--darken-1'">
          <DsfrTextField
            label="Couverts moyen par jour (convives sur place)"
            hide-details="auto"
            :rules="showDailyMealCount ? [validators.greaterThanZero] : []"
            :disabled="!showDailyMealCount"
            :messages="showDailyMealCount ? [] : 'Concerne uniquement les cantines recevant des convives'"
            validate-on-blur
            v-model="canteen.dailyMealCount"
            prepend-icon="$restaurant-fill"
            labelClasses="body-2 mb-2"
          />
        </v-col>

        <v-col cols="12" md="6" :class="showSatelliteCanteensCount ? '' : 'grey--text text--darken-1'">
          <DsfrTextField
            label="Nombre de cantines à qui je fournis des repas"
            hide-details="auto"
            :rules="showSatelliteCanteensCount ? [validators.greaterThanZero] : []"
            :disabled="!showSatelliteCanteensCount"
            :messages="
              showSatelliteCanteensCount ? [] : 'Concerne uniquement les cuisines qui livrent à des satellites'
            "
            validate-on-blur
            v-model="canteen.satelliteCanteensCount"
            prepend-icon="$community-fill"
            labelClasses="body-2 mb-2"
          />
        </v-col>

        <v-expand-transition>
          <v-col cols="12" md="8" v-if="usesCentralProducer" class="py-0">
            <DsfrTextField
              label="SIRET de la cuisine centrale"
              class="mt-2"
              hide-details="auto"
              validate-on-blur
              v-model="canteen.centralProducerSiret"
              :rules="[validators.length(14), validators.luhn]"
            />
            <p class="caption mt-1 ml-2">
              Vous ne le connaissez pas ? Utilisez cet
              <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank" rel="noopener">
                outil de recherche pour trouver le SIRET
              </a>
              de la cuisine centrale.
            </p>
          </v-col>
        </v-expand-transition>
      </v-row>

      <v-row>
        <v-col cols="12" class="mt-4">
          <v-divider></v-divider>
        </v-col>

        <v-col cols="12" md="6">
          <div>
            <p class="body-2">Secteurs d'activité</p>
            <DsfrSelect
              multiple
              :items="sectors"
              v-model="canteen.sectors"
              item-text="name"
              item-value="id"
              hide-details
            />
          </div>
        </v-col>
        <v-col cols="12" md="6">
          <div>
            <p class="body-2">Type d'établissement</p>
            <DsfrSelect
              :items="economicModels"
              solo
              v-model="canteen.economicModel"
              placeholder="Sélectionnez..."
              hide-details="auto"
              clearable
            />
          </div>
        </v-col>
        <v-col v-if="showMinistryField" cols="12">
          <p class="body-2">Ministère de tutelle</p>
          <DsfrSelect
            :items="ministries"
            v-model="canteen.lineMinistry"
            placeholder="Sélectionnez le Ministère de tutelle"
            hide-details="auto"
            clearable
          />
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
      </v-row>
      <div>
        <label class="body-2" for="images">Images</label>
        <ImagesField class="mt-0 mb-4" :imageArray.sync="canteen.images" id="images" />
      </div>
    </v-form>

    <v-dialog v-model="siretQueryInProgress" false width="300">
      <v-card class="py-4">
        <v-card-text>
          Recherche des données en cours...
          <br />
          <v-progress-circular indeterminate color="primary" class="mt-4"></v-progress-circular>
        </v-card-text>
      </v-card>
    </v-dialog>

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
import { toBase64, getObjectDiff, sectorsSelectList, readCookie } from "@/utils"
import PublicationStateNotice from "./PublicationStateNotice"
import TechnicalControlDialog from "./TechnicalControlDialog"
import ImagesField from "./ImagesField"
import Constants from "@/constants"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrAutocomplete from "@/components/DsfrAutocomplete"
import DsfrSelect from "@/components/DsfrSelect"
import DsfrTextarea from "@/components/DsfrTextarea"

const LEAVE_WARNING = "Voulez-vous vraiment quitter cette page ? Votre cantine n'a pas été sauvegardée."

export default {
  name: "CanteenForm",
  components: {
    PublicationStateNotice,
    ImagesField,
    TechnicalControlDialog,
    DsfrTextField,
    DsfrAutocomplete,
    DsfrSelect,
    DsfrTextarea,
  },
  props: {
    canteenUrlComponent: {
      type: String,
      required: false,
    },
    originalCanteen: {
      type: Object,
      required: false,
    },
  },
  data() {
    const user = this.$store.state.loggedUser
    return {
      canteen: { images: [], sectors: [] },
      technicalControlText: null,
      showTechnicalControlDialog: false,
      formIsValid: true,
      bypassLeaveWarning: false,
      deletionDialog: false,
      cityAutocompleteChoice: null,
      communes: [],
      loadingCommunes: false,
      search: null,
      managementTypes: Constants.ManagementTypes,
      productionTypes: [
        {
          title: "une <b>cantine</b> qui produit sur place les repas que je sers à mes convives",
          body: "Je prépare ce que je sers à mes convives",
          value: "site",
        },
        {
          title: "une <b>cantine</b> qui sert des repas preparés par une cuisine centrale",
          body: "Les repas que je sers à mes convives sont cuisinés ailleurs",
          value: "site_cooked_elsewhere",
        },
        {
          title: "une <b>cuisine centrale</b> qui livre des satellites mais n'a pas de lieu de service en propre",
          body: "Je prépare des produits pour des cantines satellites et je ne reçois pas de convives sur place",
          value: "central",
        },
        {
          title: "une <b>cuisine centrale</b> qui accueille aussi des convives sur place",
          body: "Je prépare des produits pour des cantines satellites et j'ai aussi de la restauration sur place",
          value: "central_serving",
        },
      ],
      economicModels: [
        { text: "Public", value: "public" },
        { text: "Privé", value: "private" },
      ],
      user,
      siretQueryInProgress: false,
      // contact forms
      fromEmail: user.email,
      fromName: `${user.firstName} ${user.lastName}`,
      messageJoinCanteen: null,
      messageTroubleshooting: null,
      siretFormIsValid: true,
      duplicateSiretCanteen: null,
      siretDialog: false,
      ministries: [
        { value: "premier_ministre", text: "Service du Premier Ministre" },
        { value: "affaires_etrangeres", text: "Ministère de l’Europe et des Affaires étrangères" },
        { value: "ecologie", text: "Ministère de la Transition écologique" },
        { value: "jeunesse", text: "Ministère de l’Education Nationale et de la Jeunesse et des Sports" },
        { value: "economie", text: "Ministère de l’Economie, de la Finance et de la Relance" },
        { value: "armee", text: "Ministère de l’Armée" },
        { value: "interieur", text: "Ministère de l’Intérieur" },
        { value: "travail", text: "Ministère Travail, de l’Emploi et de l’Insertion" },
        { value: "outre_mer", text: "Ministère des Outre-mer" },
        {
          value: "territoires",
          text: "Ministère de la Cohésion des Territoires et des Relations avec les Collectivités Territoriales",
        },
        { value: "justice", text: "Ministère de la Justice" },
        { value: "culture", text: "Ministère de la Culture" },
        { value: "sante", text: "Ministère des Solidarités et de la Santé" },
        { value: "mer", text: "Ministère de la Mer" },
        {
          value: "enseignement_superieur",
          text: "Ministère de l’Enseignement Supérieur et de la Recherche et de l’Innovation",
        },
        { value: "agriculture", text: "Ministère de l’Agriculture et de l’Alimentation" },
        { value: "transformation", text: "Ministère de la Transformation et de la Fonction Publiques" },
        { value: "autre", text: "Autre" },
      ],
    }
  },
  computed: {
    validators() {
      return validators
    },
    sectors() {
      return sectorsSelectList(this.$store.state.sectors)
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
    showSatelliteCanteensCount() {
      return this.canteen.productionType === "central" || this.canteen.productionType === "central_serving"
    },
    showDailyMealCount() {
      return this.canteen.productionType && this.canteen.productionType !== "central"
    },
    showMinistryField() {
      const concernedSectors = this.sectors.filter((x) => !!x.hasLineMinistry).map((x) => x.id)
      if (concernedSectors.length === 0) return false
      return this.canteen.sectors.some((x) => concernedSectors.indexOf(x) > -1)
    },
    usesCentralProducer() {
      return this.canteen.productionType === "site_cooked_elsewhere"
    },
  },
  beforeMount() {
    if (this.isNewCanteen) return

    const canteen = this.originalCanteen
    if (canteen) {
      this.canteen = JSON.parse(JSON.stringify(canteen))
      if (canteen.city) {
        this.populateCityAutocomplete()
      }
      if (!this.canteen.images) this.canteen.images = []
    } else this.$router.push({ name: "NewCanteen" })
  },
  created() {
    window.addEventListener("beforeunload", this.handleUnload)
    if (this.originalCanteen) {
      document.title = `Modifier - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
    } else {
      document.title = `Nouvelle cantine - ${this.$store.state.pageTitleSuffix}`
    }
  },
  beforeDestroy() {
    window.removeEventListener("beforeunload", this.handleUnload)
  },
  methods: {
    getCanteenBySiret() {
      if (!this.canteen.siret) {
        return
      } else if (validators.length(14)(this.canteen.siret) !== true || validators.luhn(this.canteen.siret) !== true) {
        return
      }
      if (this.canteen.name && this.cityAutocompleteChoice) {
        return // do not override user-entered data
      }
      this.siretQueryInProgress = true
      const getInfo = function() {
        fetch(`https://entreprise.data.gouv.fr/api/sirene/v3/etablissements/${this.canteen.siret}`)
          .then((response) => response.json())
          .then((body) => {
            if (body.etablissement) {
              if (!this.canteen.name) {
                let name
                if (body.etablissement.enseigne_1) {
                  name = body.etablissement.enseigne_1
                } else if (body.etablissement.unite_legale?.denomination) {
                  name = body.etablissement.unite_legale.denomination
                }
                this.canteen.name = name
              }

              if (!this.cityAutocompleteChoice && body.etablissement.geo_id) {
                this.canteen.postalCode = body.etablissement.code_postal
                this.canteen.cityInseeCode = body.etablissement.code_commune
                return fetch(`https://plateforme.adresse.data.gouv.fr/lookup/${body.etablissement.geo_id}`)
              }
            }
          })
          .then((response) => response.json())
          .then((body) => {
            this.canteen.city = body.commune.nom
            this.canteen.department = body.commune.departement.code
            // if this lookup fails, the choice will not be populated, making the user pick themselves
            // this is the desired behaviour, since not all location data will be given otherwise
            this.populateCityAutocomplete()
            this.siretQueryInProgress = false
          })
          .catch(() => {
            this.siretQueryInProgress = false
          })
      }.bind(this)
      setTimeout(getInfo, 800)
    },
    saveCanteen(e, bypassTechnicalControl = false) {
      if (!this.$refs.form.validate()) {
        this.$store.dispatch("notifyRequiredFieldsError")
        window.scrollTo(0, 0)
        return
      }

      const payload = this.originalCanteen ? getObjectDiff(this.originalCanteen, this.canteen) : this.canteen
      const fieldsToClean = ["dailyMealCount", "satelliteCanteensCount"]
      fieldsToClean.forEach((x) => {
        if (Object.prototype.hasOwnProperty.call(payload, x) && payload[x] === "") payload[x] = null
      })

      if (!bypassTechnicalControl) {
        if (this.canteen.productionType === "central_serving" && this.canteen.satelliteCanteensCount == 1) {
          this.displayTechnicalControlDialog("Est-ce que vous ne livrez vraiment qu'un seul autre site de service ?")
          return
        }
        const isCentralCanteen =
          this.canteen.productionType === "central_serving" || this.canteen.productionType === "central"
        if (isCentralCanteen && parseInt(this.canteen.satelliteCanteensCount) >= 250) {
          this.displayTechnicalControlDialog(
            `Vous êtes sur le point de déclarer une livraison depuis votre cuisine centrale à ${parseInt(
              this.canteen.satelliteCanteensCount
            )} établissements de service. Voulez-vous vraiment continuer ?`
          )
          return
        }
      }

      if (this.isNewCanteen) {
        for (let i = 0; i < Constants.TrackingParams.length; i++) {
          const cookieValue = readCookie(Constants.TrackingParams[i])
          if (cookieValue) payload[`creation_${Constants.TrackingParams[i]}`] = cookieValue
        }
      }

      this.$store
        .dispatch(this.isNewCanteen ? "createCanteen" : "updateCanteen", {
          id: this.canteen.id,
          payload,
        })
        .then((canteenJson) => {
          this.bypassLeaveWarning = true
          const message = this.isNewCanteen
            ? "Votre cantine a bien été créée. Vous pouvez maintenant ajouter des diagnostics."
            : "Votre cantine a bien été modifiée"
          this.$store.dispatch("notify", {
            title: "Mise à jour prise en compte",
            message,
            status: "success",
          })
          if (this.isNewCanteen) {
            const canteenUrlComponent = this.$store.getters.getCanteenUrlComponent(canteenJson)
            this.$router.push({
              // form validation ensures that the count will be > 0
              name: this.showSatelliteCanteensCount ? "SatelliteManagement" : "DiagnosticList",
              params: { canteenUrlComponent },
            })
          } else {
            this.$router.push({ name: "ManagementPage" })
          }
        })
        .catch((e) => {
          if (e.jsonPromise) {
            e.jsonPromise.then((json) => {
              const isDuplicateSiret = json.detail === "La resource que vous souhaitez créer existe déjà"
              if (isDuplicateSiret) {
                this.duplicateSiretCanteen = json
                this.messageTroubleshooting = `Je veux ajouter une deuxième cantine avec le même SIRET : ${payload.siret}...`
              }
            })
            this.$store.dispatch("notifyRequiredFieldsError")
          } else {
            this.$store.dispatch("notifyServerError", e)
          }
          window.scrollTo(0, 0)
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
    sendSiretHelp() {
      this.$refs.siretHelp.validate()
      if (!this.siretFormIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      let meta = this.meta || {}
      meta.userId = this.$store.state.loggedUser?.id
      meta.userAgent = navigator.userAgent

      const payload = {
        from: this.fromEmail,
        message: this.messageTroubleshooting,
        // TODO: put misc inquiry types in the title of trello card directly
        inquiryType: "cantine SIRET",
        meta,
      }

      this.$store
        .dispatch("sendInquiryEmail", payload)
        .then(() => {
          this.message = null
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé. Nous reviendrons vers vous dans les plus brefs délais.`,
          })
          this.siretDialog = false

          window.scrollTo(0, 0)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    sendMgmtRequest() {
      const payload = {
        email: this.user.email,
        name: this.fromName,
        message: this.messageJoinCanteen,
      }

      this.$store
        .dispatch("sendCanteenTeamRequest", { canteenId: this.duplicateSiretCanteen.id, payload })
        .then(() => {
          this.message = null
          this.$store.dispatch("notify", {
            status: "success",
            message: `Votre message a bien été envoyé.`,
          })
          window.scrollTo(0, 0)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
    populateCityAutocomplete() {
      const initialCityAutocomplete = {
        text: this.canteen.city,
        value: {
          label: this.canteen.city,
          citycode: this.canteen.cityInseeCode,
          postcode: this.canteen.postalCode,
          context: this.canteen.department,
        },
      }
      this.communes.push(initialCityAutocomplete)
      this.cityAutocompleteChoice = initialCityAutocomplete.value
    },
    displayTechnicalControlDialog(bodyText) {
      this.technicalControlText = bodyText
      this.showTechnicalControlDialog = true
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
