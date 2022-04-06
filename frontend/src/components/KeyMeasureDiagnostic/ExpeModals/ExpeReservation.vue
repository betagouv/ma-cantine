<template>
  <div>
    <div v-if="showSpinner" style="min-height: 290px; background-color: white">
      <v-progress-circular indeterminate style="position: absolute; left: 50%; top: 50%"></v-progress-circular>
    </div>
    <v-card class="text-left" v-else-if="expe">
      <v-card-title class="font-weight-black">
        Vous êtes inscrit à l'expérimentation
      </v-card-title>
      <v-card-text>
        Afin de pouvoir évaluer les effets de la solution de réservation sur la satisfaction des usagers et le taux de
        fréquentation et de confirmer son potentiel en tant que levier de lutte contre le gaspillage alimentaire, nous
        vous demandons de suivre et renseigner différents indicateurs nécessaires à l’évaluation du gaspillage
        alimentaire, du taux de fréquentation et de la satisfaction des usagers à 3 étapes de l’expérimentation.
      </v-card-text>
      <v-card-text class="text-center">
        <v-btn class="mr-4" color="primary" outlined>Télécharger le guide</v-btn>
        <v-btn color="primary" text>Lire le décret de l'expérimentation</v-btn>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-text>
        <v-form ref="form" v-model="formIsValid">
          <!-- reservation system in place? -->
          <v-checkbox v-model="expe.hasReservationSystem">
            <template v-slot:label>
              <span class="body-2 grey--text text--darken-3">
                J'ai déjà mis en place une solution de réservation de repas
              </span>
            </template>
          </v-checkbox>

          <!-- reservation system date -->
          <label v-if="expe.hasReservationSystem" class="body-2 grey--text text--darken-3" for="date">
            Date de mise en place de la solution de réservation
          </label>
          <v-menu
            v-if="expe.hasReservationSystem"
            v-model="reservationSystemStartDateMenu"
            :close-on-content-click="true"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :value="humanReadableDate(expe.reservationSystemStartDate)"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
                hide-details="auto"
                solo
                dense
                style="max-width: 200px"
                id="date"
                class="mt-2 mb-4"
              ></v-text-field>
            </template>

            <v-date-picker
              v-if="expe.hasReservationSystem"
              v-model="expe.reservationSystemStartDate"
              :max="today"
              locale="fr-FR"
            ></v-date-picker>
          </v-menu>

          <!-- launch date -->
          <label class="body-2 grey--text text--darken-3" for="launch-date">
            Date de lancement de l’expérimentation (à partir de février – mars 2022 jusqu’au 1er juillet 2023) T0 :
          </label>
          <v-menu
            v-model="launchDateMenu"
            :close-on-content-click="true"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :value="humanReadableDate(expe.experimentationStartDate)"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
                hide-details="auto"
                dense
                solo
                style="max-width: 200px"
                id="date"
                class="mt-2 mb-4"
              ></v-text-field>
            </template>

            <v-date-picker v-model="expe.experimentationStartDate" :max="today" locale="fr-FR"></v-date-picker>
          </v-menu>

          <!-- description -->
          <label class="body-2 grey--text text--darken-3" for="reservation-system-description">
            Quel type de réservation de repas allez-vous mettre en place ? Décrivez-en le fonctionnement.
          </label>
          <v-textarea
            validate-on-blur
            hide-details="auto"
            rows="2"
            solo
            v-model="expe.reservationSystemDescription"
            placeholder="Réservation via un logiciel, une application, …"
            class="mt-2 mb-4 body-2"
            id="reservation-system-description"
          ></v-textarea>

          <!-- communication -->
          <label class="body-2 grey--text text--darken-3" for="communication">
            Comment comptez-vous communiquer sur la mise en place de la solution de réservation de repas dans votre
            établissement auprès de vos usagers ?
          </label>
          <v-textarea
            validate-on-blur
            hide-details="auto"
            rows="2"
            solo
            v-model="expe.publiciseMethod"
            placeholder="Affichage sur lieu de restaurant, communication mail, courrier,... "
            class="mt-2 mb-4 body-2"
            id="communication"
          ></v-textarea>

          <!-- leader in charge -->

          <v-checkbox hide-details="auto" class="mt-2" v-model="expe.hasLeader">
            <template v-slot:label>
              <span class="body-2 grey--text text--darken-3">
                Un responsable chargé du pilotage du projet a été désigné
              </span>
            </template>
          </v-checkbox>

          <!-- leader personal info -->
          <div v-if="expe.hasLeader" class="mt-2">
            <label class="body-2 grey--text text--darken-3" for="leader-first-name">
              Prénom du responsable
            </label>
            <v-text-field
              hide-details="auto"
              solo
              dense
              v-model="expe.leaderFirstName"
              style="max-width: 300px"
              class="mt-2 mb-2 body-2"
              id="leader-first-name"
            ></v-text-field>
            <label class="body-2 grey--text text--darken-3" for="leader-last-name">
              Nom du responsable
            </label>
            <v-text-field
              hide-details="auto"
              solo
              dense
              v-model="expe.leaderLastName"
              style="max-width: 300px"
              class="mt-2 mb-4 body-2"
              id="leader-last-name"
            ></v-text-field>
            <label class="body-2 grey--text text--darken-3" for="leader-email">
              Adresse email du responsable
            </label>
            <v-text-field
              hide-details="auto"
              solo
              dense
              v-model="expe.leaderEmail"
              style="max-width: 300px"
              class="mt-2 mb-4 body-2"
              id="leader-email"
            ></v-text-field>
          </div>

          <!-- has regulations -->
          <v-checkbox hide-details="auto" class="mt-2" v-model="expe.hasRegulations">
            <template v-slot:label>
              <span class="body-2 grey--text text--darken-3">
                Un réglement à destination des convives a été rédigé
              </span>
            </template>
          </v-checkbox>

          <!-- has committee -->
          <v-checkbox hide-details="auto" class="mt-2" v-model="expe.hasCommittee">
            <template v-slot:label>
              <span class="body-2 grey--text text--darken-3">
                Un comité de pilotage du projet a été défini
              </span>
            </template>
          </v-checkbox>

          <!-- t0, t1, t2 -->
          <v-divider class="mt-4"></v-divider>
          <p class="body-1 font-weight-bold mt-4 mb-0">
            Évaluons l’impact sur la fréquentation et satisfaction convive
          </p>
          <p class="body-2 mt-0">
            Tous les 3 mois, revenez sur cette page afin de renseigner les taux de fréquentation de l’établissement.
          </p>
          <div class="mt-4 tabs-container">
            <v-tabs
              next-icon="mdi-chevron-right"
              prev-icon="mdi-chevron-left"
              :show-arrows="$vuetify.breakpoint.xs"
              v-model="tab"
              align-with-title
              color="primary"
              background-color="primary lighten-5"
            >
              <v-tab v-for="item in tabs" :key="item.key">
                {{ item.label }}
              </v-tab>
            </v-tabs>

            <v-tabs-items v-model="tab">
              <v-tab-item v-for="item in tabs" :key="item.label">
                <v-card flat>
                  <v-card-text>
                    <!-- average weight surplus -->
                    <label class="body-2 grey--text text--darken-3" :for="`avg-weight-not-served-${item.value}`">
                      Moyenne des pesées des excédents présentés aux convives et non servis (g/convive) à
                      <span class="font-italic">{{ item.label }}</span>
                      sur 20 déjeuners successifs
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.nonNegativeOrEmpty]"
                      solo
                      dense
                      v-model.number="expe[`avgWeightNotServed${item.value}`]"
                      style="max-width: 300px"
                      class="mt-2 mb-4 body-2"
                      :id="`avg-weight-not-served-${item.value}`"
                    ></v-text-field>

                    <!-- average weight food scraps -->
                    <label class="body-2 grey--text text--darken-3" :for="`avg-weight-leftover-${item.value}`">
                      Moyenne des pesées des restes des assiettes exprimées (g/convive) à
                      <span class="font-italic">{{ item.label }}</span>
                      sur 20 déjeuners successifs
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.nonNegativeOrEmpty]"
                      solo
                      dense
                      v-model.number="expe[`avgWeightLeftover${item.value}`]"
                      style="max-width: 300px"
                      class="mt-2 mb-4 body-2"
                      :id="`avg-weight-leftover-${item.value}`"
                    ></v-text-field>

                    <!-- ratio edible vs non-edible -->
                    <label class="body-2 grey--text text--darken-3" :for="`ratio-edible-${item.value}`">
                      Ratio de la part non comestible (g) rapportée à la part comestible (g)
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      suffix="%"
                      :rules="[validators.isPercentageOrEmpty]"
                      solo
                      dense
                      v-model.number="expe[`ratioEdibleNonEdible${item.value}`]"
                      style="max-width: 300px"
                      class="mt-2 mb-4 body-2"
                      :id="`ratio-edible-${item.value}`"
                    ></v-text-field>

                    <!-- average weight preparation leftovers -->
                    <label
                      class="body-2 grey--text text--darken-3"
                      :for="`avg-weight-preparation-leftover-${item.value}`"
                    >
                      Si vous préparez les repas sur place : moyenne des pesées des excédents de préparation (g/convive)
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.nonNegativeOrEmpty]"
                      solo
                      dense
                      v-model.number="expe[`avgWeightPreparationLeftover${item.value}`]"
                      style="max-width: 300px"
                      class="mt-2 mb-4 body-2"
                      :id="`avg-weight-preparation-leftover-${item.value}`"
                    ></v-text-field>

                    <!-- average bread leftover -->
                    <label class="body-2 grey--text text--darken-3" :for="`avg-bread-leftover-${item.value}`">
                      Moyenne des pesées des pains jetés sur 20 déjeuners successifs (g/convive)
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.nonNegativeOrEmpty]"
                      solo
                      dense
                      v-model.number="expe[`avgWeightBreadLeftover${item.value}`]"
                      style="max-width: 300px"
                      class="mt-2 mb-4 body-2"
                      :id="`avg-bread-leftover-${item.value}`"
                    ></v-text-field>

                    <!-- attendance rate -->
                    <label
                      class="body-2 grey--text text--darken-3"
                      :for="`avg-attendance-from-evaluation-${item.value}`"
                    >
                      Nombre moyen d'usagers par déjeuner calculé à partir de l'évaluation du nombre d'usagers sur 20
                      déjeuners successifs de la période d'évaluation à
                      <span class="font-italic">{{ item.label }}</span>
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.nonNegativeOrEmpty]"
                      solo
                      dense
                      v-model.number="expe[`avgAttendanceFromEvaluation${item.value}`]"
                      style="max-width: 300px"
                      class="mt-2 mb-4 body-2"
                      :id="`avg-attendance-from-evaluation-${item.value}`"
                    ></v-text-field>

                    <!-- reservation system usage rate -->
                    <label class="body-2 grey--text text--darken-3" :for="`solution-use-rate-${item.value}`">
                      Taux d’utilisation de la solution de réservation
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.isPercentageOrEmpty]"
                      suffix="%"
                      solo
                      dense
                      v-model.number="expe[`solutionUseRate${item.value}`]"
                      style="max-width: 300px"
                      class="mt-2 mb-4 body-2"
                      :id="`solution-use-rate-${item.value}`"
                    ></v-text-field>

                    <!-- comments -->
                    <label class="body-2 grey--text text--darken-3" :for="`comments-${item.value}`">
                      Commentaire
                    </label>
                    <v-textarea
                      validate-on-blur
                      hide-details="auto"
                      rows="2"
                      solo
                      v-model="expe[`comments${item.value}`]"
                      class="mt-2 mb-4 body-2"
                      :id="`comments-${item.value}`"
                    ></v-textarea>

                    <div v-if="item.value === 'T2'">
                      <!-- satisfaction -->
                      <label class="body-2 grey--text text--darken-3" :for="`satisfaction`">
                        Satisfaction moyenne convive (par questionnaire)
                      </label>
                      <v-rating
                        v-model.number="expe.satisfaction"
                        color="primary"
                        empty-icon="mdi-star-outline"
                        full-icon="mdi-star"
                        class="mt-2 mb-4 body-2"
                        :id="`satisfaction`"
                        background-color="grey"
                        length="5"
                        hover
                      ></v-rating>

                      <!-- system cost -->
                      <label class="body-2 grey--text text--darken-3" for="system-cost">
                        Coût de la solution de réservation sur 3 ans
                      </label>
                      <v-text-field
                        validate-on-blur
                        hide-details="auto"
                        :rules="[validators.nonNegativeOrEmpty]"
                        suffix="€"
                        solo
                        dense
                        v-model.number="expe.systemCost"
                        style="max-width: 300px"
                        class="mt-2 mb-4 body-2"
                        id="system-cost"
                      ></v-text-field>

                      <!-- participation cost -->
                      <label class="body-2 grey--text text--darken-3" for="participation-cost">
                        Coûts liés à la participation à l'expérimentation sur 3 ans
                      </label>
                      <v-text-field
                        validate-on-blur
                        hide-details="auto"
                        :rules="[validators.nonNegativeOrEmpty]"
                        suffix="€"
                        solo
                        dense
                        v-model.number="expe.participationCost"
                        style="max-width: 300px"
                        class="mt-2 mb-4 body-2"
                        id="participation-cost"
                      ></v-text-field>

                      <!-- participation cost -->
                      <label class="body-2 grey--text text--darken-3" for="participation-cost-details">
                        Détails des coûts liés à la participation à l'expérimentation
                      </label>
                      <v-textarea
                        validate-on-blur
                        hide-details="auto"
                        solo
                        rows="2"
                        v-model="expe.participationCostDetails"
                        class="mt-2 mb-4 body-2"
                        id="participation-cost-details"
                      ></v-textarea>

                      <!-- money saved -->
                      <label class="body-2 grey--text text--darken-3" for="money-saved">
                        Gains générés par l'évitement du gaspillage laimentaire en euros sur 3 ans
                      </label>
                      <v-text-field
                        validate-on-blur
                        hide-details="auto"
                        :rules="[validators.nonNegativeOrEmpty]"
                        suffix="€"
                        solo
                        dense
                        v-model.number="expe.moneySaved"
                        style="max-width: 300px"
                        class="mt-2 mb-4 body-2"
                        id="money-saved"
                      ></v-text-field>
                    </div>
                  </v-card-text>
                </v-card>
              </v-tab-item>
            </v-tabs-items>
          </div>
        </v-form>
        <v-card-actions class="mt-4">
          <v-spacer></v-spacer>
          <v-btn @click="() => $emit('close')" :disabled="isLoading" x-large outlined color="primary" class="mr-4">
            Annuler
          </v-btn>
          <v-btn @click="save" :disabled="isLoading" x-large color="primary">Sauvegarder</v-btn>
        </v-card-actions>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { formatDate, getObjectDiff } from "@/utils"
import { treatInboundPercentageValues, treatOutboundPercentageValues } from "./utils"
import validators from "@/validators"
import Constants from "@/constants"

export default {
  name: "ExpeReservation",
  props: {
    canteen: Object,
  },
  data() {
    return {
      formIsValid: true,
      expe: null,
      originalExpe: null,
      reservationSystemStartDateMenu: false,
      launchDateMenu: false,
      tab: null,
      tabs: [
        { label: "T0", value: "T0" },
        { label: "T0 + 3 mois", value: "T1" },
        { label: "T0 + 5 mois", value: "T2" },
      ],
      percentageFields: [
        "ratioEdibleNonEdibleT0",
        "solutionUseRateT0",
        "ratioEdibleNonEdibleT1",
        "solutionUseRateT1",
        "ratioEdibleNonEdibleT2",
        "solutionUseRateT2",
      ],
    }
  },
  methods: {
    humanReadableDate(date) {
      return date ? formatDate(date) : ""
    },
    save() {
      this.$refs.form.validate()
      if (!this.formIsValid) {
        this.$store.dispatch("notifyRequiredFieldsError")
        return
      }

      const method = this.isNewExpe ? "createReservationExpe" : "updateReservationExpe"
      const sentExpe = this.isNewExpe
        ? JSON.parse(JSON.stringify(this.expe))
        : getObjectDiff(this.originalExpe, this.expe)
      const payload = treatOutboundPercentageValues(sentExpe, this.percentageFields)
      const successMessage = this.isNewExpe
        ? "Votre inscription a bien été prise en compte"
        : "Vos données de l'expérimentation ont bien été sauvegardés"
      this.$store
        .dispatch(method, { canteen: this.canteen, payload })
        .then(() => {
          this.$store.dispatch("notify", {
            status: "success",
            message: successMessage,
          })
          this.$emit("close")
        })
        .catch((e) => this.$store.dispatch("notifyServerError", e))
    },
  },
  computed: {
    validators() {
      return validators
    },
    today() {
      const today = new Date()
      return today.toISOString().split("T")[0]
    },

    isLoading() {
      return this.$store.state.expeLoadingStatus === Constants.LoadingStatus.LOADING
    },

    showSpinner() {
      return this.isLoading && !this.expe
    },

    isNewExpe() {
      return this.expe && !this.expe.id
    },
  },
  mounted() {
    this.$store
      .dispatch("fetchReservationExpe", { canteen: this.canteen })
      .then((response) => {
        this.originalExpe = treatInboundPercentageValues(response || {}, this.percentageFields)
        this.expe = JSON.parse(JSON.stringify(this.originalExpe))
      })
      .catch((e) => this.$store.dispatch("notifyServerError", e))
  },
}
</script>

<style scoped>
.v-tabs >>> .v-tabs-bar.primary .v-tab,
.v-tabs >>> .v-tabs-bar.primary .v-tabs-slider {
  color: inherit;
}

.tabs-container {
  border: solid 1px #ddd;
  border-radius: 4px;
}
</style>

<style scoped>
.v-form >>> textarea::placeholder {
  color: #444;
}
</style>
