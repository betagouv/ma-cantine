<template>
  <div class="mt-n4">
    <p v-if="groupId === 'egalim'">
      <strong>Produit ayant plusieurs labels</strong>
      : la valeur d’achat ne pourra être comptée que dans une seule des catégories. Par exemple, un produit à la fois
      biologique et label rouge ne sera comptabilisé que dans la catégorie « bio ».
      <!-- TODO: list of prioritisation ? -->
    </p>
    <p v-else-if="groupId === 'nonEgalim'">
      Merci de renseigner les montants des produits hors EGAlim
    </p>
    <p v-else-if="groupId === 'outsideLaw'">
      Ici, vous pouvez affecter le produit dans plusieurs caractéristiques. Par exemple, un produit à la fois biologique
      et local pourra être comptabilisé dans les deux champs « bio » et « local ».
    </p>
    <p v-if="characteristicId === 'LOCAL'">
      Suivant votre propre définition de « local ».
    </p>
    <v-row>
      <v-col v-for="(family, fId) in families" :key="fId" cols="12" md="6" class="py-2">
        <label :for="fId" class="fr-text">
          {{ family.text }}
        </label>

        <DsfrCurrencyField
          :id="fId"
          :rules="[
            validators.nonNegativeOrEmpty,
            validators.decimalPlaces(2),
            validators.lteOrEmpty(payload.valueTotalHt),
          ]"
          solo
          v-model.number="payload[diagnosticKey(fId)]"
          class="mt-2"
        />
        <PurchaseHint
          v-if="displayPurchaseHints"
          v-model="payload[diagnosticKey(fId)]"
          :purchaseType="family.shortText + ' pour ce caractéristique'"
          :amount="purchasesSummary[diagnosticKey(fId)]"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import DsfrCurrencyField from "@/components/DsfrCurrencyField"
import PurchaseHint from "@/components/KeyMeasureDiagnostic/PurchaseHint"
import Constants from "@/constants"
import validators from "@/validators"

export default {
  name: "FamilyFieldsStep",
  props: {
    characteristicId: {
      type: String,
      required: true,
    },
    groupId: {
      type: String,
      required: true,
    },
    diagnostic: {
      type: Object,
      required: true,
    },
    payload: {
      type: Object,
      required: true,
    },
    purchasesSummary: {
      type: Object,
    },
  },
  components: {
    DsfrCurrencyField,
    PurchaseHint,
  },
  data() {
    return {
      families: Constants.ProductFamilies,
      validators,
    }
  },
  computed: {
    displayPurchaseHints() {
      return !!this.purchasesSummary
    },
  },
  methods: {
    diagnosticKey(family) {
      return this.camelize(`value_${family}_${this.characteristicId}`)
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

<style></style>
