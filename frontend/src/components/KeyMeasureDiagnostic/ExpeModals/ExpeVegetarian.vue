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
          Pour participer à l'expérimentation d'une option végétarienne quotidienne, telle que prévue par la loi Climat
          et résilience, nous vous proposons de répondre à quelques questions sur la mise en œuvre de l'option
          végétarienne quotidienne dans votre établissement. En particulier, les questions portent sur les catégories de
          plats végétariens servis, l'impact sur les pesées de gaspillage alimentaire, la fréquentation, la satisfaction
          des convives et le coût des repas.
        </p>
        <p>
          Il est également possible de participer si une option végétarienne quotidienne est déjà mise en place dans
          votre établissement.
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
                id="launch-date"
                class="mt-2 mb-4"
              ></v-text-field>
            </template>

            <v-date-picker v-model="expe.experimentationStartDate" locale="fr-FR"></v-date-picker>
          </v-menu>

          <!-- Menu Type before the XP -->
          <label class="body-2 grey--text text--darken-3" for="menu-type-before-xp">
            Avant la mise en place de l’expérimentation, mon établissement propose chaque jour :
          </label>
          <v-radio-group id="menu-type-before-xp" v-model="expe.menuTypeBeforeXp" class="mt-1">
            <v-radio v-for="option in menuOptions" :value="option.value" :key="option.value">
              <template v-slot:label>
                <span class="body-2 grey--text text--darken-3">{{ option.label }}</span>
              </template>
            </v-radio>
          </v-radio-group>

          <!-- Reservation needed? -->
          <label class="body-2 grey--text text--darken-3" for="vege-menu-reservation">
            L’option végétarienne quotidienne :
          </label>
          <v-radio-group id="vege-menu-reservation" v-model="expe.vegeMenuReservation" class="mt-1">
            <v-radio v-for="option in reservationOptions" :value="option.value" :key="option.value">
              <template v-slot:label>
                <span class="body-2 grey--text text--darken-3">{{ option.label }}</span>
              </template>
            </v-radio>
          </v-radio-group>

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
                      Quel est le taux de prise des menus végétariens par rapport aux menus non-végétariens en cas de
                      choix multiple, en moyenne sur 20 repas successifs ?
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.nonNegativeOrEmpty, validators.lteOrEmpty(100)]"
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
                      Les plans alimentaires sont établis sur 20 repas successifs, soit 4 semaines de 5 jours. Par
                      exemple, une fréquence de 4/20 correspond à une fois par semaine, 8/20 à deux fois par semaine.
                      <br />
                      Dans votre plan alimentaire, les 20 options végétariennes servies sur 20 repas successifs sont à
                      base de :
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
                            @blur="validateCompositionFields()"
                            hide-details="auto"
                            solo
                            dense
                            v-model.number="expe[`${category.fieldName}${item.value}`]"
                            :rules="compositionRules(category.fieldName, item.value)"
                            :id="`${category.htmlId}-${item.value}`"
                            suffix="/20"
                            :hint="compositionHint(category.fieldName, item.value)"
                            :persistent-hint="!!compositionHint(category.fieldName, item.value)"
                          ></v-text-field>
                        </div>
                        <v-spacer v-if="$vuetify.breakpoint.mdAndUp"></v-spacer>
                      </div>
                    </div>

                    <!-- Wholegrain percentage -->
                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium"
                      :for="`wholegrain-cereal-percentage-${item.value}`"
                    >
                      Parmi les plats à base de céréales, quelle part représentent les céréales complètes et
                      semi-complètes ?
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.nonNegativeOrEmpty, validators.lteOrEmpty(100)]"
                      solo
                      dense
                      v-model.number="expe[`wholegrainCerealPercentage${item.value}`]"
                      append-icon="mdi-percent"
                      style="max-width: 150px"
                      class="mt-2 mb-8 body-2"
                      :id="`wholegrain-cereal-percentage-${item.value}`"
                    ></v-text-field>

                    <!-- Waste evolution from start to date, T0 only -->
                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium"
                      for="waste_evolution_start_to_date_t0"
                      v-if="expe.hasDailyVegetarianOffer && item.value === 'T0'"
                    >
                      Avez-vous constaté une évolution du gaspillage avec l'option végétarienne entre le moment de sa
                      mise en place et aujourd'hui ?
                    </label>
                    <v-radio-group
                      id="waste_evolution_start_to_date_t0"
                      v-model="expe.wasteEvolutionStartToDateT0"
                      class="mt-1"
                      v-if="expe.hasDailyVegetarianOffer && item.value === 'T0'"
                    >
                      <v-radio v-for="option in wasteEvolutionToDate" :value="option.value" :key="option.value">
                        <template v-slot:label>
                          <span class="body-2 grey--text text--darken-3">{{ option.label }}</span>
                        </template>
                      </v-radio>
                    </v-radio-group>

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
                      Ecart du gaspillage en pourcentage (ex : 30% de gaspillage en plus/en moins avec l'option
                      végétarienne)
                    </label>
                    <v-text-field
                      validate-on-blur
                      hide-details="auto"
                      :rules="[validators.nonNegativeOrEmpty, validators.lteOrEmpty(100)]"
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
                            :suffix="$vuetify.breakpoint.xs ? 'g' : 'g/convive'"
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
                      :rules="[validators.nonNegativeOrEmpty, validators.lteOrEmpty(100)]"
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

                    <label class="body-2 grey--text text--darken-3 font-weight-medium d-block mb-4">
                      Le coût matière moyen des menus végétariens est-il supérieur aux autres menus ?
                    </label>

                    <!-- Qualitative coût végétarien -->
                    <label class="body-2 grey--text text--darken-3" :for="`vegetarian-cost-qualitative-${item.value}`">
                      En moyenne, le coût matière des plats végétariens est :
                    </label>
                    <v-radio-group
                      :id="`vegetarian-cost-qualitative-${item.value}`"
                      v-model="expe[`vegetarianCostQualitative${item.value}`]"
                      class="mt-1 mb-4"
                      hide-details="auto"
                    >
                      <v-radio v-for="option in vegetarianCost" :value="option.value" :key="option.value">
                        <template v-slot:label>
                          <span class="body-2 grey--text text--darken-3">{{ option.label }}</span>
                        </template>
                      </v-radio>
                    </v-radio-group>

                    <!-- Costs savings reinvested -->
                    <v-checkbox
                      :id="`cost-savings-reinvested-${item.value}`"
                      v-model="expe[`costSavingsReinvested${item.value}`]"
                      v-if="expe[`vegetarianCostQualitative${item.value}`] === 'lower'"
                    >
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3">
                          Les économies réalisées ont été réinvesties pour augmenter la part de produits durables et de
                          qualité (Bio, SIQO…)
                        </span>
                      </template>
                    </v-checkbox>

                    <!-- Coût moyen / assiette végétarien -->
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
                      Y a-t-il eu une évolution du tarif par repas facturé aux familles depuis la mise en place de
                      l’option végétarienne quotidienne ?
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
                      :rules="[validators.nonNegativeOrEmpty, validators.lteOrEmpty(100)]"
                      solo
                      dense
                      v-model.number="expe[`costEvolutionPercentage${item.value}`]"
                      append-icon="mdi-percent"
                      style="max-width: 150px"
                      class="mt-2 mb-8 body-2"
                      :id="`cost-evolution-percentage-${item.value}`"
                      v-if="!!expe[`costEvolution${item.value}`] && expe[`costEvolution${item.value}`] !== 'same'"
                    ></v-text-field>

                    <v-checkbox v-model="expe[`costPerMealVg${item.value}`]" :id="`cost-per-meal-${item.value}`">
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3">
                          Le tarif par repas est moins cher pour l’option végétarienne
                        </span>
                      </template>
                    </v-checkbox>

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
                      v-for="reason in satisfactionReasonsGuests"
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
                      Satisfaction moyenne du personnel (en cuisine et personnel encadrant)
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
                      v-for="reason in satisfactionReasonsStaff"
                      :value="reason.value"
                      :key="`staff-${reason.value}`"
                    >
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3">{{ reason.label }}</span>
                      </template>
                    </v-checkbox>

                    <v-divider class="mt-6"></v-divider>
                    <!-- Recipes -->
                    <v-checkbox hide-details="auto" class="my-4" v-model="expe[`hasUsedRecipeDocuments${item.value}`]">
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3 font-weight-medium">
                          Mon établissement a utilisé un livret de recettes végétariennes (CNRC ou autres organismes)
                        </span>
                      </template>
                    </v-checkbox>

                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium d-block mb-4"
                      :for="`recipe-document-${item.value}`"
                      v-if="expe[`hasUsedRecipeDocuments${item.value}`]"
                    >
                      Précisez, quel livret de recette avez vous utilisé ?
                    </label>
                    <v-textarea
                      v-if="expe[`hasUsedRecipeDocuments${item.value}`]"
                      solo
                      :id="`recipe-document-${item.value}`"
                      v-model="expe[`recipeDocument${item.value}`]"
                      rows="2"
                      hide-details="auto"
                    ></v-textarea>

                    <v-divider class="mt-6"></v-divider>
                    <!-- Formation -->
                    <v-checkbox hide-details="auto" class="my-4" v-model="expe[`training${item.value}`]">
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3 font-weight-medium">
                          Mon établissement a mis en place une formation spécifique des cuisiniers ou gestionnaires sur
                          les menus végétariens
                        </span>
                      </template>
                    </v-checkbox>

                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium d-block mb-4"
                      :for="`training-type-${item.value}`"
                      v-if="expe[`training${item.value}`]"
                    >
                      Précisez, quel type de formation ?
                    </label>
                    <v-textarea
                      v-if="expe[`training${item.value}`]"
                      solo
                      :id="`training-type-${item.value}`"
                      v-model="expe[`trainingType${item.value}`]"
                      rows="2"
                      hide-details="auto"
                    ></v-textarea>

                    <v-divider class="my-6"></v-divider>
                    <!-- Difficulties -->
                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium"
                      :for="`difficulties-daily-option-${item.value}`"
                    >
                      Quels sont les principaux freins rencontrés à la mise en place de l’option végétarienne
                      quotidienne ?
                    </label>

                    <v-checkbox
                      hide-details="auto"
                      class="my-2 mt-0"
                      v-model="expe[`difficultiesDailyOption${item.value}`]"
                      :multiple="true"
                      v-for="option in difficultiesOptions"
                      :value="option.value"
                      :key="option.value"
                    >
                      <template v-slot:label>
                        <span class="body-2 grey--text text--darken-3">{{ option.label }}</span>
                      </template>
                    </v-checkbox>

                    <label
                      class="body-2 grey--text text--darken-3 font-weight-medium d-block mb-4"
                      :for="`difficulties-daily-option-details-${item.value}`"
                      v-if="
                        expe[`difficultiesDailyOption${item.value}`] &&
                          expe[`difficultiesDailyOption${item.value}`].indexOf &&
                          expe[`difficultiesDailyOption${item.value}`].indexOf('other') > -1
                      "
                    >
                      Précisez
                    </label>
                    <v-textarea
                      v-if="
                        expe[`difficultiesDailyOption${item.value}`] &&
                          expe[`difficultiesDailyOption${item.value}`].indexOf &&
                          expe[`difficultiesDailyOption${item.value}`].indexOf('other') > -1
                      "
                      solo
                      :id="`difficulties-daily-option-details-${item.value}`"
                      v-model="expe[`difficultiesDailyOptionDetails${item.value}`]"
                      rows="2"
                    ></v-textarea>
                  </v-card-text>
                </v-card>
              </v-tab-item>
            </v-tabs-items>
          </div>

          <!-- Keep me informed -->
          <v-checkbox v-model="expe.shareResults">
            <template v-slot:label>
              <span class="body-2 grey--text text--darken-3">
                Je souhaite être informé des conclusions de l'évaluation de l'expérimentation
              </span>
            </template>
          </v-checkbox>
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
      menuOptions: [
        { label: "Une offre à choix multiples", value: "multiple" },
        { label: "Un menu unique pour tous les convives", value: "unique" },
      ],
      reservationOptions: [
        { label: "Est proposée chaque jour aux convives librement", value: "open" },
        { label: "Fait l'objet d'une préinscription en amont", value: "reservation_needed" },
      ],
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
        "wholegrainCerealPercentageT0",
        "wholegrainCerealPercentageT1",
      ],
      categories: [
        { label: "Œufs (omelette, œuf dur...)", htmlId: "eggs_composition", fieldName: "eggsComposition" },
        {
          label: "Fromage (pané fromager, tartiflette sans lardons, ravioles au fromage...)",
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
        {
          label: "Féculents, légumes et sauces (pâtes sauce tomate, lasagnes végétariennes, riz ratatouille...)",
          htmlId: "starch-legume-composition",
          fieldName: "starchLegumeComposition",
        },
      ],
      waste: [
        {
          label: "Plat principal végétarien : Moyenne des pesées des excédents présentés aux convives et non servis",
          htmlId: "waste-vegetarian-not-served",
          fieldName: "wasteVegetarianNotServed",
        },
        {
          label: "Plat principal végétarien : Moyenne des pesées des restes des assiettes",
          htmlId: "waste-vegetarian-components",
          fieldName: "wasteVegetarianComponents",
        },
        {
          label:
            "Plat principal non-végétarien : Moyenne des pesées des excédents présentés aux convives et non servis",
          htmlId: "waste-non-vegetarian-not-served",
          fieldName: "wasteNonVegetarianNotServed",
        },
        {
          label: "Plat principal non-végétarien : Moyenne des pesées des restes des assiettes",
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
      wasteEvolutionToDate: [
        {
          label: "Oui, le gaspillage des plats végétariens a augmenté depuis la mise en place",
          value: "higher",
        },
        {
          label: "Oui, le gaspillage des plats végétariens a diminué depuis la mise en place",
          value: "lower",
        },
        {
          label: "Non, le gaspillage des plats végétariens n'a pas évolué",
          value: "same",
        },
      ],
      costEvolution: [
        {
          label: "Le tarif par repas a augmenté",
          value: "higher",
        },
        {
          label: "Le tarif par repas a diminué",
          value: "lower",
        },
        {
          label: "Le tarif par repas n’a pas changé",
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
      vegetarianCost: [
        {
          label: "Plus que cher que les plats non-végétariens",
          value: "higher",
        },
        {
          label: "Moins cher que les plats non-végétariens",
          value: "lower",
        },
        {
          label: "Equivalent aux plats non-végétariens",
          value: "same",
        },
      ],
      satisfactionReasonsStaff: [
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
          label: "Méconnaissance (recettes, méthodes de préparation, utilisation du matériel)",
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
        {
          label: "Manque de matériel adapté",
          value: "no_equipment",
        },
      ],
      satisfactionReasonsGuests: [
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
          label: "Méconnaissance (recettes, méthodes de préparation, utilisation du matériel)",
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
        {
          label: "Problèmes de digestion",
          value: "digestion",
        },
      ],
      difficultiesOptions: [
        {
          label: "Difficultés d'accès à la formation",
          value: "formation",
        },
        {
          label: "Difficultés d'approvisionnement",
          value: "appro",
        },
        {
          label: "Manque de recettes",
          value: "recipes",
        },
        {
          label: "Surcoût des produits",
          value: "cost",
        },
        {
          label: "Réaction des convives",
          value: "clients",
        },
        {
          label: "Surcharge de travail pour le personnel",
          value: "overwork",
        },
        {
          label: "Autre",
          value: "other",
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
    lastCategoryName() {
      return this.categories[this.categories.length - 1].fieldName
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
      const sentExpe = this.isNewExpe
        ? JSON.parse(JSON.stringify(this.expe))
        : getObjectDiff(this.originalExpe, this.expe)
      const payload = treatOutboundPercentageValues(sentExpe, this.percentageFields)
      // this handles the DRF throwing an error at an empty string but not a null value
      Object.keys(payload).forEach((key) => {
        if ((key.endsWith("T0") || key.endsWith("T1")) && payload[key] === "") {
          payload[key] = null
        }
      })
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
        this.expe[`eggsComposition${time}`],
        this.expe[`cheeseComposition${time}`],
        this.expe[`soyCompositionHomeMade${time}`],
        this.expe[`soyCompositionReady${time}`],
        this.expe[`soylessCompositionHomeMade${time}`],
        this.expe[`soylessCompositionReady${time}`],
        this.expe[`cerealLegumeComposition${time}`],
        this.expe[`starchLegumeComposition${time}`],
      ]
    },
    validateCompositionFields() {
      // this hack only works because the other fields are all optional
      this.$refs.form.validate()
    },
    compositionRules(name, time) {
      let rules = [validators.nonNegativeOrEmpty]
      if (name === this.lastCategoryName) {
        rules.push(
          validators.lteSumValue(this[`compositionValidationFields${time}`], 20, this.compositionSumErrorMessage)
        )
      }
      return rules
    },
    compositionHint(name, time) {
      if (name === this.lastCategoryName) {
        let sum = 0
        this[`compositionValidationFields${time}`].forEach((v) => {
          if (v && Number(v)) sum += Number(v)
        })
        return `${sum} repas renseigné${sum === 1 ? "" : "s"}`
      }
      return null
    },
  },
  mounted() {
    this.originalExpe = treatInboundPercentageValues({}, this.percentageFields)
    this.expe = JSON.parse(JSON.stringify(this.originalExpe))
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
