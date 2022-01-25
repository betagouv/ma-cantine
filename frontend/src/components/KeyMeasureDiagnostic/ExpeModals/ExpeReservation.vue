<template>
  <v-card class="text-left">
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
      <v-form>
        <!-- reservation system in place? -->
        <v-checkbox v-model="expe.reservationInPlace">
          <template v-slot:label>
            <span class="body-2 grey--text text--darken-2">
              J'ai déjà mis en place une solution de réservation de repas
            </span>
          </template>
        </v-checkbox>

        <!-- reservation system date -->
        <label v-if="expe.reservationInPlace" class="body-2" for="date">
          Date de mise en place de la solution de réservation
        </label>
        <v-menu
          v-if="expe.reservationInPlace"
          v-model="reservationSystemDateMenu"
          :close-on-content-click="true"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              :value="humanReadableDate(expe.reservationSystemDate)"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              :rules="[validators.required]"
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
            v-if="expe.reservationInPlace"
            v-model="expe.reservationSystemDate"
            :max="today"
            locale="fr-FR"
          ></v-date-picker>
        </v-menu>

        <!-- launch date -->
        <label class="body-2" for="launch-date">
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
              :value="humanReadableDate(expe.launchDate)"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              :rules="[validators.required]"
              v-on="on"
              hide-details="auto"
              dense
              solo
              style="max-width: 200px"
              id="date"
              class="mt-2 mb-4"
            ></v-text-field>
          </template>

          <v-date-picker
            v-if="expe.reservationInPlace"
            v-model="expe.launchDate"
            :max="today"
            locale="fr-FR"
          ></v-date-picker>
        </v-menu>

        <!-- description -->
        <label class="body-2" for="reservation-system-description">
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
        <label class="body-2" for="communication">
          Comment comptez-vous communiquer sur la mise en place de la solution de réservation de repas dans votre
          établissement auprès de vos usagers ?
        </label>
        <v-textarea
          validate-on-blur
          hide-details="auto"
          rows="2"
          solo
          v-model="expe.communication"
          placeholder="Affichage sur lieu de restaurant, communication mail, courrier,... "
          class="mt-2 mb-4 body-2"
          id="communication"
        ></v-textarea>

        <!-- leader in charge -->

        <v-checkbox hide-details="auto" class="mt-2" v-model="expe.hasLeader">
          <template v-slot:label>
            <span class="body-2 grey--text text--darken-2">
              Un responsable chargé du pilotage du projet a été désigné
            </span>
          </template>
        </v-checkbox>

        <!-- leader personal info -->
        <div v-if="expe.hasLeader" class="mt-2">
          <label class="body-2" for="leader-first-name">
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
          <label class="body-2" for="leader-last-name">
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
          <label class="body-2" for="leader-email">
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
            <span class="body-2 grey--text text--darken-2">
              Un réglement à destination des convives a été rédigé
            </span>
          </template>
        </v-checkbox>

        <!-- has committee -->
        <v-checkbox hide-details="auto" class="mt-2" v-model="expe.hasCommittee">
          <template v-slot:label>
            <span class="body-2 grey--text text--darken-2">
              Un comité de pilotage du projet a été défini
            </span>
          </template>
        </v-checkbox>

        <!-- t0, t1, t2 -->
        <v-divider class="mt-4"></v-divider>
        <p class="body-1 font-weight-bold mt-4 mb-0">Évaluons l’impact sur la fréquentation et satisfaction convive</p>
        <p class="body-2 mt-0">
          Tous les 3 mois, revenez sur cette page afin de renseigner les taux de fréquentation de l’établissement.
        </p>
        <div class="mt-4 tabs-container">
          <v-tabs v-model="tab" align-with-title color="primary" background-color="primary lighten-5">
            <v-tab v-for="item in tabs" :key="item.key">
              {{ item.label }}
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="tab">
            <v-tab-item v-for="item in tabs" :key="item.label">
              <v-card flat>
                <v-card-text>
                  <!-- average weight surplus -->
                  <label class="body-2" :for="`avg-weight-surplus-${item.value}`">
                    Moyenne des pesées des excédents présentés aux convives et non servis (g/ convive) à
                    <span class="font-italic">{{ item.label }}</span>
                    sur 20 déjeuners successifs
                  </label>
                  <v-text-field
                    validate-on-blur
                    hide-details="auto"
                    solo
                    dense
                    v-model="expe[`avgWeightSurplus${item.value}`]"
                    style="max-width: 300px"
                    class="mt-2 mb-4 body-2"
                    :id="`avg-weight-surplus-${item.value}`"
                  ></v-text-field>

                  <!-- average weight food scraps -->
                  <label class="body-2" :for="`avg-weight-food-scraps-${item.value}`">
                    Moyenne des pesées des restes des assiettes exprimées (g/convive) à
                    <span class="font-italic">{{ item.label }}</span>
                    sur 20 déjeuners successifs
                  </label>
                  <v-text-field
                    validate-on-blur
                    hide-details="auto"
                    solo
                    dense
                    v-model="expe[`avgWeightFoodScraps${item.value}`]"
                    style="max-width: 300px"
                    class="mt-2 mb-4 body-2"
                    :id="`avg-weight-food-scraps-${item.value}`"
                  ></v-text-field>

                  <!-- ratio edible vs non-edible -->
                  <label class="body-2" :for="`ratio-edible-${item.value}`">
                    Ratio de la part non comestible (g) rapportée à la part comestible (g)
                  </label>
                  <v-text-field
                    validate-on-blur
                    hide-details="auto"
                    solo
                    dense
                    v-model="expe[`ratioEdible${item.value}`]"
                    style="max-width: 300px"
                    class="mt-2 mb-4 body-2"
                    :id="`ratio-edible-${item.value}`"
                  ></v-text-field>

                  <!-- average weight food scraps -->
                  <label class="body-2" :for="`avg-weight-surplus-preparation-${item.value}`">
                    Moyenne des pesées des excédents de préparation (g/convive) - Si vous préparez les repas sur place
                  </label>
                  <v-text-field
                    validate-on-blur
                    hide-details="auto"
                    solo
                    dense
                    v-model="expe[`avgWeightSurplusPreparation${item.value}`]"
                    style="max-width: 300px"
                    class="mt-2 mb-4 body-2"
                    :id="`avg-weight-surplus-preparation-${item.value}`"
                  ></v-text-field>

                  <!-- average discarded bread -->
                  <label class="body-2" :for="`avg-discarded-bread-${item.value}`">
                    Moyenne des pesées des pains jetés sur 20 déjeuners successifs (g/convive)
                  </label>
                  <v-text-field
                    validate-on-blur
                    hide-details="auto"
                    solo
                    dense
                    v-model="expe[`avgDiscardedBread${item.value}`]"
                    style="max-width: 300px"
                    class="mt-2 mb-4 body-2"
                    :id="`avg-discarded-bread-${item.value}`"
                  ></v-text-field>

                  <!-- attendance rate -->
                  <label class="body-2" :for="`attendance-rate-${item.value}`">
                    Taux de fréquentation moyen à
                    <span class="font-italic">{{ item.label }}</span>
                  </label>
                  <v-text-field
                    validate-on-blur
                    hide-details="auto"
                    solo
                    dense
                    v-model="expe[`attendanceRate${item.value}`]"
                    style="max-width: 300px"
                    class="mt-2 mb-4 body-2"
                    :id="`attendance-rate-${item.value}`"
                  ></v-text-field>

                  <!-- reservation system usage rate -->
                  <label class="body-2" :for="`reservation-system-usage-rate-${item.value}`">
                    Taux d’utilisation de la solution de réservation
                  </label>
                  <v-text-field
                    validate-on-blur
                    hide-details="auto"
                    solo
                    dense
                    v-model="expe[`reservationSystemUsage${item.value}`]"
                    style="max-width: 300px"
                    class="mt-2 mb-4 body-2"
                    :id="`reservation-system-usage-rate-${item.value}`"
                  ></v-text-field>

                  <!-- satisfaction -->
                  <label class="body-2" :for="`satisfaction-${item.value}`">
                    Satisfaction moyenne convive (par questionnaire)
                  </label>
                  <v-rating
                    v-model="expe[`satisfaction${item.value}`]"
                    color="primary"
                    empty-icon="mdi-star-outline"
                    full-icon="mdi-star"
                    class="mt-2 mb-4 body-2"
                    :id="`satisfaction-${item.value}`"
                    background-color="grey"
                    length="5"
                    hover
                  ></v-rating>
                </v-card-text>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </div>
      </v-form>
      <v-card-actions class="mt-4">
        <v-spacer></v-spacer>
        <v-btn x-large outlined color="primary" class="mr-4">Annuler</v-btn>
        <v-btn x-large color="primary">Sauvegarder</v-btn>
      </v-card-actions>
    </v-card-text>
  </v-card>
</template>

<script>
import { formatDate } from "@/utils"
import validators from "@/validators"

export default {
  name: "ExpeReservation",
  props: {
    canteen: Object,
  },
  data() {
    return {
      originalExpe: this.canteen.expeReservation || {},
      expe: JSON.parse(JSON.stringify(this.canteen.expeReservation || {})),
      reservationSystemDateMenu: false,
      launchDateMenu: false,
      tab: null,
      tabs: [
        { label: "T0", value: "T0" },
        { label: "T0 + 3 mois", value: "T1" },
        { label: "T0 + 5 mois", value: "T2" },
      ],
    }
  },
  methods: {
    humanReadableDate(date) {
      return date ? formatDate(date) : ""
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
