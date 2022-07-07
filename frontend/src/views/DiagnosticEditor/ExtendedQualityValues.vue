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
                <v-col>{{ characteristics[cId].text }}</v-col>
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

                <v-text-field
                  :id="inputHtmlId(fId, cId)"
                  hide-details="auto"
                  type="number"
                  :rules="[validators.nonNegativeOrEmpty, validators.lteOrEmpty(diagnostic.valueTotalHt)]"
                  validate-on-blur
                  solo
                  placeholder="Je ne sais pas"
                  suffix="€ HT"
                  v-model.number="diagnostic[diagnosticKey(fId, cId)]"
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
  </div>
</template>

<script>
import validators from "@/validators"
import Constants from "@/constants"
import LogoBio from "@/components/LogoBio"
import labels from "@/data/quality-labels.json"

const DEFAULT_TOTAL_ERROR = "Le totale doit être plus que le somme des valeurs par label"

const MISC_LABELS = {
  FERMIER: {
    icon: "mdi-cow",
    color: "brown",
  },
  EXTERNALITES: {
    icon: "mdi-flower-tulip-outline",
    color: "purple",
  },
  PERFORMANCE: {
    icon: "mdi-chart-line",
    color: "green",
  },
  FRANCE: {
    icon: "mdi-hexagon-outline",
    color: "indigo",
  },
  SHORT_DISTRIBUTION: {
    icon: "mdi-chart-timeline-variant",
    color: "pink",
  },
  LOCAL: {
    icon: "mdi-map-marker-outline",
    color: "blue",
  },
}

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
  },
  data() {
    const characteristicGroups = Constants.TeledeclarationCharacteristicGroups
    return {
      totalError: false,
      totalErrorMessage: DEFAULT_TOTAL_ERROR,
      families: Constants.ProductFamilies,
      characteristics: Constants.TeledeclarationCharacteristics,
      characteristicGroups,
      fieldCount: {
        egalim: characteristicGroups.egalim.fields.length,
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
        outsideLaw: 0,
      }
      Object.entries(this.diagnostic).forEach(([field, value]) => {
        if (this.characteristicGroups.egalim.fields.indexOf(field) > -1) {
          completed.egalim += parseFloat(value, 10) >= 0 ? 1 : 0
        } else if (this.characteristicGroups.outsideLaw.fields.indexOf(field) > -1) {
          completed.outsideLaw += parseFloat(value, 10) >= 0 ? 1 : 0
        }
      })
      return completed
    },
    percentageCompletion() {
      return {
        egalim: Math.round((this.fieldsCompleted.egalim / this.fieldCount.egalim) * 100),
        outsideLaw: Math.round((this.fieldsCompleted.outsideLaw / this.fieldCount.outsideLaw) * 100),
      }
    },
  },
  methods: {
    inputHtmlId(fId, cId) {
      return `${fId}-${cId}-${this.diagnostic.year}`
    },
    checkTotal() {
      // we're only checking the total against the egalim fields. Each label group of the outsideLaw fields can get up to
      // 100% but ideally wouldn't go over that. We currently don't check this however because of UX constraints.
      const totalInputs = this.sumAllEgalim()
      if (totalInputs > this.diagnostic.valueTotalHt) {
        this.totalError = true
        this.totalErrorMessage = `${DEFAULT_TOTAL_ERROR}, actuellement ${this.sumAllEgalim()} €`
      } else {
        this.totalError = false
      }
    },
    diagnosticKey(family, characteristic) {
      return this.camelize(`value_${family}_${characteristic}`)
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
      }
      singleLabel = singleLabel || MISC_LABELS[characteristicId]
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
    sumAllEgalim() {
      let totalInputs = 0
      this.characteristicGroups.egalim.fields.forEach((field) => {
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
