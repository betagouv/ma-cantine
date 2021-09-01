<template>
  <div>
    <v-checkbox
      hide-details="auto"
      v-model="diagnostic.hasDiversificationPlan"
      label="Si ma cantine fabrique plus de 200 repas par jour en moyenne, j'ai mis en place un plan pluriannuel de diversification des protéines incluant des alternatives à base de protéines végétales"
      :readonly="readonly"
      :disabled="readonly"
    />

    <p class="text-left mt-6 mb-2">J'ai mis en place un menu végétarien dans ma cantine :</p>
    <v-radio-group v-model="diagnostic.vegetarianWeeklyRecurrence">
      <v-radio
        class="ml-8"
        v-for="item in frequency"
        :key="item.value"
        :label="item.label"
        :value="item.value"
        :readonly="readonly"
        :disabled="readonly"
      ></v-radio>
    </v-radio-group>

    <p class="text-left mt-6 mb-2">Le menu végétarien proposé est :</p>
    <v-radio-group v-model="diagnostic.vegetarianMenuType">
      <v-radio
        class="ml-8"
        v-for="item in menuTypes"
        :key="item.value"
        :label="item.label"
        :value="item.value"
        :readonly="readonly"
        :disabled="readonly"
      ></v-radio>
    </v-radio-group>

    <p class="text-left mt-6 mb-2">Mon menu végétarien est à base :</p>
    <v-checkbox
      hide-details="auto"
      class="ml-8"
      v-model="diagnostic.vegetarianMenuBases"
      :multiple="true"
      v-for="item in menuBases"
      :key="item.value"
      :value="item.value"
      :label="item.label"
      :readonly="readonly"
      :disabled="readonly"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      frequency: [
        {
          label: "Moins d'une fois par semaine",
          value: "LOW",
        },
        {
          label: "Une fois par semaine",
          value: "MID",
        },
        {
          label: "Plus d'une fois par semaine",
          value: "HIGH",
        },
      ],
      menuTypes: [
        {
          label: "Un menu végétarien unique",
          value: "UNIQUE",
        },
        {
          label: "Plusieurs menus végétariens alternatifs",
          value: "SEVERAL",
        },
        {
          label: "Un menu végétarien alternatif à d'autres menus non-végétariens",
          value: "ALTERNATIVES",
        },
      ],
      menuBases: [
        {
          label: "De plats prêts à l'emploi",
          value: "READYMADE",
        },
        {
          label: "De légumes secs et céréales",
          value: "GRAIN",
        },
      ],
    }
  },
  props: {
    diagnostic: Object,
    readonly: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
