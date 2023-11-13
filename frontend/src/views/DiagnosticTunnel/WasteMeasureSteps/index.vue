<template>
  <v-form @submit.prevent v-model="formIsValid">
    <div v-if="stepUrlSlug === 'plan-action'">
      <fieldset>
        <legend class="my-3">
          J’ai réalisé un diagnostic sur les causes probables de gaspillage alimentaire
        </legend>
        <v-radio-group class="my-0" v-model="payload.hasWasteDiagnostic" hide-details>
          <v-radio
            v-for="item in boolOptions"
            :key="`hasWasteDiagnostic-${item.value}`"
            :label="item.label"
            :value="item.value"
          ></v-radio>
        </v-radio-group>
      </fieldset>
      <fieldset class="mt-8" :disabled="!payload.hasWasteDiagnostic">
        <legend class="text-left">J’ai mis en place un plan d’action adapté au diagnostic réalisé</legend>
        <v-radio-group class="my-0" v-model="payload.hasWastePlan" hide-details>
          <v-radio
            v-for="item in boolOptions"
            :key="`hasWastePlan-${item.value}`"
            :label="item.label"
            :value="item.value"
            :disabled="!payload.hasWasteDiagnostic"
            :readonly="!payload.hasWasteDiagnostic"
          ></v-radio>
        </v-radio-group>
      </fieldset>
    </div>
    <div v-else-if="stepUrlSlug === 'mesure-gaspillage'">
      <v-row>
        <v-col cols="12" sm="6">
          <fieldset>
            <legend class="my-3">
              J’ai réalisé des mesures de mon gaspillage alimentaire
            </legend>
            <v-radio-group class="my-0" v-model="payload.hasWasteMeasures" hide-details>
              <v-radio v-for="item in boolOptions" :key="item.value" :label="item.label" :value="item.value"></v-radio>
            </v-radio-group>
          </fieldset>
        </v-col>
        <v-col cols="12" sm="6">
          <fieldset :disabled="!payload.hasWasteMeasures">
            <legend class="my-3">
              Mesures du gaspillage
            </legend>
            <v-row class="mt-4">
              <v-col cols="12" md="6">
                <DsfrTextField
                  v-model.number="payload.breadLeftovers"
                  :rules="[validators.nonNegativeOrEmpty, validators.decimalPlaces(2)]"
                  validate-on-blur
                  label="Reste de pain"
                  suffix="kg/an"
                  :readonly="!payload.hasWasteMeasures"
                  :disabled="!payload.hasWasteMeasures"
                />
              </v-col>
              <v-col cols="12" md="6">
                <DsfrTextField
                  v-model.number="payload.servedLeftovers"
                  :rules="[validators.nonNegativeOrEmpty, validators.decimalPlaces(2)]"
                  validate-on-blur
                  label="Reste plateau"
                  suffix="kg/an"
                  :readonly="!payload.hasWasteMeasures"
                  :disabled="!payload.hasWasteMeasures"
                />
              </v-col>
              <v-col cols="12" md="6">
                <DsfrTextField
                  v-model.number="payload.unservedLeftovers"
                  :rules="[validators.nonNegativeOrEmpty, validators.decimalPlaces(2)]"
                  validate-on-blur
                  label="Reste en production (non servi)"
                  suffix="kg/an"
                  :readonly="!payload.hasWasteMeasures"
                  :disabled="!payload.hasWasteMeasures"
                />
              </v-col>
              <v-col cols="12" md="6">
                <DsfrTextField
                  v-model.number="payload.sideLeftovers"
                  :rules="[validators.nonNegativeOrEmpty, validators.decimalPlaces(2)]"
                  validate-on-blur
                  label="Reste de composantes (entrée, plat dessert...)"
                  suffix="kg/an"
                  :readonly="!payload.hasWasteMeasures"
                  :disabled="!payload.hasWasteMeasures"
                />
              </v-col>
            </v-row>
          </fieldset>
        </v-col>
      </v-row>
    </div>
    <div v-else-if="stepUrlSlug === 'actions'">
      <fieldset>
        <legend class="my-3">J’ai réalisé les actions de lutte contre le gaspillage alimentaire suivantes :</legend>
      </fieldset>
      <v-checkbox
        hide-details="auto"
        class="ml-8 mb-3 mt-0"
        v-model="payload.wasteActions"
        :multiple="true"
        v-for="action in wasteActions"
        :key="action.value"
        :value="action.value"
        :label="action.label"
      />
      <v-row align="center" class="ml-8 mb-3 mt-0 mr-2">
        <v-checkbox v-model="otherActionEnabled" hide-details class="shrink mt-0"></v-checkbox>
        <v-text-field
          class="my-0 py-0"
          hide-details
          :disabled="!otherActionEnabled"
          v-model="payload.otherWasteAction"
          label="Autre : donnez plus d'informations"
        ></v-text-field>
      </v-row>
    </div>
    <div v-else-if="stepUrlSlug === 'dons-alimentaires'">
      <v-row>
        <v-col cols="12" sm="6">
          <fieldset>
            <legend class="my-3">
              Je propose une ou des conventions de dons à des associations habilitées d’aide alimentaire
            </legend>
            <v-radio-group class="my-0" v-model="payload.hasDonationAgreement" hide-details>
              <v-radio v-for="item in boolOptions" :key="item.value" :label="item.label" :value="item.value"></v-radio>
            </v-radio-group>
          </fieldset>
        </v-col>
        <v-col cols="12" sm="6"></v-col>
      </v-row>
    </div>
    <div v-else-if="stepUrlSlug === 'autres'">
      <v-row>
        <v-col cols="12" sm="9" md="7">
          <fieldset>
            <legend class="my-3">Autres commentaires</legend>
            <p class="fr-text-xs mt-1 mb-3">
              Optionnel : toute précision que vous souhaiteriez apporter sur votre situation et/ou sur vos actions mises
              en place pour lutter contre le gaspillage alimentaire
            </p>
            <DsfrTextarea v-model="payload.otherWasteComments" rows="3" class="mt-6" />
          </fieldset>
        </v-col>
      </v-row>
    </div>
    <div v-else-if="stepUrlSlug === 'expérimentation'">
      <h3 class="text-h6 font-weight-bold mb-4">
        Expérimentation réservation de repas
      </h3>

      <p class="body-2">
        Vous souhaitez réduire le gaspillage alimentaire dans votre établissement et générer des économies :
        <span class="font-weight-bold">la réservation de repas peut être une solution !</span>
      </p>
      <p class="body-2">
        Pour évaluer ses effets sur le gaspillage alimentaire, la satisfaction de vos convives et le taux de
        fréquentation de votre établissement, nous vous proposons de participer à une expérimentation prévue par la loi
        climat et résilience.
      </p>
      <p class="body-2">
        Votre candidature à cette expérimentation vous permettra de mettre en place une démarche d’évaluation dont les
        résultats permettront de saisir le potentiel de la solution de réservation de repas.
      </p>
      <p class="body-2 font-weight-bold">
        Vous avez déjà mis en place une solution de réservation de repas ou souhaitez en adopter une ? Vous pouvez vous
        inscrire dès maintenant !
      </p>
      <p class="body-2">
        Vous serez amenés à répondre à des questions sur votre structure et la solution de réservation que vous aurez
        mise en place, ainsi qu’à transmettre des données relatives aux évaluations du gaspillage alimentaire, du taux
        de fréquentation et de la satisfaction des usagers sur une période de six mois.
      </p>
      <p class="body-2">Les inscriptions sont ouvertes jusqu’au 1er juillet 2023.</p>
      <p class="body-2">
        Les informations relatives aux conditions de mise en œuvre de l’expérimentation sont précisées dans
        <a href="/static/documents/Guide_pratique_XP_RESERVATION.pdf" target="_blank">le guide pratique</a>
        .
      </p>
      <v-checkbox v-model="canteen.reservationExpeParticipant" @change="onExpeCheckboxChange">
        <template v-slot:label>
          <span class="body-2 grey--text text--darken-3">
            Je suis volontaire pour participer à l’expérimentation.
          </span>
        </template>
      </v-checkbox>
      <v-btn
        color="primary"
        class="body-2 mt-n2 mb-2"
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
    <component
      v-else
      :is="step.componentName"
      :canteen="canteen"
      :diagnostic="diagnostic"
      v-on:update-payload="updatePayload"
    />
  </v-form>
</template>

<script>
import { applicableDiagnosticRules } from "@/utils"
import WasteMeasureSummary from "@/components/DiagnosticSummary/WasteMeasureSummary"
import validators from "@/validators"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrTextarea from "@/components/DsfrTextarea"
import ExpeReservation from "@/components/KeyMeasureDiagnostic/ExpeModals/ExpeReservation"
import Constants from "@/constants"

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
    WasteMeasureSummary,
    DsfrTextField,
    DsfrTextarea,
    ExpeReservation,
  },
  data() {
    const payload = {
      hasWasteDiagnostic: this.diagnostic.hasWasteDiagnostic,
      hasWastePlan: this.diagnostic.hasWastePlan,
      hasWasteMeasures: this.diagnostic.hasWasteMeasures,
      breadLeftovers: this.diagnostic.breadLeftovers,
      servedLeftovers: this.diagnostic.servedLeftovers,
      unservedLeftovers: this.diagnostic.unservedLeftovers,
      sideLeftovers: this.diagnostic.sideLeftovers,
      wasteActions: this.diagnostic.wasteActions,
      otherWasteAction: this.diagnostic.otherWasteAction,
      otherWasteComments: this.diagnostic.otherWasteComments,
    }
    const steps = [
      {
        title: "Diagnostic et plan d’action",
        urlSlug: "plan-action",
      },
      {
        title: "Mesure de mon gaspillage alimentaire",
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
        title: "Synthèse",
        isSynthesis: true,
        componentName: "WasteMeasureSummary",
        urlSlug: "synthèse",
      },
    ]
    if (!window.ENABLE_XP_RESERVATION) steps.splice(5, 1)
    if (!applicableDiagnosticRules(this.canteen).hasDonationAgreement) steps.splice(3, 1)
    return {
      formIsValid: true,
      showExpeModal: false,
      otherActionEnabled: !!this.diagnostic.otherWasteAction,
      wasteActions: Constants.WasteActions,
      steps,
      boolOptions: [
        {
          label: "Oui",
          value: true,
        },
        {
          label: "Non",
          value: false,
        },
      ],
      payload,
    }
  },
  computed: {
    step() {
      const step = this.stepUrlSlug && this.steps.find((step) => step.urlSlug === this.stepUrlSlug)
      return step || this.steps[0]
    },
    validators() {
      return validators
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
  },
  methods: {
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
  },
  mounted() {
    this.$emit("update-steps", this.steps)
    this.updatePayload()
  },
  watch: {
    payload() {
      this.updatePayload()
    },
    formIsValid() {
      this.updatePayload()
    },
  },
}
</script>

<style scoped>
fieldset:disabled {
  color: rgba(0, 0, 0, 0.38);
}
</style>
