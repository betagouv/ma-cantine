<template>
  <v-form @submit.prevent v-model="formIsValid">
    <div v-if="stepUrlSlug === 'plan-action'">
      <LastYearAutofillOption
        :canteen="canteen"
        :diagnostic="diagnostic"
        :fields="fields"
        @tunnel-autofill="onTunnelAutofill"
        class="mb-xs-6 mb-xl-16"
      />
      <DsfrRadio
        v-model="payload.hasWasteDiagnostic"
        label="J’ai réalisé un diagnostic sur les causes probables de mes déchets alimentaires"
        yesNo
        hide-details
      />
      <DsfrRadio
        v-model="payload.hasWastePlan"
        label="J’ai mis en place un plan d’action adapté au diagnostic réalisé"
        yesNo
        hide-details
        :disabled="!payload.hasWasteDiagnostic"
        :readonly="!payload.hasWasteDiagnostic"
        class="mt-8"
      />
    </div>
    <div v-else-if="stepUrlSlug === 'mesure-gaspillage'">
      <v-row>
        <v-col cols="12" sm="6">
          <DsfrRadio
            v-model="payload.hasWasteMeasures"
            label="J’ai réalisé des mesures de mes déchets alimentaires"
            yesNo
            optional
            hide-details
          />
        </v-col>
        <v-col>
          <DsfrCallout>
            <p class="fr-text-sm grey-text text--darken-3">
              Les déchets alimentaires incluent une fraction comestible (assimilable à du gaspillage alimentaire) et une
              fraction non comestible (os, épluchures, arêtes).
            </p>
          </DsfrCallout>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <fieldset :disabled="!payload.hasWasteMeasures">
            <legend class="my-3 font-weight-bold">
              Mesures des déchets
              <span :class="`fr-hint-text mt-2 ${payload.hasWasteMeasures ? '' : 'grey--text'}`">
                Optionnel
              </span>
            </legend>
            <v-row>
              <v-col cols="12" sm="6" class="pb-0">
                <DsfrTextField
                  v-model.number="payload.totalLeftovers"
                  :rules="payload.hasWasteMeasures ? [validators.nonNegativeOrEmpty, validators.decimalPlaces(2)] : []"
                  validate-on-blur
                  label="Total des déchets alimentaires"
                  suffix="kg"
                  :readonly="!payload.hasWasteMeasures"
                  :disabled="!payload.hasWasteMeasures"
                  :hideOptional="true"
                />
              </v-col>
              <v-col cols="12" sm="6" class="pb-0">
                <DsfrTextField
                  :value="payload.durationLeftoversMeasurement"
                  @input="(x) => (payload.durationLeftoversMeasurement = integerInputValue(x))"
                  :rules="
                    payload.hasWasteMeasures
                      ? [validators.nonNegativeOrEmpty, validators.isInteger, validators.lteOrEmpty(365)]
                      : []
                  "
                  validate-on-blur
                  label="Période de mesure"
                  suffix="jours"
                  :readonly="!payload.hasWasteMeasures"
                  :disabled="!payload.hasWasteMeasures"
                  :hideOptional="true"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="6" class="pb-0">
                <DsfrTextField
                  v-model.number="payload.breadLeftovers"
                  :rules="payload.hasWasteMeasures ? [validators.nonNegativeOrEmpty, validators.decimalPlaces(2)] : []"
                  validate-on-blur
                  label="Reste de pain"
                  suffix="kg/an"
                  :readonly="!payload.hasWasteMeasures"
                  :disabled="!payload.hasWasteMeasures"
                  :hideOptional="true"
                />
              </v-col>
              <v-col cols="12" sm="6" class="pb-0">
                <DsfrTextField
                  v-model.number="payload.servedLeftovers"
                  :rules="payload.hasWasteMeasures ? [validators.nonNegativeOrEmpty, validators.decimalPlaces(2)] : []"
                  validate-on-blur
                  label="Reste plateau"
                  suffix="kg/an"
                  :readonly="!payload.hasWasteMeasures"
                  :disabled="!payload.hasWasteMeasures"
                  :hideOptional="true"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="6" class="pb-0">
                <DsfrTextField
                  v-model.number="payload.unservedLeftovers"
                  :rules="payload.hasWasteMeasures ? [validators.nonNegativeOrEmpty, validators.decimalPlaces(2)] : []"
                  validate-on-blur
                  label="Reste en production (non servi)"
                  suffix="kg/an"
                  :readonly="!payload.hasWasteMeasures"
                  :disabled="!payload.hasWasteMeasures"
                  :hideOptional="true"
                />
              </v-col>
              <v-col cols="12" sm="6" class="pb-0">
                <DsfrTextField
                  v-model.number="payload.sideLeftovers"
                  :rules="payload.hasWasteMeasures ? [validators.nonNegativeOrEmpty, validators.decimalPlaces(2)] : []"
                  validate-on-blur
                  label="Reste de composantes (entrée, plat dessert...)"
                  suffix="kg/an"
                  :readonly="!payload.hasWasteMeasures"
                  :disabled="!payload.hasWasteMeasures"
                  :hideOptional="true"
                />
              </v-col>
            </v-row>
          </fieldset>
        </v-col>
      </v-row>
    </div>
    <fieldset v-else-if="stepUrlSlug === 'actions'">
      <legend class="my-3">
        J’ai réalisé les actions suivantes de lutte contre les déchets alimentaires :
        <span class="fr-hint-text mt-2">Optionnel</span>
      </legend>
      <v-checkbox
        hide-details="auto"
        class="mb-3 mt-0"
        v-model="payload.wasteActions"
        :multiple="true"
        v-for="action in wasteActions"
        :key="action.value"
        :value="action.value"
        :label="action.label"
      />
      <v-row align="center" class="ml-0 mb-3 mt-0 mr-2">
        <v-checkbox
          v-model="otherActionEnabled"
          hide-details
          class="shrink mt-0"
          aria-label="Autre : donnez plus d'informations"
        ></v-checkbox>
        <v-text-field
          class="my-0 py-0 other-text-input"
          ref="other-action-field"
          hide-details
          :disabled="!otherActionEnabled"
          v-model="payload.otherWasteAction"
          :rules="otherActionEnabled ? [validators.required] : []"
          label="Autre : donnez plus d'informations"
        ></v-text-field>
      </v-row>
    </fieldset>
    <div v-else-if="stepUrlSlug === 'dons-alimentaires'">
      <v-row>
        <v-col cols="12" sm="6">
          <DsfrRadio
            v-model="payload.hasDonationAgreement"
            label="Je propose une ou des conventions de dons à des associations habilitées d’aide alimentaire"
            yesNo
            optional
            hide-details
          />
        </v-col>
        <v-col cols="12" sm="6">
          <v-row>
            <v-col cols="12" md="6" class="pb-0">
              <DsfrTextField
                label="Fréquence de dons"
                :value="payload.donationFrequency"
                @input="(x) => (payload.donationFrequency = integerInputValue(x))"
                :rules="payload.hasDonationAgreement ? [validators.nonNegativeOrEmpty, validators.isInteger] : []"
                validate-on-blur
                suffix="dons/an"
                :readonly="!payload.hasDonationAgreement"
                :disabled="!payload.hasDonationAgreement"
              />
            </v-col>
            <v-col cols="12" md="6" class="pb-0">
              <DsfrTextField
                label="Quantité de denrées données"
                v-model.number="payload.donationQuantity"
                :rules="
                  payload.hasDonationAgreement ? [validators.nonNegativeOrEmpty, validators.decimalPlaces(2)] : []
                "
                validate-on-blur
                suffix="kg/an"
                :readonly="!payload.hasDonationAgreement"
                :disabled="!payload.hasDonationAgreement"
              />
            </v-col>
            <v-col cols="12" class="pb-0">
              <DsfrTextField
                label="Type de denrées données"
                v-model="payload.donationFoodType"
                :readonly="!payload.hasDonationAgreement"
                :disabled="!payload.hasDonationAgreement"
              />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </div>
    <div v-else-if="stepUrlSlug === 'autres'">
      <v-row>
        <v-col cols="12" sm="9" md="7">
          <DsfrTextarea v-model="payload.otherWasteComments" id="otherWasteComments" rows="3" class="mt-6">
            <template v-slot:label>
              <label for="otherWasteComments" class="mb-3">
                Autres commentaires
                <span class="fr-hint-text mt-2">
                  Optionnel : toute précision que vous souhaiteriez apporter sur votre situation et/ou sur vos actions
                  mises en place pour lutter contre les déchets alimentaires
                </span>
              </label>
            </template>
          </DsfrTextarea>
        </v-col>
      </v-row>
    </div>
    <div v-else-if="stepUrlSlug === 'expérimentation'" class="fr-text">
      <p>
        Vous souhaitez réduire le gaspillage alimentaire dans votre établissement et générer des économies :
        <span class="font-weight-bold">la réservation de repas peut être une solution !</span>
      </p>
      <p>
        Pour évaluer ses effets sur le gaspillage alimentaire, la satisfaction de vos convives et le taux de
        fréquentation de votre établissement, nous vous proposons de participer à une expérimentation prévue par la loi
        climat et résilience.
      </p>
      <p>
        Votre candidature à cette expérimentation vous permettra de mettre en place une démarche d’évaluation dont les
        résultats permettront de saisir le potentiel de la solution de réservation de repas.
      </p>
      <p class="font-weight-bold">
        Vous avez déjà mis en place une solution de réservation de repas ou souhaitez en adopter une ? Vous pouvez vous
        inscrire dès maintenant !
      </p>
      <p>
        Vous serez amenés à répondre à des questions sur votre structure et la solution de réservation que vous aurez
        mise en place, ainsi qu’à transmettre des données relatives aux évaluations du gaspillage alimentaire, du taux
        de fréquentation et de la satisfaction des usagers sur une période de six mois.
      </p>
      <p>Les inscriptions sont ouvertes jusqu’au 1er juillet 2023.</p>
      <p>
        Les informations relatives aux conditions de mise en œuvre de l’expérimentation sont précisées dans
        <a
          href="/static/documents/Guide_pratique_XP_RESERVATION.pdf"
          target="_blank"
          title="le guide pratique - ouvre une nouvelle fenêtre"
        >
          le guide pratique
          <v-icon color="primary" small>mdi-open-in-new</v-icon>
        </a>
        .
      </p>
      <v-checkbox v-model="canteen.reservationExpeParticipant" @change="onExpeCheckboxChange">
        <template v-slot:label>
          <span class="fr-text grey--text text--darken-3">
            Je suis volontaire pour participer à l’expérimentation.
          </span>
        </template>
      </v-checkbox>
      <v-btn
        color="primary"
        class="mt-n2 mb-2"
        v-if="canteen.reservationExpeParticipant"
        outlined
        small
        @click="() => (showExpeModal = true)"
      >
        Mettre à jour mes données
      </v-btn>
      <v-dialog v-model="showExpeModal" :width="$vuetify.breakpoint.mdAndUp ? 900 : undefined">
        <ExpeReservation v-if="showExpeModal" @close="() => (showExpeModal = false)" :canteen="canteen" />
      </v-dialog>
    </div>
    <div v-else-if="stepUrlSlug === 'évaluations'" class="fr-text">
      <p>Complèter vos évaluations de vos déchets alimentaires</p>
      <ul class="mb-2">
        <li v-for="m in measurements" :key="m.id">
          <router-link
            :to="{
              name: 'WasteMeasurementTunnel',
              params: { canteenUrlComponent, id: m.id },
            }"
          >
            {{ m.periodStartDate }} - {{ m.periodEndDate }}
          </router-link>
          : {{ m.totalMass }} kg
        </li>
      </ul>
      <div>
        <v-btn
          color="primary"
          outlined
          small
          :to="{
            name: 'WasteMeasurementTunnel',
            params: { canteenUrlComponent },
            query,
          }"
        >
          Ajouter une nouvelle
        </v-btn>
      </div>
    </div>
  </v-form>
</template>

<script>
import { applicableDiagnosticRules } from "@/utils"
import validators from "@/validators"
import LastYearAutofillOption from "../LastYearAutofillOption"
import DsfrCallout from "@/components/DsfrCallout"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrTextarea from "@/components/DsfrTextarea"
import DsfrRadio from "@/components/DsfrRadio"
import ExpeReservation from "@/components/KeyMeasureDiagnostic/ExpeModals/ExpeReservation"
import Constants from "@/constants"

const STEPS = [
  {
    title: "Diagnostic et plan d’action",
    urlSlug: "plan-action",
  },
  {
    title: "Mesure de mes déchets alimentaires",
    urlSlug: "mesure-gaspillage",
  },
  {
    title: "Détail des actions mises en place",
    urlSlug: "actions",
  },
  {
    title: "Dons alimentaires",
    urlSlug: "dons-alimentaires",
  },
  {
    title: "Autres commentaires",
    urlSlug: "autres",
  },
  {
    title: "Expérimentation réservation de repas",
    urlSlug: "expérimentation",
  },
  {
    title: "Mesure de mes déchets alimentaires (pt 2)",
    urlSlug: "évaluations",
  },
  {
    title: "Synthèse",
    isSynthesis: true,
    urlSlug: "complet",
  },
]

export default {
  name: "WasteSteps",
  props: {
    canteen: {
      type: Object,
      required: true,
    },
    diagnostic: {
      type: Object,
      required: true,
    },
    stepUrlSlug: {
      type: String,
    },
  },
  components: {
    LastYearAutofillOption,
    DsfrCallout,
    DsfrTextField,
    DsfrTextarea,
    DsfrRadio,
    ExpeReservation,
  },
  data() {
    return {
      formIsValid: true,
      showExpeModal: false,
      otherActionEnabled: !!this.diagnostic.otherWasteAction,
      wasteActions: Constants.WasteActions,
      payload: {},
      fields: [
        "hasWasteDiagnostic",
        "hasWastePlan",
        "hasWasteMeasures",
        "totalLeftovers",
        "durationLeftoversMeasurement",
        "breadLeftovers",
        "servedLeftovers",
        "unservedLeftovers",
        "sideLeftovers",
        "wasteActions",
        "otherWasteAction",
        "otherWasteComments",
        "hasDonationAgreement",
        "donationFrequency",
        "donationQuantity",
        "donationFoodType",
      ],
      measurements: undefined,
      query: {
        return: document.location.href,
      },
    }
  },
  computed: {
    steps() {
      // filter steps
      // - 2024-11: hide comment step
      // - hide XP step if not enabled
      // - hide donation step if no donation agreement
      const removeStep = (urlSlug) => {
        let idx = STEPS.findIndex((step) => step.urlSlug === urlSlug)
        if (idx > -1) STEPS.splice(idx, 1)
      }
      removeStep("autres")
      if (!window.ENABLE_XP_RESERVATION) {
        removeStep("expérimentation")
      }
      if (!applicableDiagnosticRules(this.canteen).hasDonationAgreement) {
        removeStep("dons-alimentaires")
      }
      // TODO: make evaluations step conditional on hasWasteMeasures
      // if (!this.payload.hasWasteMeasures) {
      //   removeStep("évaluations")
      // }
      return STEPS
    },
    step() {
      const step = this.stepUrlSlug && this.steps.find((step) => step.urlSlug === this.stepUrlSlug)
      return step || this.steps[0]
    },
    validators() {
      return validators
    },
    canteenUrlComponent() {
      return this.$store.getters.getCanteenUrlComponent(this.canteen)
    },
  },
  methods: {
    initialisePayload() {
      const payload = {}
      this.fields.forEach((f) => (payload[f] = this.diagnostic[f]))
      this.$set(this, "payload", payload)
      this.fetchWasteMeasurements()
    },
    updatePayload() {
      this.$emit("update-payload", { payload: this.payload, formIsValid: this.formIsValid })
    },
    onExpeCheckboxChange(checked) {
      this.$store
        .dispatch("updateCanteen", {
          id: this.canteen.id,
          payload: { reservationExpeParticipant: checked },
        })
        .then((canteen) => {
          this.$emit("update:canteen", canteen)
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))

      if (checked) this.showExpeModal = true
    },
    onTunnelAutofill(e) {
      this.$set(this, "payload", e.payload)
      this.$emit("tunnel-autofill", e)
    },
    integerInputValue(val) {
      return this.numberInputValue(val, parseInt)
    },
    numberInputValue(val, parseFunction) {
      if (val === "") return null
      const parsedValue = parseFunction(val)
      if (parsedValue === 0) return 0
      return parsedValue || val
    },
    fetchWasteMeasurements() {
      // TODO: only fetch for TD year
      fetch(`/api/v1/canteens/${this.canteen.id}/wasteMeasurements`)
        .then((response) => response.json())
        .then((response) => {
          this.measurements = response
        })
    },
  },
  mounted() {
    this.$emit("update-steps", this.steps)
    this.initialisePayload()
    this.updatePayload()
  },
  watch: {
    formIsValid() {
      this.updatePayload()
    },
    payload: {
      handler() {
        this.updatePayload()
      },
      deep: true,
    },
    otherActionEnabled(newValue) {
      if (newValue) this.$nextTick().then(this.$refs["other-action-field"]?.validate)
      else this.payload.otherWasteAction = null
    },
    "payload.hasWasteMeasures": function() {
      if (this.payload.hasWasteMeasures) return
      const fieldsToClear = [
        "totalLeftovers",
        "durationLeftoversMeasurement",
        "breadLeftovers",
        "servedLeftovers",
        "unservedLeftovers",
        "sideLeftovers",
      ]
      fieldsToClear.forEach((x) => (this.payload[x] = null))
    },
    "payload.hasDonationAgreement": function() {
      const fieldsToClear = ["donationFrequency", "donationQuantity", "donationFoodType"]
      fieldsToClear.forEach((x) => (this.payload[x] = null))
    },
    $route() {
      // it is possible to navigate without saving.
      // So must initialise payload every step to avoid saving something unintentionally
      this.initialisePayload()
    },
  },
}
</script>

<style scoped>
fieldset:disabled {
  color: #929292;
}
</style>
