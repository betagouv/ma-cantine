<template>
  <div>
    <label :for="'total-' + diagnostic.year" class="body-2">
      La valeur (en HT) de mes achats alimentaires total
    </label>

    <v-text-field
      :id="'total-' + diagnostic.year"
      hide-details="auto"
      type="number"
      :rules="[
        validators.nonNegativeOrEmpty,
        validators.gteSum([diagnostic.valueBioHt, diagnostic.valueSustainableHt], totalErrorMessage),
      ]"
      validate-on-blur
      solo
      placeholder="Je ne sais pas"
      suffix="€ HT"
      v-model.number="diagnostic.valueTotalHt"
      :readonly="readonly"
      :disabled="readonly"
      :messages="totalError ? [totalErrorMessage] : undefined"
      :error="totalError"
      @blur="totalError = false"
      class="mt-2"
    ></v-text-field>

    <!-- TODO: a11y -->
    <p class="body-2 mt-6">Les valeurs de mes achats par label :</p>
    <v-expansion-panels class="mb-4 mt-2">
      <v-expansion-panel v-for="(characteristic, cId) in characteristics" :key="cId">
        <v-expansion-panel-header>
          <v-row align="center">
            <v-col
              cols="2"
              class="py-0 my-1 pr-0 d-flex align-center justify-center"
              style="display: block; height: 30px;"
            >
              <LogoBio v-if="cId === 'BIO'" style="max-width: 100%; max-height: 100%;" />
              <img
                v-for="label in qualityLabels(cId)"
                :key="label.title"
                :src="`/static/images/quality-labels/${label.src}`"
                :alt="label.title"
                :title="label.title"
                :style="label.style || 'max-width: 100%; height: inherit;'"
              />
            </v-col>
            <v-col>
              {{ characteristic.text }}
            </v-col>
          </v-row>
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
              ></v-text-field>
              <!--
                  :messages="totalError ? [totalErrorMessage] : undefined"
                  :error="totalError"
                  @blur="totalError = false"
                -->
            </v-col>
          </v-row>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    <!-- TODO: label referencing, validation, styling -->
  </div>
</template>

<script>
// import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import validators from "@/validators"
import Constants from "@/constants"
import LogoBio from "@/components/LogoBio"
import labels from "@/data/quality-labels.json"

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
      totalErrorMessage: "Le totale ne peut pas être moins que le somme des valeurs suivantes",
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
      // TODO: update
      const result = validators.gteSum(
        [this.diagnostic.valueBioHt, this.diagnostic.valueSustainableHt],
        this.totalErrorMessage
      )(this.diagnostic.valueTotalHt)
      this.totalError = result !== true
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
      if (singleLabel) {
        return [singleLabel]
      }
    },
  },
}
</script>
