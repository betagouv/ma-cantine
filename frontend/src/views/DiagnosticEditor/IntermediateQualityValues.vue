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

    <v-row v-for="(group, groupId) in characteristicGroups" :key="groupId" class="mt-6">
      <v-divider class="mb-6"></v-divider>
      <p v-if="group.text" class="caption mb-4 ml-2">{{ group.text }}</p>
      <v-col cols="12" md="6" v-for="cId in group.characteristics" :key="cId">
        <div class="d-flex align-center">
          <LogoBio v-if="cId === 'BIO'" style="max-height: 34px;" />
          <div
            v-else
            v-for="label in qualityLabels(cId)"
            :key="label.title || label.icon"
            style="max-height: 34px; display: inline;"
          >
            <img
              v-if="label.src"
              :src="`/static/images/quality-labels/${label.src}`"
              :alt="label.title"
              :title="label.title"
              style="max-height: 34px;"
            />
            <v-icon class="mt-1" size="30" :color="label.color" v-else-if="label.icon">
              {{ label.icon }}
            </v-icon>
          </div>
          <label :for="inputHtmlId(cId)" class="body-2 ml-4">
            La valeur (en HT) de mes achats « {{ characteristics[cId].text }} »
          </label>
        </div>
        <div>
          <v-text-field
            :id="inputHtmlId(cId)"
            hide-details="auto"
            type="number"
            :rules="[validators.nonNegativeOrEmpty, validators.lteOrEmpty(diagnostic.valueTotalHt)]"
            validate-on-blur
            solo
            placeholder="Je ne sais pas"
            suffix="€ HT"
            v-model.number="diagnostic[diagnosticKey(cId)]"
            :readonly="readonly"
            :disabled="readonly"
            class="mt-2"
            @blur="checkTotal"
          ></v-text-field>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import LogoBio from "@/components/LogoBio"
import validators from "@/validators"
import Constants from "@/constants"
import labels from "@/data/quality-labels.json"

const DEFAULT_TOTAL_ERROR = "Le totale doit être plus que le somme des valeurs par label"

export default {
  name: "IntermediateQualityValues",
  props: {
    originalDiagnostic: Object,
    purchasesSummary: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  components: { LogoBio },
  data() {
    return {
      characteristicGroups: Constants.TeledeclarationCharacteristicGroups,
      characteristics: Constants.TeledeclarationCharacteristics,
      totalError: false,
      totalErrorMessage: DEFAULT_TOTAL_ERROR,
    }
  },
  computed: {
    hasActiveTeledeclaration() {
      return this.diagnostic.teledeclaration && this.diagnostic.teledeclaration.status === "SUBMITTED"
    },
    validators() {
      return validators
    },
    diagnostic() {
      return this.originalDiagnostic
    },
  },
  methods: {
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
    sumAllEgalim() {
      let totalInputs = 0
      this.characteristicGroups.egalim.characteristics.forEach((cId) => {
        totalInputs += parseFloat(this.diagnostic[this.diagnosticKey(cId)]) || 0
      })
      return totalInputs
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
      singleLabel = singleLabel || Constants.LabelIcons[characteristicId]
      if (singleLabel) {
        return [singleLabel]
      }
    },
    inputHtmlId(cId) {
      return `${cId}-${this.diagnostic.year}`
    },
    diagnosticKey(characteristic) {
      return this.camelize(`value_${characteristic}_ht`)
    },
    camelize(underscoredString) {
      const stringArray = underscoredString.split("_")
      let string = stringArray[0].toLowerCase()
      for (let index = 1; index < stringArray.length; index++) {
        string += stringArray[index].slice(0, 1).toUpperCase() + stringArray[index].slice(1).toLowerCase()
      }
      return string
    },
  },
}
</script>
