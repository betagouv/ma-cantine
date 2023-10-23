<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasWasteDiagnostic"
      label="J'ai réalisé un diagnostic sur les causes probables de gaspillage alimentaire"
      :readonly="readonly"
      :disabled="readonly"
    />

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasWastePlan"
      label="J'ai mis en place un plan d’actions adapté au diagnostic réalisé"
      :readonly="readonly"
      :disabled="readonly"
    />

    <fieldset class="mt-3 mb-4">
      <legend class="text-left my-3">J'ai réalisé des actions de lutte contre le gaspillage alimentaire :</legend>

      <v-checkbox
        hide-details="auto"
        class="ml-8 mb-3 mt-0"
        v-model="diagnostic.wasteActions"
        :multiple="true"
        v-for="action in wasteActions"
        :key="action.value"
        :value="action.value"
        :label="action.label"
        :readonly="readonly"
        :disabled="readonly"
      />
      <v-row align="center" class="ml-8 mb-3 mt-0 mr-2">
        <v-checkbox
          v-model="otherActionEnabled"
          hide-details
          class="shrink mt-0"
          :readonly="readonly"
          :disabled="readonly"
        ></v-checkbox>
        <!-- Will leave this UI version of the text-field since it is next to a checkbox -->
        <v-text-field
          class="my-0 py-0"
          hide-details
          :disabled="!otherActionEnabled || readonly"
          v-model="diagnostic.otherWasteAction"
          label="Autre : donnez plus d'informations"
          :readonly="readonly"
        ></v-text-field>
      </v-row>
    </fieldset>

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasWasteMeasures"
      label="J'ai réalisé des mesures de mon gaspillage alimentaire"
      :readonly="readonly"
      :disabled="readonly"
    />
    <v-expand-transition>
      <v-row v-if="diagnostic.hasWasteMeasures" class="mt-4 ml-8">
        <v-col cols="12" md="8" class="pa-0">
          <DsfrTextField
            v-model.number="diagnostic.breadLeftovers"
            :rules="[validators.nonNegativeOrEmpty, validators.decimalPlaces(2)]"
            validate-on-blur
            label="Reste de pain"
            suffix="kg/an"
            :readonly="readonly"
            :disabled="readonly"
          />
          <DsfrTextField
            v-model.number="diagnostic.servedLeftovers"
            :rules="[validators.nonNegativeOrEmpty, validators.decimalPlaces(2)]"
            validate-on-blur
            label="Reste plateau"
            suffix="kg/an"
            :readonly="readonly"
            :disabled="readonly"
          />
          <DsfrTextField
            v-model.number="diagnostic.unservedLeftovers"
            :rules="[validators.nonNegativeOrEmpty, validators.decimalPlaces(2)]"
            validate-on-blur
            label="Reste en production (non servi)"
            suffix="kg/an"
            :readonly="readonly"
            :disabled="readonly"
          />
          <DsfrTextField
            v-model.number="diagnostic.sideLeftovers"
            :rules="[validators.nonNegativeOrEmpty, validators.decimalPlaces(2)]"
            validate-on-blur
            label="Reste de composantes (entrée, plat dessert...)"
            suffix="kg/an"
            :readonly="readonly"
            :disabled="readonly"
          />
        </v-col>
      </v-row>
    </v-expand-transition>

    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasDonationAgreement"
      label="Je propose une ou des conventions de dons à des associations habilitées d’aide alimentaire"
      :readonly="readonly"
      :disabled="readonly"
      v-if="applicableRules.hasDonationAgreement"
    />

    <v-expand-transition v-if="applicableRules.hasDonationAgreement">
      <v-row v-if="diagnostic.hasDonationAgreement" class="my-4 ml-8">
        <v-col cols="12" md="8" class="pa-0">
          <DsfrTextField
            v-model.number="diagnostic.donationFrequency"
            :rules="[validators.nonNegativeOrEmpty]"
            validate-on-blur
            label="Fréquence de dons"
            suffix="dons/an"
            :readonly="readonly"
            :disabled="readonly"
          />
          <DsfrTextField
            v-model.number="diagnostic.donationQuantity"
            :rules="[validators.nonNegativeOrEmpty]"
            validate-on-blur
            label="Quantité des denrées données"
            suffix="kg/an"
            :readonly="readonly"
            :disabled="readonly"
          />
        </v-col>
        <v-col cols="11" class="pa-0">
          <DsfrTextField
            v-model="diagnostic.donationFoodType"
            label="Type de denrées données"
            :readonly="readonly"
            :disabled="readonly"
          />
        </v-col>
      </v-row>
    </v-expand-transition>

    <DsfrTextarea
      v-model="diagnostic.otherWasteComments"
      label="Autres commentaires"
      rows="3"
      :readonly="readonly"
      :disabled="readonly"
      class="mt-6"
    />

    <v-divider v-if="showExpeSegment" class="mb-8"></v-divider>
    <div v-if="showExpeSegment">
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

      <v-checkbox v-if="canteen" v-model="canteen.reservationExpeParticipant" @change="onExpeCheckboxChange">
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
  </div>
</template>

<script>
import validators from "@/validators"
import { applicableDiagnosticRules } from "@/utils"
import ExpeReservation from "@/components/KeyMeasureDiagnostic/ExpeModals/ExpeReservation"
import DsfrTextField from "@/components/DsfrTextField"
import DsfrTextarea from "@/components/DsfrTextarea"

export default {
  props: {
    diagnostic: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
    canteen: Object,
  },
  components: { ExpeReservation, DsfrTextField, DsfrTextarea },
  data() {
    return {
      showExpeModal: false,
      wasteActions: [
        {
          label: "Pré-inscription des convives obligatoire",
          value: "INSCRIPTION",
        },
        {
          label: "Sensibilisation par affichage ou autre média",
          value: "AWARENESS",
        },
        {
          label: "Formation / information du personnel de restauration",
          value: "TRAINING",
        },
        {
          label: "Réorganisation de la distribution des composantes du repas",
          value: "DISTRIBUTION",
        },
        {
          label: "Choix des portions (grande faim, petite faim)",
          value: "PORTIONS",
        },
        {
          label: "Réutilisation des restes de préparation / surplus",
          value: "REUSE",
        },
      ],
      otherActionEnabled: !!this.diagnostic.otherWasteAction,
    }
  },
  computed: {
    validators() {
      return validators
    },
    applicableRules() {
      return applicableDiagnosticRules(this.canteen)
    },
    showExpeSegment() {
      return !!this.canteen && window.ENABLE_XP_RESERVATION
    },
  },
  methods: {
    onExpeCheckboxChange(checked) {
      this.$store
        .dispatch("updateCanteen", {
          id: this.canteen.id,
          payload: { reservationExpeParticipant: checked },
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))

      if (checked) this.showExpeModal = true
    },
  },
  watch: {
    otherActionEnabled(val) {
      if (!val) {
        this.diagnostic.otherWasteAction = null
      }
    },
  },
}
</script>

<style scoped>
.explanation {
  color: grey;
  font-size: 0.8em;
}
</style>
