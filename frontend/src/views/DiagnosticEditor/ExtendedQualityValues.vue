<template>
  <div>
    <!-- Input used for cross-field validation : https://github.com/vuetifyjs/vuetify/issues/8698 -->
    <v-input hidden :rules="[checkTotal]" hide-details></v-input>

    <label :for="'total-' + diagnostic.year" class="body-2">
      La valeur (en HT) de mes achats alimentaires total
    </label>

    <DsfrCurrencyField
      :id="'total-' + diagnostic.year"
      v-model.number="diagnostic.valueTotalHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      :messages="totalError ? [errorMessage] : undefined"
      @blur="checkTotal"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueTotalHt"
      @autofill="checkTotal"
      purchaseType="totaux"
      :amount="purchasesSummary.total"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />

    <label :for="'meat-poultry-' + diagnostic.year" class="body-2 mt-4 d-block">
      <div class="d-inline-flex mr-2">
        <v-icon size="30" color="brown">
          mdi-food-steak
        </v-icon>
        <v-icon size="30" color="brown">
          mdi-food-drumstick
        </v-icon>
      </div>
      La valeur (en HT) des mes achats en viandes et volailles fraiches ou surgelées total
    </label>

    <DsfrCurrencyField
      :id="'meat-poultry-' + diagnostic.year"
      v-model.number="diagnostic.valueMeatPoultryHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="meatError"
      :messages="meatError ? [errorMessage] : undefined"
      @blur="checkTotal"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueMeatPoultryHt"
      @autofill="checkTotal"
      purchaseType="totaux viandes et volailles"
      :amount="purchasesSummary.meatPoultryTotal"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />

    <label :for="'fish-' + diagnostic.year" class="body-2 mt-4 d-block">
      <div class="d-inline-flex mr-2">
        <v-icon size="30" color="blue">
          mdi-fish
        </v-icon>
      </div>
      La valeur (en HT) des mes achats en poissons, produits de la mer et de l'aquaculture total
    </label>

    <DsfrCurrencyField
      :id="'fish-' + diagnostic.year"
      v-model.number="diagnostic.valueFishHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="fishError"
      :messages="fishError ? [errorMessage] : undefined"
      @blur="checkTotal"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field mt-2' : 'mt-2'"
    />
    <PurchaseHint
      v-if="displayPurchaseHints"
      v-model="diagnostic.valueFishHt"
      @autofill="checkTotal"
      purchaseType="totaux de poissons, produits de la mer et de l'aquaculture"
      :amount="purchasesSummary.fishTotal"
      :class="$vuetify.breakpoint.mdAndUp ? 'narrow-field' : ''"
    />

    <br />
    <div v-for="(group, groupId) in characteristicGroups" :key="groupId">
      <p v-if="group.text" class="caption mb-0 ml-2">{{ group.text }}</p>
      <v-row align="center" class="pr-2 mb-2 ml-1">
        <v-col cols="6" sm="8" md="9" class="pl-0 pb-1">
          <v-progress-linear :value="percentageCompletion[groupId]" rounded height="6"></v-progress-linear>
        </v-col>
        <v-col class="text-right pb-1">
          <p class="caption my-0">{{ fieldsCompleted[groupId] }} / {{ fieldCount[groupId] }} champs remplis</p>
        </v-col>
      </v-row>
      <v-expansion-panels class="mt-1 mb-4">
        <v-expansion-panel v-for="cId in group.characteristics" :key="cId">
          <v-expansion-panel-header>
            <template v-slot:default="{ open }">
              <v-row align="center">
                <v-col
                  cols="2"
                  class="py-0 my-1 pr-0 d-flex align-center justify-center"
                  style="display: block; height: 30px;"
                  v-if="$vuetify.breakpoint.smAndUp"
                >
                  <LogoBio v-if="cId === 'BIO'" style="max-width: 100%; max-height: 100%;" />
                  <div
                    v-for="label in qualityLabels(cId)"
                    :key="label.title || label.icon"
                    style="max-width: 100%; height: inherit;"
                  >
                    <img
                      v-if="label.src"
                      :src="`/static/images/quality-labels/${label.src}`"
                      :alt="label.title"
                      :title="label.title"
                      style="max-width: 100%; height: 100%;"
                    />
                    <v-icon class="mt-1" :color="label.color" v-else-if="label.icon">
                      {{ label.icon }}
                    </v-icon>
                  </div>
                </v-col>
                <v-col>
                  {{ characteristics[cId].text }}
                  <span v-if="cId === 'LOCAL'">(suivant votre propre définition)</span>
                </v-col>
                <v-col cols="3" class="text--secondary text-right pr-4">
                  <v-fade-transition leave-absolute>
                    <span v-if="!open" key="0">
                      {{ percentage(cId) }}
                    </span>
                  </v-fade-transition>
                </v-col>
              </v-row>
            </template>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-row class="mb-2">
              <v-col v-for="(family, fId) in families" :key="fId" cols="12" md="6">
                <label :for="inputHtmlId(fId, cId)" class="body-2">
                  {{ family.text }}
                </label>

                <DsfrCurrencyField
                  :id="inputHtmlId(fId, cId)"
                  :rules="[
                    validators.nonNegativeOrEmpty,
                    validators.decimalPlaces(2),
                    validators.lteOrEmpty(diagnostic.valueTotalHt),
                  ]"
                  solo
                  v-model.number="diagnostic[diagnosticKey(fId, cId)]"
                  :readonly="readonly"
                  :disabled="readonly"
                  class="mt-2"
                  @blur="checkTotal"
                />
                <PurchaseHint
                  v-if="displayPurchaseHints"
                  v-model="diagnostic[diagnosticKey(fId, cId)]"
                  :purchaseType="family.shortText + ' pour ce caractéristique'"
                  :amount="purchasesSummary[summaryKey(fId, cId)]"
                />
              </v-col>
            </v-row>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </div>
  </div>
</template>

<script>
import validators from "@/validators"
import Constants from "@/constants"
import LogoBio from "@/components/LogoBio"
import labels from "@/data/quality-labels.json"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import DsfrCurrencyField from "@/components/DsfrCurrencyField"

const DEFAULT_TOTAL_ERROR = "Le totale doit être plus que la somme des valeurs par label"
const DEFAULT_FAMILY_TOTAL_ERROR = "La somme des achats par famille ne peut pas excéder le total des achats"

export default {
  name: "ExtendedQualityValues",
  props: {
    originalDiagnostic: Object,
    purchasesSummary: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    LogoBio,
    PurchaseHint,
    DsfrCurrencyField,
  },
  data() {
    const characteristicGroups = Constants.TeledeclarationCharacteristicGroups
    return {
      errorType: undefined,
      errorMessage: "",
      families: Constants.ProductFamilies,
      characteristics: Constants.TeledeclarationCharacteristics,
      characteristicGroups,
      fieldCount: {
        egalim: characteristicGroups.egalim.fields.length,
        nonEgalim: characteristicGroups.nonEgalim.fields.length,
        outsideLaw: characteristicGroups.outsideLaw.fields.length,
      },
    }
  },
  computed: {
    validators() {
      return validators
    },
    diagnostic() {
      return this.originalDiagnostic
    },
    displayPurchaseHints() {
      return this.purchasesSummary && Object.values(this.purchasesSummary).some((x) => !!x) && !this.readonly
    },
    hasActiveTeledeclaration() {
      return this.diagnostic.teledeclaration && this.diagnostic.teledeclaration.status === "SUBMITTED"
    },
    fieldsCompleted() {
      let completed = {
        egalim: 0,
        nonEgalim: 0,
        outsideLaw: 0,
      }
      Object.entries(this.diagnostic).forEach(([field, value]) => {
        if (this.characteristicGroups.egalim.fields.indexOf(field) > -1) {
          completed.egalim += parseFloat(value, 10) >= 0 ? 1 : 0
        } else if (this.characteristicGroups.outsideLaw.fields.indexOf(field) > -1) {
          completed.outsideLaw += parseFloat(value, 10) >= 0 ? 1 : 0
        } else if (this.characteristicGroups.nonEgalim.fields.indexOf(field) > -1) {
          completed.nonEgalim += parseFloat(value, 10) >= 0 ? 1 : 0
        }
      })
      return completed
    },
    percentageCompletion() {
      return {
        egalim: Math.round((this.fieldsCompleted.egalim / this.fieldCount.egalim) * 100),
        nonEgalim: Math.round((this.fieldsCompleted.nonEgalim / this.fieldCount.nonEgalim) * 100),
        outsideLaw: Math.round((this.fieldsCompleted.outsideLaw / this.fieldCount.outsideLaw) * 100),
      }
    },
    totalError() {
      return this.errorType === "FAMILY" || this.errorType === "TOTAL"
    },
    meatError() {
      return this.errorType === "FAMILY" || this.errorType === "MEAT"
    },
    fishError() {
      return this.errorType === "FAMILY" || this.errorType === "FISH"
    },
  },
  methods: {
    inputHtmlId(fId, cId) {
      return `${fId}-${cId}-${this.diagnostic.year}`
    },
    isTruthyOrZero(value) {
      return !!value || value === 0
    },
    checkTotal() {
      // we're only checking the total against the egalim and non-egalim fields. Each label group of the outsideLaw fields
      // can get up to 100% but ideally wouldn't go over that. We currently don't check this however because of UX constraints.
      const totalInputs = this.sumAllEgalimAndNonEgalim()
      const totalMeatPoultry = this.diagnostic.valueMeatPoultryHt
      const totalFish = this.diagnostic.valueFishHt
      const totalFamilies = totalMeatPoultry + totalFish

      this.errorMessage = ""
      this.errorType = undefined
      if (totalInputs > this.diagnostic.valueTotalHt) {
        this.errorType = "TOTAL"
        this.errorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${this.sumAllEgalimAndNonEgalim()} €`
        return false
      } else if (totalFamilies > this.diagnostic.valueTotalHt) {
        this.errorType = "FAMILY"
        this.errorMessage = `${DEFAULT_FAMILY_TOTAL_ERROR}, actuellement ${totalFamilies} €`
        return false
      } else if (this.isTruthyOrZero(totalMeatPoultry) && this.sumMeatVolailles() > totalMeatPoultry) {
        this.errorType = "MEAT"
        this.errorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${this.sumMeatVolailles()} €`
        return false
      } else if (this.isTruthyOrZero(totalFish) && this.sumFish() > totalFish) {
        this.errorType = "FISH"
        this.errorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${this.sumFish()} €`
        return false
      }
      return true
    },
    diagnosticKey(family, characteristic) {
      return this.camelize(`value_${family}_${characteristic}`)
    },
    summaryKey(family, characteristic) {
      return this.camelize(`${family}_${characteristic}`)
    },
    camelize(underscoredString) {
      const stringArray = underscoredString.split("_")
      let string = stringArray[0].toLowerCase()
      for (let index = 1; index < stringArray.length; index++) {
        string += stringArray[index].slice(0, 1).toUpperCase() + stringArray[index].slice(1).toLowerCase()
      }
      return string
    },
    qualityLabels(characteristicId) {
      let singleLabel
      let labelGroup
      switch (characteristicId) {
        case "LABEL_ROUGE":
          singleLabel = labels.find((l) => l.src.startsWith("label-rouge"))
          break
        case "AOCAOP_IGP_STG":
          labelGroup = [
            labels.find((l) => l.src.startsWith("Logo-AOC")),
            labels.find((l) => l.src.startsWith("IGP")),
            labels.find((l) => l.src.startsWith("STG")),
          ]
          return labelGroup
        case "HVE":
          singleLabel = labels.find((l) => l.src.startsWith("hve"))
          break
        case "PECHE_DURABLE":
          singleLabel = labels.find((l) => l.src.endsWith("peche-durable.png"))
          break
        case "RUP":
          singleLabel = labels.find((l) => l.src.startsWith("rup"))
          break
        case "COMMERCE_EQUITABLE":
          singleLabel = labels.find((l) => l.src.startsWith("commerce-equitable"))
          break
      }
      singleLabel = singleLabel || Constants.MiscLabelIcons[characteristicId]
      if (singleLabel) {
        return [singleLabel]
      }
    },
    labelSum(characteristicId) {
      let labelTotal = 0
      Object.keys(this.families).forEach((family) => {
        const key = this.diagnosticKey(family, characteristicId)
        labelTotal += parseFloat(this.diagnostic[key]) || 0
      })
      return labelTotal
    },
    sumAllEgalimAndNonEgalim() {
      const fields = this.characteristicGroups.egalim.fields.concat(this.characteristicGroups.nonEgalim.fields)
      return this.sumFields(fields)
    },
    sumMeatVolailles() {
      const fields = this.characteristicGroups.egalim.fields.concat(this.characteristicGroups.nonEgalim.fields)
      return this.sumFields(fields.filter((f) => f.startsWith("valueViandesVolailles")))
    },
    sumFish() {
      const fields = this.characteristicGroups.egalim.fields.concat(this.characteristicGroups.nonEgalim.fields)
      return this.sumFields(fields.filter((f) => f.startsWith("valueProduitsDeLaMer")))
    },
    sumFields(fields) {
      let totalInputs = 0
      fields.forEach((field) => {
        totalInputs += parseFloat(this.diagnostic[field]) || 0
      })
      return totalInputs
    },
    percentage(characteristicId) {
      const total = this.diagnostic.valueTotalHt
      if (!total) return
      const labelTotal = this.labelSum(characteristicId)
      const percentage = Math.round((labelTotal / total) * 100)
      if (percentage) {
        return `${percentage} %`
      } else if (labelTotal) {
        return "< 1 %"
      }
    },
  },
}
</script>

<style scoped>
.narrow-field {
  width: 50%;
}
</style>
