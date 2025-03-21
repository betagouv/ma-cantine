<template>
  <div class="fr-text">
    <ul role="list">
      <li v-if="diagnostic.hasWasteDiagnostic">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J’ai réalisé un diagnostic sur les causes probables de mes déchets alimentaires
        </div>
      </li>
      <li v-else-if="diagnosticUsesNullAsFalse || diagnostic.hasWasteDiagnostic === false">
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n’ai pas encore réalisé un diagnostic sur les causes probables de mes déchets alimentaires
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          Avez-vous réalisé un diagnostic sur les causes probables de vos déchets alimentaires ?
        </div>
      </li>

      <!-- if they have a waste diagnostic, do they have a waste plan? -->
      <li v-if="diagnostic.hasWasteDiagnostic">
        <span v-if="diagnostic.hasWastePlan">
          <v-icon color="primary" class="mr-1">$check-line</v-icon>
          <span>
            J’ai mis en place un plan d’action adapté au diagnostic réalisé
          </span>
        </span>
        <span v-else-if="diagnosticUsesNullAsFalse || diagnostic.hasWastePlan === false">
          <v-icon color="primary" class="mr-1">$close-line</v-icon>
          <span>
            Je n’ai pas encore mis en place un plan d’action adapté au diagnostic réalisé
          </span>
        </span>
        <span v-else>
          <v-icon color="primary" class="mr-1">$question-line</v-icon>
          <span>
            Avez-vous mis en place un plan d’action adapté au diagnostic réalisé ?
          </span>
        </span>
      </li>

      <li v-if="diagnostic.hasWasteMeasures && hasOldWasteMeasures">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J’ai réalisé des mesures de mes déchets alimentaires :
          <ul role="list" class="mt-2">
            <li class="fr-text-xs mb-1" v-for="measure in wasteMeasures" :key="measure.label">
              {{ measure.label }} :
              <span class="font-weight-bold ml-1">{{ measure.value }}</span>
            </li>
          </ul>
        </div>
      </li>
      <li v-else-if="diagnostic.hasWasteMeasures">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <span>
          J’ai réalisé des mesures de mes déchets alimentaires
        </span>
      </li>
      <li v-else-if="diagnosticUsesNullAsFalse || diagnostic.hasWasteMeasures === false">
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n’ai pas encore réalisé des mesures de mes déchets alimentaires
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          Avez-vous réalisé des mesures de vos déchets alimentaires ?
        </div>
      </li>

      <li v-if="appliedWasteActions">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          J’ai mis en place les actions suivantes :
          <ul role="list" class="mt-2">
            <li class="fr-text-xs mb-1" v-for="(action, index) in appliedWasteActions" :key="`${action}-${index}`">
              {{ action }}
            </li>
          </ul>
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je n’ai pas encore mis en place des actions concrètes contre le gaspillage
        </div>
      </li>

      <li v-if="displayDonationAgreementSegment && diagnostic.hasDonationAgreement">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je propose une ou des conventions de dons à des associations habilitées d’aide alimentaire
          <ul role="list" class="mt-2">
            <li class="fr-text-xs mb-1" v-for="measure in donationMeasures" :key="measure.label">
              {{ measure.label }} :
              <span class="font-weight-bold ml-1">{{ measure.value }}</span>
            </li>
          </ul>
        </div>
      </li>

      <li
        v-else-if="
          displayDonationAgreementSegment && (diagnosticUsesNullAsFalse || diagnostic.hasDonationAgreement === false)
        "
      >
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je ne propose pas de convention de dons à des associations habilitées d’aide alimentaire
        </div>
      </li>

      <li v-else-if="displayDonationAgreementSegment">
        <v-icon color="primary" class="mr-2">$question-line</v-icon>
        <div>
          Proposez-vous une convention de dons à des associations habilitées d’aide alimentaire ?
        </div>
      </li>

      <li v-if="canteen.reservationExpeParticipant">
        <v-icon color="primary" class="mr-2">$check-line</v-icon>
        <div>
          Je suis volontaire pour l’expérimentation autour de la réservation de repas
        </div>
      </li>
      <li v-else>
        <v-icon color="primary" class="mr-2">$close-line</v-icon>
        <div>
          Je ne suis pas volontaire pour l’expérimentation autour de la réservation de repas
        </div>
      </li>
    </ul>
    <div v-if="diagnostic.otherWasteComments" class="mt-4 ml-1">
      <p class="font-weight-bold mb-2">Autres commentaires</p>
      <p>{{ diagnostic.otherWasteComments }}</p>
    </div>
    <div>
      <v-dialog v-model="xpReservationInfoDialog" max-width="600">
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="primary" outlined small v-bind="attrs" v-on="on">
            <v-icon small class="mr-2">$information-line</v-icon>
            En savoir plus sur l'expérimentation de réservation de repas de 2023
          </v-btn>
        </template>
        <v-card class="text-left">
          <div class="pa-4 d-flex align-center" style="background-color: #F5F5F5">
            <v-card-title>
              <h1 class="fr-h6 mb-0">
                Expérimentation réservation de repas
              </h1>
            </v-card-title>
            <v-spacer></v-spacer>
            <v-btn color="primary" outlined @click="xpReservationInfoDialog = false">
              Fermer
            </v-btn>
          </div>
          <v-card-text class="text-sm-body-1 grey-text text-darken-3 pt-6">
            <p>
              Vous souhaitez réduire le gaspillage alimentaire dans votre établissement et générer des économies :
              <span class="font-weight-bold">la réservation de repas peut être une solution !</span>
            </p>
            <p>
              Pour évaluer ses effets sur le gaspillage alimentaire, la satisfaction de vos convives et le taux de
              fréquentation de votre établissement, nous vous proposons de participer à une expérimentation prévue par
              la loi climat et résilience.
            </p>
            <p>
              Votre candidature à cette expérimentation vous permettra de mettre en place une démarche d’évaluation dont
              les résultats permettront de saisir le potentiel de la solution de réservation de repas.
            </p>
            <p class="font-weight-bold">
              Vous avez déjà mis en place une solution de réservation de repas ou souhaitez en adopter une ? Vous pouvez
              vous inscrire dès maintenant !
            </p>
            <p>
              Vous serez amenés à répondre à des questions sur votre structure et la solution de réservation que vous
              aurez mise en place, ainsi qu’à transmettre des données relatives aux évaluations du gaspillage
              alimentaire, du taux de fréquentation et de la satisfaction des usagers sur une période de six mois.
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
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import wasteActions from "@/data/waste-actions.json"
import { applicableDiagnosticRules, diagnosticUsesNullAsFalse } from "@/utils"

export default {
  name: "WasteMeasureSummary",
  props: {
    diagnostic: {},
    canteen: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      xpReservationInfoDialog: false,
    }
  },
  computed: {
    appliedWasteActions() {
      if (!this.diagnostic.wasteActions?.length) return null
      return [
        ...this.diagnostic.wasteActions.map((x) => wasteActions[x]),
        ...[this.diagnostic.otherWasteAction],
      ].filter((x) => !!x)
    },
    wasteMeasures() {
      const diag = this.diagnostic
      return [
        {
          label: "Total des déchets alimentaires",
          value: isDefined(diag.totalLeftovers) ? `${diag.totalLeftovers} kg pour l'année` : "—",
        },
        {
          label: "Période de mesure",
          value: isDefined(diag.durationLeftoversMeasurement) ? `${diag.durationLeftoversMeasurement} jours` : "—",
        },
        { label: "Reste de pain", value: isDefined(diag.breadLeftovers) ? `${diag.breadLeftovers} kg/an` : "—" },
        { label: "Reste plateau", value: isDefined(diag.servedLeftovers) ? `${diag.servedLeftovers} kg/an` : "—" },
        {
          label: "Reste en production",
          value: isDefined(diag.unservedLeftovers) ? `${diag.unservedLeftovers} kg/an` : "—",
        },
        { label: "Reste de composantes", value: isDefined(diag.sideLeftovers) ? `${diag.sideLeftovers} kg/an` : "—" },
      ]
    },
    hasOldWasteMeasures() {
      // for the campaign of 2025, we no longer ask for waste measures in the diagnostic, but in the anti-waste tool
      const diag = this.diagnostic
      return (
        !!diag.totalLeftovers ||
        !!diag.durationLeftoversMeasurement ||
        !!diag.breadLeftovers ||
        !!diag.servedLeftovers ||
        !!diag.unservedLeftovers ||
        !!diag.sideLeftovers
      )
    },
    displayDonationAgreementSegment() {
      return applicableDiagnosticRules(this.canteen).hasDonationAgreement
    },
    donationMeasures() {
      const d = this.diagnostic
      return [
        { label: "Fréquence de dons", value: isDefined(d.donationFrequency) ? `${d.donationFrequency} dons/an` : "—" },
        {
          label: "Quantité des denrées données",
          value: isDefined(d.donationQuantity) ? `${d.donationQuantity} kg/an` : "—",
        },
        { label: "Type de denrées données", value: d.donationFoodType ? `${d.donationFoodType}` : "—" },
      ]
    },
    diagnosticUsesNullAsFalse() {
      return diagnosticUsesNullAsFalse(this.diagnostic)
    },
  },
}

const isDefined = (value) => value || value === 0
</script>

<style scoped>
ul {
  list-style-type: none;
  padding-left: 0;
}
li {
  margin-bottom: 14px;
  display: flex;
}
li .v-icon {
  align-items: baseline;
}
</style>
