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
        <p>
          Afin d'évaluer les effets de la mise en place du menu végétarien quotidien sur la satisfaction des usagers et
          le taux de fréquentation, nous vous demandons de suivre et renseigner différents indicateurs ci-dessous à deux
          étapes de l’expérimentation.
        </p>
        <p>
          Pour plus d'informations, consultez le
          <a
            href="https://ma-cantine-1.gitbook.io/ma-cantine-egalim/diversification-des-sources-de-proteines-et-menus-vegetariens/guide-pour-la-mise-en-place-du-menu-vegetarien-en-milieu-scolaire"
            target="_blank"
            rel="noopener"
          >
            livret de recettes végétariennes du CNRC
            <v-icon small color="primary">mdi-open-in-new</v-icon>
          </a>
          et le
          <a
            href="https://ma-cantine-1.gitbook.io/ma-cantine-egalim/diversification-des-sources-de-proteines-et-menus-vegetariens/untitled"
            target="_blank"
            rel="noopener"
          >
            le cadre pour la mise en oeuvre du plan pluriannuel de diversification des sources de protéines
            <v-icon small color="primary">mdi-open-in-new</v-icon>
          </a>
        </p>
      </v-card-text>
      <v-divider></v-divider>

      <v-card-text>
        <v-form ref="form" v-model="formIsValid">
          <!-- daily vegetarian option in place? -->
          <v-checkbox v-model="expe.hasDailyVegetarianOffer">
            <template v-slot:label>
              <span class="body-2 grey--text text--darken-3">
                J'ai déjà mis en place l'option végétarienne quotidienne
              </span>
            </template>
          </v-checkbox>

          <!-- daily vegetarian option implementation date -->
          <label v-if="expe.hasDailyVegetarianOffer" class="body-2 grey--text text--darken-3" for="date">
            Date de mise en place
          </label>
          <v-menu
            v-if="expe.hasDailyVegetarianOffer"
            v-model="vegetarianDailyStartDateMenu"
            :close-on-content-click="true"
            transition="scale-transition"
            offset-y
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :value="humanReadableDate(expe.dailyVegetarianOfferStartDate)"
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
              v-if="expe.hasDailyVegetarianOffer"
              v-model="expe.dailyVegetarianOfferStartDate"
              :max="today"
              locale="fr-FR"
            ></v-date-picker>
          </v-menu>

          <!-- launch date -->
          <label class="body-2 grey--text text--darken-3" for="launch-date">
            Date de lancement de l’expérimentation
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
                    <!-- Vegetarian menu rate -->
                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium"
                      :for="`vegetarian-menu-percentage-${item.value}`"
                    >
                      Pourcentage de menus végétariens servis par rapport aux autres menus
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.lteOrEmpty(100)]"
                      solo
                      dense
                      v-model.number="expe[`vegetarianMenuPercentage${item.value}`]"
                      append-icon="mdi-percent"
                      style="max-width: 150px"
                      class="mt-2 mb-4 body-2"
                      :id="`vegetarian-menu-percentage-${item.value}`"
                    ></v-text-field>

                    <!-- Menu composition -->
                    <label class="body-2 grey--text text--darken-3 font-weight-medium">
                      Dans votre plan alimentaire de 20 repas successifs, les options végétariennes servies dans votre
                      établissement sont des plats à base de :
                    </label>
                    <div class="mt-4 mb-8" style="border-bottom: solid 1px #EEE;">
                      <div
                        class="d-flex py-2"
                        style="border-top: solid 1px #EEE;"
                        v-for="category in categories"
                        :key="category.htmlId"
                      >
                        <label
                          class="body-2 grey--text text--darken-3 pr-2"
                          :style="$vuetify.breakpoint.mdAndUp ? 'width: 35%;' : 'width: 70%;'"
                          :for="`${category.htmlId}-${item.value}`"
                        >
                          {{ category.label }}
                        </label>
                        <div class="d-flex">
                          <v-text-field
                            validate-on-blur
                            hide-details="auto"
                            solo
                            dense
                            v-model.number="expe[`${category.fieldName}${item.value}`]"
                            :rules="[
                              validators.nonNegativeOrEmpty,
                              validators.lteSumValue(
                                self[`compositionValidationFields${item.value}`],
                                20,
                                compositionSumErrorMessage
                              ),
                            ]"
                            :id="`${category.htmlId}-${item.value}`"
                          ></v-text-field>
                          <div class="my-auto ml-2">/20</div>
                        </div>
                        <v-spacer v-if="$vuetify.breakpoint.mdAndUp"></v-spacer>
                      </div>
                    </div>

                    <!-- Gaspillage évolution -->
                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium"
                      :for="`waste-evolution-${item.value}`"
                    >
                      Constatez-vous plus de gaspillage avec les options végétariennes ?
                    </label>
                    <v-radio-group
                      :id="`waste-evolution-${item.value}`"
                      v-model="expe[`wasteEvolution${item.value}`]"
                      class="mb-2"
                    >
                      <v-radio
                        v-for="wasteEvolutionItem in wasteEvolution"
                        :value="wasteEvolutionItem.value"
                        :key="wasteEvolutionItem.value"
                      >
                        <template v-slot:label>
                          <span class="body-2 grey--text text--darken-3">{{ wasteEvolutionItem.label }}</span>
                        </template>
                      </v-radio>
                    </v-radio-group>

                    <!-- Gaspillage ressenti poucentage -->
                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium"
                      :for="`waste-evolution-percentage-${item.value}`"
                      v-if="!!expe[`wasteEvolution${item.value}`] && expe[`wasteEvolution${item.value}`] !== 'same'"
                    >
                      Écart du gaspillage en pourcentage
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.lteOrEmpty(100)]"
                      solo
                      dense
                      v-model.number="expe[`wasteEvolutionPercentage${item.value}`]"
                      append-icon="mdi-percent"
                      style="max-width: 150px"
                      class="mt-2 mb-8 body-2"
                      :id="`waste-evolution-percentage-${item.value}`"
                      v-if="!!expe[`wasteEvolution${item.value}`] && expe[`wasteEvolution${item.value}`] !== 'same'"
                    ></v-text-field>

                    <!-- Gaspillage -->
                    <label class="body-2 grey--text text--darken-3 font-weight-medium">
                      Résultats des pesées de gaspillage alimentaire sur au moins 3 jours consécutifs (en g/convive)
                    </label>
                    <div class="my-4" style="border-bottom: solid 1px #EEE;">
                      <div
                        class="d-flex py-2"
                        style="border-top: solid 1px #EEE;"
                        v-for="wasteItem in waste"
                        :key="wasteItem.htmlId"
                      >
                        <label
                          class="body-2 grey--text text--darken-3 pr-2"
                          :style="$vuetify.breakpoint.mdAndUp ? 'width: 55%;' : 'width: 70%;'"
                          :for="`${wasteItem.htmlId}-${item.value}`"
                        >
                          {{ wasteItem.label }}
                        </label>
                        <div>
                          <v-text-field
                            validate-on-blur
                            hide-details="auto"
                            solo
                            dense
                            v-model.number="expe[`${wasteItem.fieldName}${item.value}`]"
                            :id="`${wasteItem.htmlId}-${item.value}`"
                          ></v-text-field>
                        </div>
                        <v-spacer v-if="$vuetify.breakpoint.mdAndUp"></v-spacer>
                      </div>
                    </div>

                    <!-- Attendance évolution -->
                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium"
                      :for="`attendance-evolution-${item.value}`"
                    >
                      Constatez-vous une évolution de la fréquentation depuis l'introduction de l'option végétarienne
                      quotidienne ?
                    </label>
                    <v-radio-group
                      :id="`attendance-evolution-${item.value}`"
                      v-model="expe[`attendanceEvolution${item.value}`]"
                      class="mb-2"
                    >
                      <v-radio
                        v-for="attendanceEvolutionItem in attendanceEvolution"
                        :value="attendanceEvolutionItem.value"
                        :key="attendanceEvolutionItem.value"
                      >
                        <template v-slot:label>
                          <span class="body-2 grey--text text--darken-3">{{ attendanceEvolutionItem.label }}</span>
                        </template>
                      </v-radio>
                    </v-radio-group>

                    <!-- Attendance ressenti poucentage -->
                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium"
                      :for="`attendance-evolution-percentage-${item.value}`"
                      v-if="
                        !!expe[`attendanceEvolution${item.value}`] &&
                          expe[`attendanceEvolution${item.value}`] !== 'same'
                      "
                    >
                      Écart de la fréquentation en pourcentage
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.lteOrEmpty(100)]"
                      solo
                      dense
                      v-model.number="expe[`attendanceEvolutionPercentage${item.value}`]"
                      append-icon="mdi-percent"
                      style="max-width: 150px"
                      class="mt-2 mb-8 body-2"
                      :id="`attendance-evolution-percentage-${item.value}`"
                      v-if="
                        !!expe[`attendanceEvolution${item.value}`] &&
                          expe[`attendanceEvolution${item.value}`] !== 'same'
                      "
                    ></v-text-field>

                    <!-- Coût moyen / assiette végétarien -->
                    <label class="body-2 grey--text text--darken-3 font-weight-medium d-block mb-4">
                      Le coût matière moyen des menus végétariens est-il supérieur aux autres menus ?
                    </label>
                    <label class="body-2 grey--text text--darken-3" :for="`vegetarian-cost-${item.value}`">
                      Coût moyen du repas végétarien (en € / assiette)
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.nonNegativeOrEmpty]"
                      solo
                      dense
                      v-model.number="expe[`vegetarianCost${item.value}`]"
                      append-icon="mdi-currency-eur"
                      style="max-width: 150px"
                      class="mt-2 mb-4 body-2"
                      :id="`vegetarian-cost-${item.value}`"
                    ></v-text-field>

                    <!-- Coût moyen / assiette non-végétarien -->
                    <label class="body-2 grey--text text--darken-3" :for="`non-vegetarian-cost-${item.value}`">
                      Coût moyen du repas non-végétarien (en € / assiette)
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.nonNegativeOrEmpty]"
                      solo
                      dense
                      v-model.number="expe[`nonVegetarianCost${item.value}`]"
                      append-icon="mdi-currency-eur"
                      style="max-width: 150px"
                      class="mt-2 mb-8 body-2"
                      :id="`non-vegetarian-cost-${item.value}`"
                    ></v-text-field>

                    <!-- Cost evolution -->
                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium"
                      :for="`cost-evolution-${item.value}`"
                    >
                      Comment le coût facturé aux familles a-t-il évolué depuis la mise en place du menu quotidien ?
                    </label>
                    <v-radio-group
                      :id="`cost-evolution-${item.value}`"
                      v-model="expe[`costEvolution${item.value}`]"
                      class="mb-2"
                    >
                      <v-radio
                        v-for="costEvolutionItem in costEvolution"
                        :value="costEvolutionItem.value"
                        :key="costEvolutionItem.value"
                      >
                        <template v-slot:label>
                          <span class="body-2 grey--text text--darken-3">{{ costEvolutionItem.label }}</span>
                        </template>
                      </v-radio>
                    </v-radio-group>

                    <!-- Cost evolution percentage -->
                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium"
                      :for="`cost-evolution-percentage-${item.value}`"
                      v-if="!!expe[`costEvolution${item.value}`] && expe[`costEvolution${item.value}`] !== 'same'"
                    >
                      Écart du coût facturé aux familles
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.lteOrEmpty(100)]"
                      solo
                      dense
                      v-model.number="expe[`costEvolutionPercentage${item.value}`]"
                      append-icon="mdi-percent"
                      style="max-width: 150px"
                      class="mt-2 mb-8 body-2"
                      :id="`cost-evolution-percentage-${item.value}`"
                      v-if="!!expe[`costEvolution${item.value}`] && expe[`costEvolution${item.value}`] !== 'same'"
                    ></v-text-field>

                    <!-- Satisfaction convive -->
                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium"
                      :for="`satisfaction-guests-${item.value}`"
                    >
                      Satisfaction moyenne des convives
                    </label>
                    <v-rating
                      v-model.number="expe[`satisfactionGuests${item.value}`]"
                      color="primary"
                      empty-icon="mdi-star-outline"
                      full-icon="mdi-star"
                      class="mt-2 mb-4 body-2"
                      :id="`satisfaction-guests-${item.value}`"
                      background-color="grey"
                      length="5"
                      hover
                    ></v-rating>

                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium d-block mb-4"
                      :for="`satisfaction-guests-reasons-${item.value}`"
                    >
                      Quelles sont les principales raisons évoquées par les convives ?
                    </label>
                    <v-checkbox
                      hide-details="auto"
                      class="my-2 mt-0"
                      v-model="expe[`satisfactionGuestsReasons${item.value}`]"
                      :multiple="true"
                      v-for="reason in satisfactionReasons"
                      :value="reason.value"
                      :key="`guests-${reason.value}`"
                    >
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3">{{ reason.label }}</span>
                      </template>
                    </v-checkbox>

                    <!-- Satisfaction staff -->
                    <label
                      class="body-2 grey--text text--darken-3 mt-8 d-block font-weight-medium"
                      :for="`satisfaction-staff-${item.value}`"
                    >
                      Satisfaction moyenne du personnel
                    </label>
                    <v-rating
                      v-model.number="expe[`satisfactionStaff${item.value}`]"
                      color="primary"
                      empty-icon="mdi-star-outline"
                      full-icon="mdi-star"
                      class="mt-2 mb-4 body-2"
                      :id="`satisfaction-staff-${item.value}`"
                      background-color="grey"
                      length="5"
                      hover
                    ></v-rating>

                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium d-block mb-4"
                      :for="`satisfaction-staff-reasons-${item.value}`"
                    >
                      Quelles sont les principales raisons évoquées par le personnel ?
                    </label>
                    <v-checkbox
                      hide-details="auto"
                      class="my-2 mt-0"
                      v-model="expe[`satisfactionStaffReasons${item.value}`]"
                      :multiple="true"
                      v-for="reason in satisfactionReasons"
                      :value="reason.value"
                      :key="`staff-${reason.value}`"
                    >
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3">{{ reason.label }}</span>
                      </template>
                    </v-checkbox>

                    <v-divider class="mt-6"></v-divider>
                    <!-- Recipees -->
                    <v-checkbox hide-details="auto" class="my-4" v-model="expe[`hasUsedRecipeeDocuments${item.value}`]">
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3 font-weight-medium">
                          Avez-vous utilisé le livret de recettes végétariennes publié par le CNRC ou par d’autres
                          organismes ?
                        </span>
                      </template>
                    </v-checkbox>

                    <v-divider class="mt-6"></v-divider>
                    <!-- Formation -->
                    <v-checkbox hide-details="auto" class="my-4" v-model="expe[`training${item.value}`]">
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3 font-weight-medium">
                          Votre établissement a-t-il mis en place une formation spécifique des cuisiniers ou
                          gestionnaires sur les menus végétariens ?
                        </span>
                      </template>
                    </v-checkbox>
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
  name: "ExpeVegetarian",
  props: {
    canteen: Object,
  },
  data() {
    return {
      formIsValid: true,
      expe: null,
      originalExpe: null,
      vegetarianDailyStartDateMenu: false,
      launchDateMenu: false,
      tab: null,
      compositionSumErrorMessage: "La somme ne doit pas dépasser 20 repas",
      tabs: [
        { label: "À date", value: "T0" },
        { label: "En décembre 2022", value: "T1" },
      ],
      percentageFields: [
        "vegetarianMenuPercentageT0",
        "vegetarianMenuPercentageT1",
        "attendanceEvolutionPercentageT0",
        "attendanceEvolutionPercentageT1",
        "wasteEvolutionPercentageT0",
        "wasteEvolutionPercentageT1",
        "costEvolutionPercentageT0",
        "costEvolutionPercentageT1",
      ],
      categories: [
        { label: "Œufs (omelette, œuf dur...)", htmlId: "eggs_composition", fieldName: "eggsComposition" },
        {
          label: "Fromage (pané fromager, tartiflette sans lardons...)",
          htmlId: "cheese-composition",
          fieldName: "cheeseComposition",
        },
        {
          label: "Galettes/boulettes/nuggets fait maison à base de soja",
          htmlId: "soy-composition-home-made",
          fieldName: "soyCompositionHomeMade",
        },
        {
          label: "Galettes/boulettes/nuggets prêt à l’emploi à base de soja",
          htmlId: "soy-composition-ready",
          fieldName: "soyCompositionReady",
        },
        {
          label: "Galettes/boulettes/nuggets fait maison sans soja",
          htmlId: "soyless-composition-home-made",
          fieldName: "soylessCompositionHomeMade",
        },
        {
          label: "Galettes/boulettes/nuggets prêt à l’emploi sans soja",
          htmlId: "soyless-composition-ready",
          fieldName: "soylessCompositionReady",
        },
        {
          label: "Plats à base de céréales, légumineuses et légumes (dahls, chili végétarien…)",
          htmlId: "cereal-legume-composition",
          fieldName: "cerealLegumeComposition",
        },
      ],
      waste: [
        {
          label: "Menus végétariens : Moyenne des pesées des excédents présentés aux convives et non servis",
          htmlId: "waste-vegetarian-not-served",
          fieldName: "wasteVegetarianNotServed",
        },
        {
          label: "Menus végétariens : Moyenne des pesées des restes des assiettes",
          htmlId: "waste-vegetarian-components",
          fieldName: "wasteVegetarianComponents",
        },
        {
          label: "Menus non-végétariens : Moyenne des pesées des excédents présentés aux convives et non servis",
          htmlId: "waste-non-vegetarian-not-served",
          fieldName: "wasteNonVegetarianNotServed",
        },
        {
          label: "Menus non-végétariens : Moyenne des pesées des restes des assiettes",
          htmlId: "waste-non-vegetarian-components",
          fieldName: "wasteNonVegetarianComponents",
        },
      ],
      wasteEvolution: [
        {
          label: "Oui, il y a plus de gaspillage",
          value: "higher",
        },
        {
          label: "Non, il y a moins de gaspillage",
          value: "lower",
        },
        {
          label: "Pas de différence notable",
          value: "same",
        },
      ],
      costEvolution: [
        {
          label: "Le coût a augmenté",
          value: "higher",
        },
        {
          label: "Le coût a diminué",
          value: "lower",
        },
        {
          label: "Pas de différence notable",
          value: "same",
        },
      ],
      attendanceEvolution: [
        {
          label: "La fréquentation a augmenté",
          value: "higher",
        },
        {
          label: "La fréquentation a diminué",
          value: "lower",
        },
        {
          label: "Pas de différence notable",
          value: "same",
        },
      ],
      satisfactionReasons: [
        {
          label: "Liberté de choix (régime, culte...)",
          value: "choice",
        },
        {
          label: "Goût et texture",
          value: "taste",
        },
        {
          label: "Nouveauté",
          value: "novelty",
        },
        {
          label: "Variété des recettes",
          value: "variety",
        },
        {
          label: "Méconnaissance",
          value: "ignorance",
        },
        {
          label: "Opposition de principe",
          value: "reject",
        },
        {
          label: "Impact sur la santé",
          value: "health",
        },
        {
          label: "Impact sur l'environnement",
          value: "environment",
        },
      ],
    }
  },
  computed: {
    validators() {
      return validators
    },
    today() {
      const today = new Date()
      return today.toISOString().split("T")[0]
    },
    isNewExpe() {
      return this.expe && !this.expe.id
    },
    isLoading() {
      return this.$store.state.expeLoadingStatus === Constants.LoadingStatus.LOADING
    },

    showSpinner() {
      return this.isLoading && !this.expe
    },
    compositionValidationFieldsT0() {
      if (!this.expe) return []
      return this.getCompositionValidationFields("T0")
    },
    compositionValidationFieldsT1() {
      if (!this.expe) return []
      return this.getCompositionValidationFields("T1")
    },
    self() {
      // Kludge needed to dynamically access computed properties from the template.
      // https://forum.vuejs.org/t/dynamically-modelling-a-computed-property/73723/4
      return this
    },
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
      const method = this.isNewExpe ? "createVegetarianExpe" : "updateVegetarianExpe"
      const payload = treatOutboundPercentageValues(
        this.isNewExpe ? this.expe : getObjectDiff(this.originalExpe, this.expe),
        this.percentageFields
      )
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
    getCompositionValidationFields(time) {
      return [
        this.expe[`cheeseComposition${time}`],
        this.expe[`soyCompositionHomeMade${time}`],
        this.expe[`soyCompositionReady${time}`],
        this.expe[`soylessComposition${time}`],
        this.expe[`soylessCompositionReady${time}`],
        this.expe[`cerealLegumeComposition${time}`],
      ]
    },
  },
  mounted() {
    this.$store
      .dispatch("fetchVegetarianExpe", { canteen: this.canteen })
      .then((response) => {
        this.originalExpe = treatInboundPercentageValues(response || {}, this.percentageFields)
        this.expe = JSON.parse(JSON.stringify(this.originalExpe))
      })
      .catch((e) => {
        console.log(e)
        this.$store.dispatch("notifyServerError", e)
      })
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

.v-form >>> textarea::placeholder {
  color: #444;
}
</style>
