<template>
  <div>
    <label :for="'total-' + diagnostic.year" class="body-2">
      La valeur (en HT) de mes achats alimentaires total
    </label>

    <v-text-field
      :id="'total-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[validators.nonNegativeOrEmpty]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueTotalHt"
      :readonly="readonly"
      :disabled="readonly"
      :error="totalError"
      :messages="totalError ? [totalErrorMessage] : undefined"
      @blur="checkTotal"
      class="mt-2"
    ></v-text-field>

    <!-- TODO: a11y -->
    <p class="body-2 mt-6">Les valeurs de mes achats par label :</p>
    <v-expansion-panels class="mb-4 mt-2">
      <v-expansion-panel v-for="(characteristic, cId) in characteristics" :key="cId">
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
                  :style="label.style || 'max-width: 100%; height: inherit;'"
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
              <v-col>{{ characteristic.text }}</v-col>
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
              <label :for="'total-' + diagnostic.year" class="body-2">
                {{ family.text }}
              </label>

              <v-text-field
                :id="`${fId}-${cId}-${diagnostic.year}`"
                hide-details="auto"
                type="number"
                :rules="[validators.nonNegativeOrEmpty]"
                validate-on-blur
                solo
                placeholder="Je ne sais pas"
                suffix="€ HT"
                v-model.number="diagnostic[camelize(`${fId}_${cId}`)]"
                :readonly="readonly"
                :disabled="readonly"
                class="mt-2"
                @blur="checkTotal"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script>
// import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import validators from "@/validators"
import Constants from "@/constants"
import LogoBio from "@/components/LogoBio"
import labels from "@/data/quality-labels.json"

const DEFAULT_TOTAL_ERROR = "Le totale doit être plus que le somme des valeurs par label"

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
    // PurchaseHint,
    LogoBio,
  },
  data() {
    return {
      totalError: false,
      totalErrorMessage: DEFAULT_TOTAL_ERROR,
      families: Constants.ProductFamilies,
      characteristics: Constants.TeledeclarationCharacteristics,
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
  },
  methods: {
    checkTotal() {
      const totalInputs = this.sumAll()
      if (totalInputs > this.diagnostic.valueTotalHt) {
        this.totalError = true
        this.totalErrorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${this.sumAll()} €`
      } else {
        this.totalError = false
      }
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
          labelGroup.forEach((l) => {
            l.style = "max-width: 30%; height: 'fit-content';"
          })
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
        case "FERMIER":
          singleLabel = {
            icon: "mdi-cow",
            color: "blue",
          }
          break
        case "EQUIVALENTS":
          singleLabel = {
            icon: "mdi-reflect-horizontal",
            color: "orange",
          }
          break
        case "EXTERNALITES":
          singleLabel = {
            icon: "mdi-flower-tulip-outline",
            color: "purple",
          }
          break
        case "PERFORMANCE":
          singleLabel = {
            icon: "mdi-chart-line",
            color: "green",
          }
          break
        case "FRANCE":
          singleLabel = {
            icon: "mdi-hexagon-outline",
            color: "brown",
          }
          break
        case "LOCAL":
          singleLabel = {
            icon: "mdi-map-marker-outline",
            color: "pink",
          }
          break
        case "SHORT_DISTRIBUTION":
          singleLabel = {
            icon: "mdi-chart-timeline-variant",
            color: "indigo",
          }
          break
      }
      if (singleLabel) {
        return [singleLabel]
      }
    },
    labelSum(characteristicId) {
      let labelTotal = 0
      Object.keys(this.families).forEach((family) => {
        const key = this.camelize(`${family}_${characteristicId}`)
        labelTotal += this.diagnostic[key] || 0
      })
      return labelTotal
    },
    sumAll() {
      let totalInputs = 0
      Object.keys(this.characteristics).forEach((characteristicId) => {
        totalInputs += this.labelSum(characteristicId)
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
