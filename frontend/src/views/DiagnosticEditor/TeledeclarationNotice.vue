<template>
  <div id="teledeclaration">
    <h2 class="font-weight-black text-h5 mt-8 mb-4">Télédéclarer mon diagnostic</h2>
    <p>
      Un bilan annuel relatif à la mise en œuvre des dispositions de la loi EGAlim, et notamment des objectifs
      d'approvisionnement en produits de qualité et durables dont bio dans les repas servis dans les restaurants
      collectifs, est prévu par le décret du 23 avril 2019.
    </p>
    <p>
      Nous vous proposons d’utiliser les informations de votre autodiagnostic {{ teledeclarationYear }} et de les
      transmettre, avec votre accord, à la DGAL, direction du Ministère de l'agriculture en charge de l'élaboration de
      ce bilan.
    </p>
    <v-form ref="teledeclarationForm" v-model="formValid" id="teledeclaration-form">
      <v-checkbox :rules="[validators.checked]" :disabled="disabled" @change="(x) => this.$emit('input', x)">
        <template v-slot:label>
          <span class="grey--text text--darken-3 font-weight-bold">
            Je déclare sur l’honneur la véracité de mes informations
          </span>
        </template>
      </v-checkbox>
    </v-form>
  </div>
</template>

<script>
import validators from "@/validators"

export default {
  data() {
    return {
      formValid: true,
    }
  },
  props: {
    value: {
      type: Boolean,
    },
    disabled: {
      type: Boolean,
    },
    teledeclarationYear: {
      type: Number,
    },
  },
  computed: {
    validators() {
      return validators
    },
  },
}
</script>

<style scoped>
#teledeclaration-form >>> .v-input--checkbox .v-label.theme--light {
  font-size: 16px;
  font-weight: bold;
  color: rgba(0, 0, 0, 0.87);
}
#teledeclaration-form >>> .v-input--checkbox .v-label.theme--light.v-label--is-disabled {
  color: rgba(0, 0, 0, 0.37);
}
</style>
